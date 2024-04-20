import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routers import user_routes, verification_code_routes


class Server:
    def __init__(self, ip: str, port: int) -> None:
        self.__ip = ip
        self.__port = port
        self.app = FastAPI(debug=True, title="YOUR API NAME", version="YOUR API VERSION")

    def init_routes(self):
        self.app.include_router(user_routes.router)
        self.app.include_router(verification_code_routes.router)

        @self.app.get("/", include_in_schema=False)
        async def redirect_to_docs():
            return RedirectResponse("/docs")

    def run(self):
        uvicorn.run(
            self.app,
            host=self.__ip,
            port=self.__port
        )
