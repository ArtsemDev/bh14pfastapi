from fastapi import APIRouter
from starlette.requests import Request
from markupsafe import Markup
from wtforms.csrf.session import SessionCSRF

from blog.forms import FeedbackForm
from src.config import templating
from src.tasks import ping

router = APIRouter(include_in_schema=False)


@router.get(path="/")
async def index(request: Request):
    task = ping.delay()
    print(task)
    print(type(task))
    tag = Markup(base="<a href=\"https://google.com\">LINK</a>")
    return templating.TemplateResponse(
        request=request,
        name="blog/index.html",
        context={
            "products": [
                {
                    "name": "Product 1",
                    "min_price": 100,
                    "max_price": 200
                },
                {
                    "name": "Product 2",
                    "min_price": 150,
                    "max_price": 300
                },
            ],
            "tag": tag,
            "feedback_form": FeedbackForm(meta={"csrf_context": request.client.host})
        }
    )


@router.post(path="/")
async def post_index(request: Request):
    form = FeedbackForm(await request.form(), meta={"csrf_context": request.client.host})
    if form.validate():
        print("GOOD")
        print(form.data)
        form = FeedbackForm(meta={"csrf_context": request.client.host})
    else:
        print("NOT GOOD")
    return templating.TemplateResponse(
        request=request,
        name="blog/index.html",
        context={
            "products": [
                {
                    "name": "Product 1",
                    "min_price": 100,
                    "max_price": 200
                },
                {
                    "name": "Product 2",
                    "min_price": 150,
                    "max_price": 300
                },
            ],
            "feedback_form": form
        }
    )
