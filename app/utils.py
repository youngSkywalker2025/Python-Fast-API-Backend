# app/utils.py
from passlib.context import CryptContext

# Tell Passlib which hashing algorithm to use
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str) -> str:
    """Return the bcrypt hash of the given password."""
    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password: str) -> bool:
    """Check if plain_password matches the hashed_password."""
    # hashes the plain password internally, then checks if it equals the stored hash
    return pwd_context.verify(plain_password, hashed_password)


