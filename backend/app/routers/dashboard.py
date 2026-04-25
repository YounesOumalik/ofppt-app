from fastapi import APIRouter, Query
from sqlalchemy import select, func

from ..auth import CurrentUser, DBSession
from ..models import Role, Groupe, Formateur, Stagiaire, Avancement, Salle, Inscription
from ..schemas import DashboardKPI

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/kpi", response_model=DashboardKPI)
async def get_kpi(user: CurrentUser, db: DBSession, code_efp: str = Query(None)):
    # Filtrer par EFP
    if user.role == Role.DIRECTEUR_COMPLEXE and code_efp:
        scope_efp = code_efp
    elif user.role == Role.DIRECTEUR_COMPLEXE:
        scope_efp = None  # Tous les EFP
    else:
        scope_efp = user.code_efp

    # Groupes
    query_groupes = select(Groupe)
    if scope_efp:
        query_groupes = query_groupes.where(Groupe.code_efp == scope_efp)
    groupes = db.execute(query_groupes).scalars().all()
    nb_groupes = len(groupes)
    effectif_total = sum(g.effectif for g in groupes)

    # Formateurs
    query_fmt = select(Formateur)
    if scope_efp:
        query_fmt = query_fmt.where(Formateur.code_efp == scope_efp)
    formateurs = db.execute(query_fmt).scalars().all()
    nb_fp = len([f for f in formateurs if f.type == "FP"])
    nb_fv = len([f for f in formateurs if f.type == "FV"])

    # Salles
    query_salles = select(Salle)
    if scope_efp:
        query_salles = query_salles.where(Salle.code_efp == scope_efp)
    salles = db.execute(query_salles).scalars().all()
    nb_salles = len(salles)

    # Stagiaires actifs
    query_insc = select(Inscription).where(Inscription.actif == True)
    if scope_efp:
        query_insc = query_insc.where(Inscription.code_efp == scope_efp)
    inscriptions = db.execute(query_insc).scalars().all()
    nb_stagiaires_actifs = len(set(i.stagiaire_matricule for i in inscriptions))

    # Avancement
    query_adv = select(Avancement)
    if scope_efp:
        query_adv = query_adv.where(Avancement.code_efp == scope_efp)
    avancement_list = db.execute(query_adv).scalars().all()

    mh_prevue = sum(
        float(g.filiere_code and next((a.mh_affectee_globale for a in avancement_list if a.code_groupe == g.code_groupe), 0) or 0)
        for g in groupes
    ) if groupes else 0
    mh_affectee = sum(a.mh_affectee_globale for a in avancement_list)
    mh_realisee = sum(a.mh_realisee_globale for a in avancement_list)
    taux_realisation = (mh_realisee / mh_affectee * 100) if mh_affectee > 0 else 0
    taux_absence = (sum(a.moy_absence for a in avancement_list) / len(avancement_list)) if avancement_list else 0
    nb_efm_fait = len([a for a in avancement_list if a.validation_efm == "oui"])

    return DashboardKPI(
        code_efp=scope_efp,
        nb_groupes=nb_groupes,
        effectif_total=effectif_total,
        nb_formateurs_fp=nb_fp,
        nb_formateurs_fv=nb_fv,
        nb_salles=nb_salles,
        nb_stagiaires_actifs=nb_stagiaires_actifs,
        mh_prevue=round(mh_prevue, 2),
        mh_affectee=round(mh_affectee, 2),
        mh_realisee=round(mh_realisee, 2),
        taux_realisation=round(taux_realisation, 2),
        taux_absence_moyen=round(taux_absence, 2),
        nb_modules_efm_fait=nb_efm_fait,
        nb_modules_total=len(avancement_list),
    )
