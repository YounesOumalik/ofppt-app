from pydantic import BaseModel


class ImportResult(BaseModel):
    fichier: str
    type: str
    lignes_lues: int
    lignes_inserees: int
    lignes_mises_a_jour: int
    erreurs: list[dict] = []


class DashboardKPI(BaseModel):
    code_efp: str | None = None
    nb_groupes: int
    effectif_total: int
    nb_formateurs_fp: int
    nb_formateurs_fv: int
    nb_salles: int
    nb_stagiaires_actifs: int
    mh_prevue: float
    mh_affectee: float
    mh_realisee: float
    taux_realisation: float
    taux_absence_moyen: float
    nb_modules_efm_fait: int
    nb_modules_total: int
