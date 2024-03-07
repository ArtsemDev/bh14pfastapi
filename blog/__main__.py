from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from blog import views
from blog.handlers import router
from src.config import static

app = FastAPI()
app.add_middleware(middleware_class=GZipMiddleware)
app.add_middleware(middleware_class=ProxyHeadersMiddleware, trusted_hosts=("*", ))

app.mount(path="/static", app=static, name="static")
app.include_router(router=router)
app.include_router(router=views.router)


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host="0.0.0.0",
        port=80
    )
