from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

async def handle_route_error(e: Exception, status_code: status):
    raise HTTPException(
        detail=jsonable_encoder(e),
        status_code=status.HTTP_400_BAD_REQUEST
    )