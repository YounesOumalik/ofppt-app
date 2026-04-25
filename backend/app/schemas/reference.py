from pydantic import BaseModel, ConfigDict


class EFPOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code_efp: str
    libelle: str
    complexe: str


class SecteurOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    libelle: str


class FiliereOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code_filiere: str
    libelle: str
    niveau: str | None = None
    type_formation: str | None = None
    secteur_id: int | None = None


class DiplomeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code_diplome: str
    libelle_long: str | None = None
    filiere_code: str | None = None


class ModuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code_module: str
    libelle: str
    regional: bool


class ModuleFiliereOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    filiere_code: str
    code_module: str
    annee_formation: int | None = None
    mh_p_s1: float
    mh_syn_s1: float
    mh_asyn_s1: float
    mh_p_s2: float
    mh_syn_s2: float
    mh_asyn_s2: float


class SalleIn(BaseModel):
    code_efp: str
    nom: str
    type: str | None = None
    capacite: int | None = None
    mhs: float = 60


class SalleOut(SalleIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
