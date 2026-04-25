from pydantic import BaseModel, ConfigDict


class GroupeIn(BaseModel):
    code_groupe: str
    code_efp: str
    filiere_code: str | None = None
    annee_formation: int | None = None
    creneau: str | None = None
    mode: str | None = None
    effectif: int = 0
    statut: str | None = None
    fusion_groupe: str | None = None
    code_fusion: str | None = None


class GroupeOut(GroupeIn):
    model_config = ConfigDict(from_attributes=True)


class InscriptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    stagiaire_matricule: str
    code_groupe: str | None = None
    code_efp: str
    code_diplome: str | None = None
    actif: bool
    payant: bool
    principale: bool
    regime: str | None = None
    motif_admission: str | None = None
    date_inscription: str | None = None


class AvancementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code_efp: str
    code_groupe: str
    code_module: str
    formateur_pre_matricule: str | None = None
    formateur_syn_matricule: str | None = None
    mh_affectee_globale: float
    mh_realisee_globale: float
    taux_realisation_global: float
    moy_absence: float
    nb_cc: int
    seance_efm: str | None = None
    validation_efm: str | None = None
    classe_teams: str | None = None
