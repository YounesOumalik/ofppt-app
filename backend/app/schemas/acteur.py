from pydantic import BaseModel, ConfigDict


class FormateurIn(BaseModel):
    matricule: str
    nom_complet: str
    type: str | None = None
    code_efp: str | None = None
    metier: str | None = None


class FormateurOut(FormateurIn):
    model_config = ConfigDict(from_attributes=True)


class StagiaireOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    matricule: str
    nom: str | None = None
    prenom: str | None = None
    nom_ar: str | None = None
    prenom_ar: str | None = None
    sexe: str | None = None
    cin: str | None = None
    date_naissance: str | None = None
    lieu_naissance: str | None = None
    tel: str | None = None
    tel_tuteur: str | None = None
    adresse: str | None = None
    nationalite: str | None = None
    niveau_scolaire: str | None = None
