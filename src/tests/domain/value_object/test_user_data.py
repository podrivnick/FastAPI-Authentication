import pytest
from src.domain.user import value_objects as vo
from src.domain.user.value_objects.auth_token import (
    AuthTokenIsEmptyException,
    AuthTokenTooLongException,
)
from src.domain.user.value_objects.full_name import (
    FullNameIsEmpty,
    FullNameIsNotCorrectFormat,
    FullNameTooLong,
)
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


def test_auth_token_is_valid():
    auth_token_empty = ""
    auth_token_is_too_long = "fdsdf3"

    with pytest.raises(AuthTokenIsEmptyException):
        vo.AuthToken(auth_token_empty)

    with pytest.raises(AuthTokenTooLongException):
        vo.AuthToken(auth_token_is_too_long * 200)


@pytest.mark.parametrize(
    "first_name, last_name, fullname, expected_exception",
    [
        ("Artem", "Rybakov", "", FullNameIsEmpty),
        ("Artem", "Rybakov", "Artem Rybakov" * 200, FullNameTooLong),
        ("Artem", "Rybakov", "__@@fullname", FullNameIsNotCorrectFormat),
        ("", "Rybakov", "Artem Rybakov", FullNameIsEmpty),
        ("Artem" * 200, "Rybakov", "Artem Rybakov", FullNameTooLong),
        ("___##@@~~Artem", "Rybakov", "Artem Rybakov", FullNameIsNotCorrectFormat),
        ("Artem", "", "Artem Rybakov", FullNameIsEmpty),
        ("Artem", "Rybakov" * 200, "Artem Rybakov", FullNameTooLong),
        ("Artem", "___##@@~~Rybakov", "Artem Rybakov", FullNameIsNotCorrectFormat),
    ],
)
def test_fullname_is_valid(first_name, last_name, fullname, expected_exception):
    with pytest.raises(expected_exception):
        vo.FullName(first_name, last_name, fullname)
