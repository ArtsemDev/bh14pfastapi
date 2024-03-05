from pydantic import BaseModel, EmailStr, Field, model_validator

from profile.types import PasswordStr


class UserRegisterForm(BaseModel):
    email: EmailStr
    password: PasswordStr = Field(default=..., min_length=8, max_length=64)
    confirm_password: PasswordStr = Field(default=..., min_length=8, max_length=64)

    @model_validator(mode="after")
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("password does not match confirm password")

        if self.email.lower().split("@")[0] in self.password.lower():
            raise ValueError("password has not contain email")

        return self


class UserLoginForm(BaseModel):
    email: EmailStr
    password: PasswordStr = Field(default=..., min_length=8, max_length=64)
