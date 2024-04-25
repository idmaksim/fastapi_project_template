import table_models
from db import get_db
from random import randint
from sqlalchemy.orm import Session
from email_sender import send_email
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix='/verification_code',
    tags=['Verification Codes']
)


@router.get('/send')
async def send_verification_code(
        email: str,
        db: Session = Depends(get_db)
    ):
    
    current_code: int = randint(100000, 999999)
    
    recipient_info: dict = dict(
        verification_code=current_code,
        email=email
    )
    
    await send_email(email, "OTP Verification", f"{current_code}")

    query = db.query(table_models.VerificationCodes).filter(
        table_models.VerificationCodes.email == email
    )

    old_recipient_info = query.first()

    if old_recipient_info is None:
        new_recipient_info = table_models.VerificationCodes(**recipient_info)
        db.add(new_recipient_info)
        db.commit()
        db.refresh(new_recipient_info)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(
                data=new_recipient_info
            )
        )

    else:
        query.update(recipient_info, synchronize_session=False)
        try:
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(
                    data=recipient_info
                )
            )

        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error
            )
