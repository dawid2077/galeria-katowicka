#auth.py
import jwt
from config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# HTTPBearer automatycznie wyciąga token z nagłówka Authorization (Bearer <token>)
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    # Upewnij się, że klucz jest w formacie PEM
    public_key = settings.CLERK_PUBLIC_KEY
    if not public_key.startswith("-----BEGIN PUBLIC KEY-----"):
        public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            # Zamiast wyłączać verify_aud, lepiej nie podawać go lub zweryfikować poprawnie
            options={"verify_aud": False} 
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )