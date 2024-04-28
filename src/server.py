import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from routers import (
    image_routes, 
    user_routes, 
    verification_code_routes,
    exercise_routes,
    muscle_group_routes,
    session_routes
)


class Server:
    def __init__(self, ip: str, port: int) -> None:
        self.__ip = ip
        self.__port = port
        self.__app = FastAPI(debug=True, title="SOON", version="beta 1.0")

    def init_routes(self):
        self.__app.include_router(user_routes.router)
        self.__app.include_router(verification_code_routes.router)
        self.__app.include_router(image_routes.router)
        self.__app.include_router(exercise_routes.router)
        self.__app.include_router(muscle_group_routes.router)
        self.__app.include_router(session_routes.router)

        @self.__app.get("/", include_in_schema=False)
        async def redirect_to_docs():
            return RedirectResponse("/docs")
        
        @self.__app.get('/download')
        async def download_apk():
            return FileResponse(
                path='../apk/app-release.apk',
                media_type='application/octet-stream',
                filename='release.apk'
            )

    def run(self):
        uvicorn.run(
            app=self.__app,
            host=self.__ip,
            port=self.__port
        )
