import pytest
from src.domain.user import value_objects as vo
from src.domain.user.value_objects.auth_token import (
    AuthTokenIsEmptyException,
    AuthTokenTooLongException,
)
from src.domain.user.value_objects.full_name import (
    FullNameIsEmptyException,
    FullNameIsNotCorrectFormatException,
    FullNameTooLongException,
)
from src.domain.user.value_objects.password import (
    EmptyPasswordException,
    TooLongPasswordException,
    WrongPasswordException,
)
from src.domain.user.value_objects.username import (
    EmptyUsernameException,
    TooLongUsernameException,
    WrongUsernameFormatException,
)


def test_username_is_valid():
    username_too__much__text = "f"
    username_empty = ""
    username_wrong__format = "_gfdgdsfgr@@"

    with pytest.raises(TooLongUsernameException):
        vo.UserName(username_too__much__text * 200)

    with pytest.raises(EmptyUsernameException):
        vo.UserName(username_empty)

    with pytest.raises(WrongUsernameFormatException):
        vo.UserName(username_wrong__format)


def test_password_is_valid():
    password_empty = ""
    password_is_too_long = "Passweodsffveedffffffffffffffffffffffffffffffffffxdfdf2"
    password_wrong_format = "3445343434"

    with pytest.raises(EmptyPasswordException):
        vo.Password(password_empty)

    with pytest.raises(TooLongPasswordException):
        vo.Password(password_is_too_long)

    with pytest.raises(WrongPasswordException):
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
        ("Artem", "Rybakov", "", FullNameIsEmptyException),
        ("Artem", "Rybakov", "Artem Rybakov" * 200, FullNameTooLongException),
        ("Artem", "Rybakov", "__@@fullname", FullNameIsNotCorrectFormatException),
        ("", "Rybakov", "Artem Rybakov", FullNameIsEmptyException),
        ("Artem" * 200, "Rybakov", "Artem Rybakov", FullNameTooLongException),
        (
            "___##@@~~Artem",
            "Rybakov",
            "Artem Rybakov",
            FullNameIsNotCorrectFormatException,
        ),
        ("Artem", "", "Artem Rybakov", FullNameIsEmptyException),
        ("Artem", "Rybakov" * 200, "Artem Rybakov", FullNameTooLongException),
        (
            "Artem",
            "___##@@~~Rybakov",
            "Artem Rybakov",
            FullNameIsNotCorrectFormatException,
        ),
    ],
)
def test_fullname_is_valid(first_name, last_name, fullname, expected_exception):
    with pytest.raises(expected_exception):
        vo.FullName(first_name, last_name, fullname)
