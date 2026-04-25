from sqlalchemy import String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class EFP(Base):
    __tablename__ = "efp"
    code_efp: Mapped[str] = mapped_column(String(10), primary_key=True)
    libelle: Mapped[str] = mapped_column(String(255))
    complexe: Mapped[str] = mapped_column(String(100), default="Khenifra")


class Secteur(Base):
    __tablename__ = "secteur"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    libelle: Mapped[str] = mapped_column(String(150), unique=True)


class Filiere(Base):
    __tablename__ = "filiere"
    code_filiere: Mapped[str] = mapped_column(String(50), primary_key=True)
    libelle: Mapped[str] = mapped_column(String(255))
    niveau: Mapped[str | None] = mapped_column(String(10), nullable=True)
    secteur_id: Mapped[int | None] = mapped_column(ForeignKey("secteur.id"), nullable=True)
    type_formation: Mapped[str | None] = mapped_column(String(50), nullable=True)
    secteur: Mapped["Secteur | None"] = relationship()


class Diplome(Base):
    __tablename__ = "diplome"
    code_diplome: Mapped[str] = mapped_column(String(50), primary_key=True)
    libelle_long: Mapped[str | None] = mapped_column(String(255), nullable=True)
    filiere_code: Mapped[str | None] = mapped_column(ForeignKey("filiere.code_filiere"), nullable=True)


class Module(Base):
    __tablename__ = "module"
    code_module: Mapped[str] = mapped_column(String(30), primary_key=True)
    libelle: Mapped[str] = mapped_column(String(255))
    regional: Mapped[bool] = mapped_column(Boolean, default=False)


class ModuleFiliere(Base):
    __tablename__ = "module_filiere"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filiere_code: Mapped[str] = mapped_column(ForeignKey("filiere.code_filiere"))
    code_module: Mapped[str] = mapped_column(ForeignKey("module.code_module"))
    annee_formation: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mh_p_s1: Mapped[float] = mapped_column(Float, default=0)
    mh_syn_s1: Mapped[float] = mapped_column(Float, default=0)
    mh_asyn_s1: Mapped[float] = mapped_column(Float, default=0)
    mh_p_s2: Mapped[float] = mapped_column(Float, default=0)
    mh_syn_s2: Mapped[float] = mapped_column(Float, default=0)
    mh_asyn_s2: Mapped[float] = mapped_column(Float, default=0)


class Salle(Base):
    __tablename__ = "salle"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code_efp: Mapped[str] = mapped_column(ForeignKey("efp.code_efp"))
    nom: Mapped[str] = mapped_column(String(150))
    type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # Salle, Atelier, Labo
    capacite: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mhs: Mapped[float] = mapped_column(Float, default=60)  # Masse horaire semaine dispo
