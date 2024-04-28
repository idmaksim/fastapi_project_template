import os
import shutil

from fastapi.responses import FileResponse, JSONResponse
from fastapi import APIRouter, HTTPException, File, UploadFile, status
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix='/images',
    tags=['Images']
)

if not os.path.exists('../images'):
    os.mkdir('../images')


@router.post('')
async def add_image(
    image_name: str,
    file: UploadFile = File(...)
):
    try:
        print(os.getcwd())
        image_path = f'../images/{image_name}.png'


        if os.path.exists(image_path):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='image with this name already exists'
            )

        with open(image_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        del buffer

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(
                detail=f'image {image_name} succesfully added: {os.path.exists(image_path)}'
            )
        )   
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{error}'
        )
    

@router.get('')
async def get_image(
    image_name: str
):
    image_name = "../images/" + image_name + ".png"
    if os.path.exists(image_name):
        return FileResponse(
            path=image_name
        )
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND   ,
        detail='image not found'   
    )
