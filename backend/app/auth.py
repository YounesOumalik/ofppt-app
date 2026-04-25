from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import select

from .config import settings
from .db import get_db
from .models import Utilisateur, Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(p: str) -> str:
    return pwd_context.hash(p)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(sub: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRES_MIN)
    return jwt.encode({"sub": sub, "exp": expire}, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> Utilisateur:
    cred_exc = HTTPException(status.HTTP_401_UNAUTHORIZED, "Identifiants invalides")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO])
        sub = payload.get("sub")
        if not sub:
            raise cred_exc
    except JWTError:
        raise cred_exc
    user = db.execute(select(Utilisateur).where(Utilisateur.id == int(sub))).scalar_one_or_none()
    if not user or not user.actif:
        raise cred_exc
    return user


def require_roles(*roles: Role):
    def checker(user: Annotated[Utilisateur, Depends(get_current_user)]) -> Utilisateur:
        if user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Permission refusée")
        return user
    return checker


def scope_efp(user: Utilisateur) -> str | None:
    """Retourne le code_efp auquel filtrer les requêtes pour cet utilisateur, ou None si vue globale."""
    if user.role == Role.DIRECTEUR_COMPLEXE:
        return None
    return user.code_efp


CurrentUser = Annotated[Utilisateur, Depends(get_current_user)]
DBSession = Annotated[Session, Depends(get_db)]
