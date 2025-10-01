import pytest
from jose import jwt, ExpiredSignatureError
from app import auth_utils
from app.routers import auth
from app.auth_utils import ALGORITHM, settings

def test_hash_and_verify_password():
    password = "my_secret"
    hashed = auth_utils.hash_password(password)
    assert hashed != password
    assert auth_utils.verify_password(password, hashed)
    assert not auth_utils.verify_password("wrong_password", hashed)

def test_create_access_token():
    sub = "testuser@example.com"
    token = auth_utils.create_access_token(sub)
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == sub
    assert "exp" in decoded

def test_expired_token():
    sub = "expireduser@example.com"
    token = auth.create_access_token(sub=sub, expires_minutes=-1)

    with pytest.raises(ExpiredSignatureError):
        jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])