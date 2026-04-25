from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

from ..models.acteur import Role


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    nom_complet: str
    role: Role
    code_efp: str | None = None
    actif: bool
    formateur_matricule: str | None = None
    stagiaire_matricule: str | None = None
    cree_le: datetime
    dernier_login: datetime | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nom_complet: str
    role: Role
    code_efp: str | None = None
    formateur_matricule: str | None = None
    stagiaire_matricule: str | None = None


class UserUpdate(BaseModel):
    nom_complet: str | None = None
    role: Role | None = None
    code_efp: str | None = None
    actif: bool | None = None


class PasswordChange(BaseModel):
    new_password: str


TokenOut.model_rebuild()
