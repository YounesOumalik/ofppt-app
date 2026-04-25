from fastapi import APIRouter, UploadFile, File, HTTPException, status
from sqlalchemy import select

from ..auth import require_roles, CurrentUser, DBSession
from ..models import Role, ImportLog, Groupe, Module, Diplome, Filiere, EFP, Formateur, Stagiaire
from ..schemas import ImportResult
from ..importers.parse_avancement import parse_avancement_excel
from ..importers.parse_stagiaires import parse_stagiaires_excel

router = APIRouter(prefix="/api/import", tags=["import"])


@router.post("/avancement", response_model=ImportResult, dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE, Role.DIRECTEUR_ETABLISSEMENT)])
async def import_avancement(
    file: UploadFile,
    user: CurrentUser,
    db: DBSession,
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Format .xlsx ou .xls attendu")

    content = await file.read()
    code_efp = user.code_efp or "TKM0"  # Default si complexe

    stats = parse_avancement_excel(content, code_efp, db)

    log = ImportLog(
        fichier=file.filename,
        type="avancement",
        utilisateur_id=user.id,
        lignes_lues=stats["lues"],
        lignes_inserees=stats["inserees"],
        lignes_mises_a_jour=stats["mises_a_jour"],
        erreurs=stats["erreurs"],
    )
    db.add(log)
    db.commit()

    return ImportResult(
        fichier=file.filename,
        type="avancement",
        lignes_lues=stats["lues"],
        lignes_inserees=stats["inserees"],
        lignes_mises_a_jour=stats["mises_a_jour"],
        erreurs=stats["erreurs"],
    )


@router.post("/stagiaires", response_model=ImportResult, dependencies=[require_roles(Role.DIRECTEUR_COMPLEXE, Role.DIRECTEUR_ETABLISSEMENT)])
async def import_stagiaires(
    file: UploadFile,
    user: CurrentUser,
    db: DBSession,
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Format .xlsx ou .xls attendu")

    content = await file.read()
    code_efp = user.code_efp or "TKM0"

    stats = parse_stagiaires_excel(content, code_efp, db)

    log = ImportLog(
        fichier=file.filename,
        type="stagiaire",
        utilisateur_id=user.id,
        lignes_lues=stats["lues"],
        lignes_inserees=stats["inserees"],
        lignes_mises_a_jour=stats["mises_a_jour"],
        erreurs=stats["erreurs"],
    )
    db.add(log)
    db.commit()

    return ImportResult(
        fichier=file.filename,
        type="stagiaire",
        lignes_lues=stats["lues"],
        lignes_inserees=stats["inserees"],
        lignes_mises_a_jour=stats["mises_a_jour"],
        erreurs=stats["erreurs"],
    )
