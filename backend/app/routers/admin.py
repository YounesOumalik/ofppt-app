from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from sqlalchemy import select

from ..auth import hash_password, require_roles, CurrentUser, DBSession
from ..models import Utilisateur, Role, UserStatus
from ..schemas import UserOut, UserCreate, UserUpdate

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
async def list_users(user: CurrentUser, db: DBSession):
    """Lister les utilisateurs (filtrés selon rôle)."""
    if user.role == Role.DIRECTEUR_COMPLEXE:
        users = db.execute(select(Utilisateur)).scalars().all()
    elif user.role == Role.DIRECTEUR_ETABLISSEMENT:
        users = db.execute(select(Utilisateur).where(Utilisateur.code_efp == user.code_efp)).scalars().all()
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Accès refusé")
    return [UserOut.model_validate(u) for u in users]


@router.get("/users/pending", response_model=list[UserOut], dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE)])
async def list_pending_users(user: CurrentUser, db: DBSession):
    """Lister les utilisateurs EN ATTENTE DE VALIDATION."""
    users = db.execute(
        select(Utilisateur).where(Utilisateur.statut == UserStatus.PENDING_VALIDATION)
    ).scalars().all()
    return [UserOut.model_validate(u) for u in users]


@router.post("/users/{user_id}/validate", response_model=UserOut, dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE)])
async def validate_user(user_id: int, user: CurrentUser, db: DBSession):
    """🔓 Admin valide un nouvel utilisateur."""
    target = db.execute(select(Utilisateur).where(Utilisateur.id == user_id)).scalar_one_or_none()
    if not target:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Utilisateur non trouvé")

    if target.statut != UserStatus.PENDING_VALIDATION:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Utilisateur n'est pas en attente de validation")

    # Valider
    target.statut = UserStatus.ACTIVE
    target.valide_par = user.id
    target.date_validation = datetime.utcnow()
    db.commit()
    db.refresh(target)

    return UserOut.model_validate(target)


@router.post("/users/{user_id}/reject", dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE)])
async def reject_user(user_id: int, raison: str, user: CurrentUser, db: DBSession):
    """❌ Admin rejette un utilisateur en attente."""
    target = db.execute(select(Utilisateur).where(Utilisateur.id == user_id)).scalar_one_or_none()
    if not target:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if target.statut != UserStatus.PENDING_VALIDATION:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    target.statut = UserStatus.BANNED
    db.commit()
    return {"msg": f"Utilisateur rejeté. Raison: {raison}"}


@router.put("/users/{user_id}", response_model=UserOut, dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE, Role.DIRECTEUR_ETABLISSEMENT)])
async def update_user(user_id: int, req: UserUpdate, user: CurrentUser, db: DBSession):
    """Mettre à jour un utilisateur."""
    target = db.execute(select(Utilisateur).where(Utilisateur.id == user_id)).scalar_one_or_none()
    if not target:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if user.role == Role.DIRECTEUR_ETABLISSEMENT and target.code_efp != user.code_efp:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    if req.nom_complet:
        target.nom_complet = req.nom_complet
    if req.role:
        target.role = req.role
    if req.code_efp:
        target.code_efp = req.code_efp
    if req.actif is not None:
        target.actif = req.actif

    db.commit()
    db.refresh(target)
    return UserOut.model_validate(target)


@router.delete("/users/{user_id}", dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE, Role.DIRECTEUR_ETABLISSEMENT)])
async def deactivate_user(user_id: int, user: CurrentUser, db: DBSession):
    """Désactiver un utilisateur."""
    target = db.execute(select(Utilisateur).where(Utilisateur.id == user_id)).scalar_one_or_none()
    if not target:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if user.role == Role.DIRECTEUR_ETABLISSEMENT and target.code_efp != user.code_efp:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    target.statut = UserStatus.INACTIVE
    target.actif = False
    db.commit()
    return {"msg": "Utilisateur désactivé"}
