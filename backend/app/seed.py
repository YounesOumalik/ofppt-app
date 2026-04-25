from sqlalchemy.orm import Session
from sqlalchemy import select

from .config import settings
from .db import Base, engine
from .models import Utilisateur, Role, EFP
from .auth import hash_password


def init_db():
    Base.metadata.create_all(bind=engine)


def seed_admin(db: Session):
    """Créer les EFP et admin par défaut."""
    # Créer les 3 EFP
    efps = [
        EFP(code_efp="TKL0", libelle="INSTITUT SPECIALISE DE TECHNOLOGIE APPLIQUEE KHENIFRA", complexe="Khenifra"),
        EFP(code_efp="TKM0", libelle="INSTITUT SPECIALISE DE TECHNOLOGIE APPLIQUEE 2 KHENIFRA", complexe="Khenifra"),
        EFP(code_efp="TKK0", libelle="CFP KHENIFRA", complexe="Khenifra"),
    ]
    for efp in efps:
        existing = db.execute(select(EFP).where(EFP.code_efp == efp.code_efp)).scalar_one_or_none()
        if not existing:
            db.add(efp)

    # Créer l'admin complexe
    admin_email = settings.ADMIN_EMAIL
    existing_admin = db.execute(select(Utilisateur).where(Utilisateur.email == admin_email)).scalar_one_or_none()
    if not existing_admin:
        admin = Utilisateur(
            email=admin_email,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            nom_complet="Administrateur Complexe Khenifra",
            role=Role.DIRECTEUR_COMPLEXE,
        )
        db.add(admin)

    db.commit()
    print("✅ Base initialisée et admin créé")
