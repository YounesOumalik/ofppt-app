from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from ..auth import require_roles, CurrentUser, DBSession
from ..models import Role, Salle, Groupe, Formateur, Module, Filiere
from ..schemas import SalleIn, SalleOut, GroupeIn, GroupeOut, FormateurIn, FormateurOut, FiliereOut, ModuleOut

router = APIRouter(prefix="/api/parametrage", tags=["parametrage"])


@router.get("/salles", response_model=list[SalleOut])
async def list_salles(user: CurrentUser, db: DBSession):
    if user.role == Role.DIRECTEUR_COMPLEXE:
        salles = db.execute(select(Salle)).scalars().all()
    else:
        salles = db.execute(select(Salle).where(Salle.code_efp == user.code_efp)).scalars().all()
    return [SalleOut.model_validate(s) for s in salles]


@router.post("/salles", response_model=SalleOut, dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE, Role.DIRECTEUR_ETABLISSEMENT)])
async def create_salle(req: SalleIn, user: CurrentUser, db: DBSession):
    if user.role == Role.DIRECTEUR_ETABLISSEMENT and req.code_efp != user.code_efp:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    salle = Salle(**req.model_dump())
    db.add(salle)
    db.commit()
    db.refresh(salle)
    return SalleOut.model_validate(salle)


@router.put("/salles/{salle_id}", response_model=SalleOut, dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE, Role.DIRECTEUR_ETABLISSEMENT)])
async def update_salle(salle_id: int, req: SalleIn, user: CurrentUser, db: DBSession):
    salle = db.execute(select(Salle).where(Salle.id == salle_id)).scalar_one_or_none()
    if not salle:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if user.role == Role.DIRECTEUR_ETABLISSEMENT and salle.code_efp != user.code_efp:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    for k, v in req.model_dump().items():
        setattr(salle, k, v)
    db.commit()
    db.refresh(salle)
    return SalleOut.model_validate(salle)


@router.get("/groupes", response_model=list[GroupeOut])
async def list_groupes(user: CurrentUser, db: DBSession):
    if user.role == Role.DIRECTEUR_COMPLEXE:
        groupes = db.execute(select(Groupe)).scalars().all()
    else:
        groupes = db.execute(select(Groupe).where(Groupe.code_efp == user.code_efp)).scalars().all()
    return [GroupeOut.model_validate(g) for g in groupes]


@router.post("/groupes", response_model=GroupeOut, dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE, Role.DIRECTEUR_ETABLISSEMENT)])
async def create_groupe(req: GroupeIn, user: CurrentUser, db: DBSession):
    if user.role == Role.DIRECTEUR_ETABLISSEMENT and req.code_efp != user.code_efp:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    # Vérifier unicité
    existing = db.execute(select(Groupe).where(Groupe.code_groupe == req.code_groupe)).scalar_one_or_none()
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Groupe déjà existant")

    groupe = Groupe(**req.model_dump())
    db.add(groupe)
    db.commit()
    db.refresh(groupe)
    return GroupeOut.model_validate(groupe)


@router.put("/groupes/{code}", response_model=GroupeOut, dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE, Role.DIRECTEUR_ETABLISSEMENT)])
async def update_groupe(code: str, req: GroupeIn, user: CurrentUser, db: DBSession):
    groupe = db.execute(select(Groupe).where(Groupe.code_groupe == code)).scalar_one_or_none()
    if not groupe:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if user.role == Role.DIRECTEUR_ETABLISSEMENT and groupe.code_efp != user.code_efp:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    for k, v in req.model_dump().items():
        setattr(groupe, k, v)
    db.commit()
    db.refresh(groupe)
    return GroupeOut.model_validate(groupe)


@router.get("/formateurs", response_model=list[FormateurOut])
async def list_formateurs(user: CurrentUser, db: DBSession):
    if user.role == Role.DIRECTEUR_COMPLEXE:
        formateurs = db.execute(select(Formateur)).scalars().all()
    else:
        formateurs = db.execute(select(Formateur).where(Formateur.code_efp == user.code_efp)).scalars().all()
    return [FormateurOut.model_validate(f) for f in formateurs]


@router.post("/formateurs", response_model=FormateurOut, dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE, Role.DIRECTEUR_ETABLISSEMENT)])
async def create_formateur(req: FormateurIn, user: CurrentUser, db: DBSession):
    if req.code_efp and user.role == Role.DIRECTEUR_ETABLISSEMENT and req.code_efp != user.code_efp:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    existing = db.execute(select(Formateur).where(Formateur.matricule == req.matricule)).scalar_one_or_none()
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Formateur déjà existant")

    formateur = Formateur(**req.model_dump())
    db.add(formateur)
    db.commit()
    db.refresh(formateur)
    return FormateurOut.model_validate(formateur)


@router.put("/formateurs/{matricule}", response_model=FormateurOut, dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE, Role.DIRECTEUR_ETABLISSEMENT)])
async def update_formateur(matricule: str, req: FormateurIn, user: CurrentUser, db: DBSession):
    formateur = db.execute(select(Formateur).where(Formateur.matricule == matricule)).scalar_one_or_none()
    if not formateur:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if user.role == Role.DIRECTEUR_ETABLISSEMENT and formateur.code_efp != user.code_efp:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    for k, v in req.model_dump().items():
        setattr(formateur, k, v)
    db.commit()
    db.refresh(formateur)
    return FormateurOut.model_validate(formateur)
