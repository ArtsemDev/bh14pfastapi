from re import compile

from annotated_types import Annotated, Predicate


PASSWORD_PATTERN = compile(pattern=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,64}$")


def _check_strong_password(v: str) -> bool:
    if PASSWORD_PATTERN.fullmatch(string=v):
        return True
    return False


PasswordStr = Annotated[str, Predicate(func=_check_strong_password)]
