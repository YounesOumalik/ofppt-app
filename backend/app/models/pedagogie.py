from sqlalchemy import String, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Groupe(Base):
    __tablename__ = "groupe"
    code_groupe: Mapped[str] = mapped_column(String(30), primary_key=True)
    code_efp: Mapped[str] = mapped_column(ForeignKey("efp.code_efp"))
    filiere_code: Mapped[str | None] = mapped_column(ForeignKey("filiere.code_filiere"), nullable=True)
    annee_formation: Mapped[int | None] = mapped_column(Integer, nullable=True)
    creneau: Mapped[str | None] = mapped_column(String(10), nullable=True)  # CDJ | CDS
    mode: Mapped[str | None] = mapped_column(String(20), nullable=True)  # Résidentiel | Alterné
    effectif: Mapped[int] = mapped_column(Integer, default=0)
    statut: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fusion_groupe: Mapped[str | None] = mapped_column(String(255), nullable=True)
    code_fusion: Mapped[str | None] = mapped_column(String(30), nullable=True)


class Inscription(Base):
    __tablename__ = "inscription"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_inscription_session: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)
    stagiaire_matricule: Mapped[str] = mapped_column(ForeignKey("stagiaire.matricule"))
    code_groupe: Mapped[str | None] = mapped_column(ForeignKey("groupe.code_groupe"), nullable=True)
    code_efp: Mapped[str] = mapped_column(ForeignKey("efp.code_efp"))
    code_diplome: Mapped[str | None] = mapped_column(ForeignKey("diplome.code_diplome"), nullable=True)
    actif: Mapped[bool] = mapped_column(default=True)
    payant: Mapped[bool] = mapped_column(default=True)
    principale: Mapped[bool] = mapped_column(default=True)
    regime: Mapped[str | None] = mapped_column(String(50), nullable=True)
    motif_admission: Mapped[str | None] = mapped_column(String(255), nullable=True)
    date_inscription: Mapped[str | None] = mapped_column(String(30), nullable=True)
    date_dossier_complet: Mapped[str | None] = mapped_column(String(30), nullable=True)
    annee_etude: Mapped[str | None] = mapped_column(String(50), nullable=True)


class Avancement(Base):
    __tablename__ = "avancement"
    __table_args__ = (UniqueConstraint("code_groupe", "code_module", name="uq_avancement_groupe_module"),)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code_efp: Mapped[str] = mapped_column(ForeignKey("efp.code_efp"))
    code_groupe: Mapped[str] = mapped_column(ForeignKey("groupe.code_groupe"))
    code_module: Mapped[str] = mapped_column(ForeignKey("module.code_module"))
    formateur_pre_matricule: Mapped[str | None] = mapped_column(ForeignKey("formateur.matricule"), nullable=True)
    formateur_syn_matricule: Mapped[str | None] = mapped_column(String(30), nullable=True)
    mh_affectee_p: Mapped[float] = mapped_column(Float, default=0)
    mh_affectee_syn: Mapped[float] = mapped_column(Float, default=0)
    mh_affectee_globale: Mapped[float] = mapped_column(Float, default=0)
    mh_realisee_p: Mapped[float] = mapped_column(Float, default=0)
    mh_realisee_syn: Mapped[float] = mapped_column(Float, default=0)
    mh_realisee_globale: Mapped[float] = mapped_column(Float, default=0)
    taux_realisation_p: Mapped[float] = mapped_column(Float, default=0)
    taux_realisation_syn: Mapped[float] = mapped_column(Float, default=0)
    taux_realisation_global: Mapped[float] = mapped_column(Float, default=0)
    moy_absence: Mapped[float] = mapped_column(Float, default=0)
    nb_cc: Mapped[int] = mapped_column(Integer, default=0)
    seance_efm: Mapped[str | None] = mapped_column(String(10), nullable=True)
    validation_efm: Mapped[str | None] = mapped_column(String(10), nullable=True)
    classe_teams: Mapped[str | None] = mapped_column(String(10), nullable=True)
    module_pie: Mapped[str | None] = mapped_column(String(10), nullable=True)
    efp_pie: Mapped[str | None] = mapped_column(String(10), nullable=True)
