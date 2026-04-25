import pandas as pd
from io import BytesIO
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..models import Stagiaire, Inscription, Groupe, Diplome, EFP


def parse_stagiaires_excel(file_content: bytes, code_efp: str, db: Session) -> dict:
    """Parse et import idempotent de la liste stagiaires Excel."""
    try:
        df = pd.read_excel(BytesIO(file_content), sheet_name="Export")
        df = df.fillna("")

        stats = {"lues": len(df), "inserees": 0, "mises_a_jour": 0, "erreurs": []}

        for idx, row in df.iterrows():
            try:
                matricule = str(row.get("MatriculeEtudiant", "")).strip()
                if not matricule:
                    continue

                # Créer ou mettre à jour le stagiaire
                existing_stag = db.execute(select(Stagiaire).where(Stagiaire.matricule == matricule)).scalar_one_or_none()

                if existing_stag:
                    existing_stag.nom = str(row.get("Nom", "")).strip() or None
                    existing_stag.prenom = str(row.get("Prenom", "")).strip() or None
                    existing_stag.nom_ar = str(row.get("Nom_Arabe", "")).strip() or None
                    existing_stag.prenom_ar = str(row.get("Prenom_arabe", "")).strip() or None
                    existing_stag.sexe = str(row.get("Sexe", "")).strip() or None
                    existing_stag.cin = str(row.get("CIN", "")).strip() or None
                    existing_stag.date_naissance = str(row.get("DateNaissance", "")).strip() or None
                    existing_stag.lieu_naissance = str(row.get("LieuNaissance", "")).strip() or None
                    existing_stag.tel = str(row.get("NTelelephone", "")).strip() or None
                    existing_stag.tel_tuteur = str(row.get("NTel_du_Tuteur", "")).strip() or None
                    existing_stag.adresse = str(row.get("Adresse", "")).strip() or None
                    existing_stag.nationalite = str(row.get("Nationalite", "")).strip() or None
                    existing_stag.niveau_scolaire = str(row.get("NiveauScolaire", "")).strip() or None
                    stats["mises_a_jour"] += 1
                else:
                    new_stag = Stagiaire(
                        matricule=matricule,
                        nom=str(row.get("Nom", "")).strip() or None,
                        prenom=str(row.get("Prenom", "")).strip() or None,
                        nom_ar=str(row.get("Nom_Arabe", "")).strip() or None,
                        prenom_ar=str(row.get("Prenom_arabe", "")).strip() or None,
                        sexe=str(row.get("Sexe", "")).strip() or None,
                        cin=str(row.get("CIN", "")).strip() or None,
                        date_naissance=str(row.get("DateNaissance", "")).strip() or None,
                        lieu_naissance=str(row.get("LieuNaissance", "")).strip() or None,
                        tel=str(row.get("NTelelephone", "")).strip() or None,
                        tel_tuteur=str(row.get("NTel_du_Tuteur", "")).strip() or None,
                        adresse=str(row.get("Adresse", "")).strip() or None,
                        nationalite=str(row.get("Nationalite", "")).strip() or None,
                        niveau_scolaire=str(row.get("NiveauScolaire", "")).strip() or None,
                    )
                    db.add(new_stag)
                    stats["inserees"] += 1

                # Créer l'inscription
                id_inscription = row.get("id_inscriptionsessionprogramme")
                code_groupe = str(row.get("Code", "")).strip() or None
                code_diplome = str(row.get("CodeDiplome", "")).strip() or None

                existing_insc = db.execute(
                    select(Inscription).where(Inscription.id_inscription_session == str(id_inscription) if id_inscription else False)
                ).scalar_one_or_none() if id_inscription else None

                if not existing_insc:
                    new_insc = Inscription(
                        id_inscription_session=str(id_inscription) if id_inscription else None,
                        stagiaire_matricule=matricule,
                        code_groupe=code_groupe,
                        code_efp=code_efp,
                        code_diplome=code_diplome,
                        actif=str(row.get("EtudiantActif", "")).lower() == "oui",
                        payant=str(row.get("EtudiantPayant", "")).lower() == "oui",
                        principale=str(row.get("Principale", "")).lower() == "oui",
                        regime=str(row.get("Regimeinscription", "")).strip() or None,
                        motif_admission=str(row.get("MotifAdmission", "")).strip() or None,
                        date_inscription=str(row.get("DateInscription", "")).strip() or None,
                        date_dossier_complet=str(row.get("DateDossierComplet", "")).strip() or None,
                        annee_etude=str(row.get("anneeEtude", "")).strip() or None,
                    )
                    db.add(new_insc)
            except Exception as e:
                stats["erreurs"].append(f"Ligne {idx+2}: {str(e)}")

        db.commit()
        return stats
    except Exception as e:
        return {"lues": 0, "inserees": 0, "mises_a_jour": 0, "erreurs": [str(e)]}
