from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from app.settings import settings
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password=password)
def verify_password(password:str, saved_hash:str) -> bool:
    return password_hash.verify(password=password, hash=saved_hash)
ALGORITHM = "HS256"
def create_access_token(user_id: int) -> str:
    payload = {
        "sub": f"{user_id}",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    }
    encoded = jwt.encode(payload, settings.secret_key, ALGORITHM)
    return encoded
def decode_access_token(token: str, algorithms: list[str]) -> int | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=algorithms)
        return int(payload["sub"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
