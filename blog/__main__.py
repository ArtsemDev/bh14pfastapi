from fastapi import FastAPI

from blog.handlers import router


app = FastAPI()
app.include_router(router=router)


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host="0.0.0.0",
        port=80
    )
