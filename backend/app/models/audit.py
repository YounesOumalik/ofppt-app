from datetime import datetime
from sqlalchemy import String, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class ImportLog(Base):
    __tablename__ = "import_log"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fichier: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(20))  # avancement | stagiaire
    date_import: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    utilisateur_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lignes_lues: Mapped[int] = mapped_column(Integer, default=0)
    lignes_inserees: Mapped[int] = mapped_column(Integer, default=0)
    lignes_mises_a_jour: Mapped[int] = mapped_column(Integer, default=0)
    erreurs: Mapped[list | None] = mapped_column(JSON, nullable=True)
