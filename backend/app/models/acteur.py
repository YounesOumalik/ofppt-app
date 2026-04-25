from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Role(str, PyEnum):
    DIRECTEUR_COMPLEXE = "directeur_complexe"
    DIRECTEUR_ETABLISSEMENT = "directeur_etablissement"
    GESTIONNAIRE_STAGIAIRES = "gestionnaire_stagiaires"
    FORMATEUR = "formateur"
    STAGIAIRE = "stagiaire"


class UserStatus(str, PyEnum):
    PENDING_VALIDATION = "pending_validation"
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"


class Formateur(Base):
    __tablename__ = "formateur"
    matricule: Mapped[str] = mapped_column(String(30), primary_key=True)
    nom_complet: Mapped[str] = mapped_column(String(255))
    type: Mapped[str | None] = mapped_column(String(5), nullable=True)  # FP | FV
    code_efp: Mapped[str | None] = mapped_column(ForeignKey("efp.code_efp"), nullable=True)
    metier: Mapped[str | None] = mapped_column(String(150), nullable=True)


class Stagiaire(Base):
    __tablename__ = "stagiaire"
    matricule: Mapped[str] = mapped_column(String(30), primary_key=True)
    nom: Mapped[str | None] = mapped_column(String(150), nullable=True)
    prenom: Mapped[str | None] = mapped_column(String(150), nullable=True)
    nom_ar: Mapped[str | None] = mapped_column(String(150), nullable=True)
    prenom_ar: Mapped[str | None] = mapped_column(String(150), nullable=True)
    sexe: Mapped[str | None] = mapped_column(String(2), nullable=True)
    cin: Mapped[str | None] = mapped_column(String(30), nullable=True)
    date_naissance: Mapped[str | None] = mapped_column(String(30), nullable=True)
    lieu_naissance: Mapped[str | None] = mapped_column(String(150), nullable=True)
    tel: Mapped[str | None] = mapped_column(String(30), nullable=True)
    tel_tuteur: Mapped[str | None] = mapped_column(String(30), nullable=True)
    adresse: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nationalite: Mapped[str | None] = mapped_column(String(50), nullable=True)
    niveau_scolaire: Mapped[str | None] = mapped_column(String(255), nullable=True)


class Utilisateur(Base):
    __tablename__ = "utilisateur"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    nom_complet: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum(Role))
    statut: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.PENDING_VALIDATION)
    code_efp: Mapped[str | None] = mapped_column(ForeignKey("efp.code_efp"), nullable=True)
    actif: Mapped[bool] = mapped_column(Boolean, default=True)
    formateur_matricule: Mapped[str | None] = mapped_column(ForeignKey("formateur.matricule"), nullable=True)
    stagiaire_matricule: Mapped[str | None] = mapped_column(ForeignKey("stagiaire.matricule"), nullable=True)
    cree_le: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    dernier_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    valide_par: Mapped[int | None] = mapped_column(ForeignKey("utilisateur.id"), nullable=True)
    date_validation: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
