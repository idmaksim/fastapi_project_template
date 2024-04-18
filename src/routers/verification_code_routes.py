from db import get_db
from sqlalchemy.orm import Session
import table_models
from fastapi import Depends, APIRouter, HTTPException
from random import randint
from email_sender import send_email

router = APIRouter(
    prefix='/verification_code',
    tags=['Verification Codes']
)


@router.get('/send', status_code=200)
async def verification_code_get(email: str, db: Session = Depends(get_db)):
    
    current_code: int = randint(100000, 999999)
    
    recipient_info: dict = dict(
        verification_code=current_code,
        email=email
    )
    
    await send_email(email, "OTP Verification", f"{current_code}")

    query = db.query(table_models.VerificationCodes).filter(
        table_models.VerificationCodes.email ==email
    )

    old_recipient_info = query.first()

    if old_recipient_info is None:
        new_recipient_info = table_models.VerificationCodes(**recipient_info)

        db.add(new_recipient_info)
        db.commit()

        db.refresh(new_recipient_info)

        return dict(
            data=new_recipient_info
        )

    else:

        query.update(recipient_info, synchronize_session=False)

        try:
            db.commit()

            return dict(
                data=recipient_info
            )

        except:
            raise HTTPException(
                status_code=304,
                detail='cant update vc'
            )
