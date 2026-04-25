from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from sqlalchemy import select

from ..auth import hash_password, verify_password, create_access_token, CurrentUser, DBSession
from ..models import Utilisateur, Role, UserStatus
from ..schemas import LoginIn, TokenOut, UserOut, UserCreate, PasswordChange

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup")
async def signup(req: UserCreate, db: DBSession):
    """Inscription d'un nouvel utilisateur - EN ATTENTE DE VALIDATION ADMIN."""
    # Vérifier email unique
    existing = db.execute(select(Utilisateur).where(Utilisateur.email == req.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email déjà enregistré")

    # Créer l'utilisateur en statut PENDING_VALIDATION
    new_user = Utilisateur(
        email=req.email,
        password_hash=hash_password(req.password),
        nom_complet=req.nom_complet,
        role=Role.DIRECTEUR_ETABLISSEMENT,  # Rôle par défaut pour nouveaux
        code_efp=req.code_efp,
        statut=UserStatus.PENDING_VALIDATION,  # 🔒 En attente de validation
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "msg": "Inscription réussie. En attente de validation admin.",
        "email": req.email,
        "statut": UserStatus.PENDING_VALIDATION.value,
    }


@router.post("/login", response_model=TokenOut)
async def login(req: LoginIn, db: DBSession):
    user = db.execute(select(Utilisateur).where(Utilisateur.email == req.email)).scalar_one_or_none()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email ou mot de passe incorrect")

    # 🔒 Vérifier que l'utilisateur est validé ET actif
    if user.statut != UserStatus.ACTIVE:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Compte non actif. Statut: {user.statut.value}. Contactez l'admin."
        )
    if not user.actif:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Compte désactivé")

    user.dernier_login = datetime.utcnow()
    db.commit()
    token = create_access_token(str(user.id))
    return TokenOut(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
async def get_current(user: CurrentUser):
    return UserOut.model_validate(user)


@router.post("/password-change")
async def change_password(new_pwd: str, user: CurrentUser, db: DBSession):
    user.password_hash = hash_password(new_pwd)
    db.commit()
    return {"msg": "Mot de passe modifié"}
