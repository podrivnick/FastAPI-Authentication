import pytest
from src.domain.user import value_objects as vo
from src.domain.user.value_objects.password import (
    EmptyPasswordError,
    TooLongPasswordError,
    WrongPasswordFormatError,
)
from src.domain.user.value_objects.username import (
    EmptyUsernameError,
    TooLongUsernameError,
    WrongUsernameFormatError,
)


def test_username_is_valid():
    username_too__much__text = "f"
    username_empty = ""
    username_wrong__format = "_gfdgdsfgr@@"

    with pytest.raises(TooLongUsernameError):
        vo.UserName(username_too__much__text * 200)

    with pytest.raises(EmptyUsernameError):
        vo.UserName(username_empty)

    with pytest.raises(WrongUsernameFormatError):
        vo.UserName(username_wrong__format)


def test_password_is_valid():
    password_empty = ""
    password_is_too_long = "Passweodsffveedffffffffffffffffffffffffffffffffffxdfdf2"
    password_wrong_format = "3445343434"

    with pytest.raises(EmptyPasswordError):
        vo.Password(password_empty)

    with pytest.raises(TooLongPasswordError):
        vo.Password(password_is_too_long)

    with pytest.raises(WrongPasswordFormatError):
        vo.Password(password_wrong_format)
