# app/security.py (or wherever your hashing lives)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def truncate_password_to_72_bytes(password: str) -> str:
    """Truncate password to 72 bytes (bcrypt limit), preserving UTF-8 safety."""
    if isinstance(password, str):
        pwd_bytes = password.encode("utf-8")
        if len(pwd_bytes) > 72:
            # Truncate to 72 bytes, then decode back — ignore decode errors
            return pw.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return password

def _normalize_password(pw: str) -> str:
    b = pw.encode("utf-8")
    return pw.encode("utf-8")[:72].decode("utf-8", errors="ignore")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(_normalize_password(password))

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(_normalize_password(plain), hashed)