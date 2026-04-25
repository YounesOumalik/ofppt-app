from fastapi import APIRouter, Query
from sqlalchemy import select

from ..auth import CurrentUser, DBSession
from ..models import Role, Stagiaire, Groupe, Formateur, Module, Avancement, Inscription
from ..schemas import StagiaireOut, GroupeOut, FormateurOut, ModuleOut, AvancementOut

router = APIRouter(prefix="/api/data", tags=["data"])


@router.get("/stagiaires", response_model=list[StagiaireOut])
async def list_stagiaires(user: CurrentUser, db: DBSession, search: str = Query("")):
    # Stagiaires du groupe si gestionnaire, tous si complexe
    if user.role == Role.DIRECTEUR_COMPLEXE:
        stagiaires = db.execute(select(Stagiaire)).scalars().all()
    else:
        # Stagiaires de son EFP
        inscriptions = db.execute(
            select(Inscription).where(Inscription.code_efp == user.code_efp)
        ).scalars().all()
        matricules = [i.stagiaire_matricule for i in inscriptions]
        stagiaires = db.execute(
            select(Stagiaire).where(Stagiaire.matricule.in_(matricules))
        ).scalars().all() if matricules else []

    if search:
        stagiaires = [s for s in stagiaires if search.lower() in (s.nom or "").lower() or search.lower() in (s.prenom or "").lower()]

    return [StagiaireOut.model_validate(s) for s in stagiaires]


@router.get("/groupes", response_model=list[GroupeOut])
async def list_groupes(user: CurrentUser, db: DBSession, code_efp: str = Query(None)):
    if user.role == Role.DIRECTEUR_COMPLEXE:
        query = select(Groupe)
        if code_efp:
            query = query.where(Groupe.code_efp == code_efp)
    else:
        query = select(Groupe).where(Groupe.code_efp == user.code_efp)

    groupes = db.execute(query).scalars().all()
    return [GroupeOut.model_validate(g) for g in groupes]


@router.get("/formateurs", response_model=list[FormateurOut])
async def list_formateurs(user: CurrentUser, db: DBSession):
    if user.role == Role.DIRECTEUR_COMPLEXE:
        formateurs = db.execute(select(Formateur)).scalars().all()
    else:
        formateurs = db.execute(select(Formateur).where(Formateur.code_efp == user.code_efp)).scalars().all()

    return [FormateurOut.model_validate(f) for f in formateurs]


@router.get("/modules", response_model=list[ModuleOut])
async def list_modules(user: CurrentUser, db: DBSession):
    modules = db.execute(select(Module)).scalars().all()
    return [ModuleOut.model_validate(m) for m in modules]


@router.get("/avancement", response_model=list[AvancementOut])
async def list_avancement(user: CurrentUser, db: DBSession, code_groupe: str = Query(None)):
    if user.role == Role.DIRECTEUR_COMPLEXE:
        query = select(Avancement)
    else:
        query = select(Avancement).where(Avancement.code_efp == user.code_efp)

    if code_groupe:
        query = query.where(Avancement.code_groupe == code_groupe)

    avancement = db.execute(query).scalars().all()
    return [AvancementOut.model_validate(a) for a in avancement]
