from wtforms import Form
from wtforms.csrf.core import CSRF
from wtforms.csrf.session import SessionCSRF
from wtforms.fields import *
from wtforms.widgets import *
from wtforms.validators import *

from hashlib import md5

SECRET_KEY = '1234567890'

class IPAddressCSRF(CSRF):
    """
    Generate a CSRF token based on the user's IP. I am probably not very
    secure, so don't use me.
    """
    def setup_form(self, form):
        self.csrf_context = form.meta.csrf_context
        return super(IPAddressCSRF, self).setup_form(form)

    def generate_csrf_token(self, csrf_token):
        token = md5((SECRET_KEY + self.csrf_context).encode()).hexdigest()
        return token

    def validate_csrf_token(self, form, field):
        if field.data != field.current_token:
            raise ValueError('Invalid CSRF')


class FeedbackForm(Form):
    email = EmailField(render_kw={"placeholder": "Your email"})
    message = TextAreaField(render_kw={"placeholder": "Your Message"})

    class Meta:
        csrf = True
        csrf_class = IPAddressCSRF
