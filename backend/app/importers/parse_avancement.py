import pandas as pd
from io import BytesIO
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update

from ..models import (
    Avancement, Groupe, Module, Formateur, ModuleFiliere, EFP
)


def parse_avancement_excel(file_content: bytes, code_efp: str, db: Session) -> dict:
    """Parse et import idempotent du fichier avancement Excel."""
    try:
        df = pd.read_excel(BytesIO(file_content), sheet_name="AvancementProgramme" if "AvancementProgramme" in pd.ExcelFile(BytesIO(file_content)).sheet_names else 0)
        df = df.fillna("")

        stats = {"lues": len(df), "inserees": 0, "mises_a_jour": 0, "erreurs": []}

        for idx, row in df.iterrows():
            try:
                groupe_code = str(row.get("Groupe", "")).strip()
                module_code = str(row.get("Code Module", "")).strip()

                if not groupe_code or not module_code:
                    continue

                # Vérifier que le groupe existe
                groupe = db.execute(select(Groupe).where(Groupe.code_groupe == groupe_code)).scalar_one_or_none()
                if not groupe:
                    stats["erreurs"].append(f"Ligne {idx+2}: Groupe {groupe_code} introuvable")
                    continue

                # Vérifier que le module existe
                module = db.execute(select(Module).where(Module.code_module == module_code)).scalar_one_or_none()
                if not module:
                    stats["erreurs"].append(f"Ligne {idx+2}: Module {module_code} introuvable")
                    continue

                formateur_pre = str(row.get("Mle Affecté Présentiel Actif", "")).strip() or None
                mh_p_s1 = float(row.get("MHP S1 DRIF", 0) or 0)
                mh_syn_s1 = float(row.get("MHSYN S1 DRIF", 0) or 0)
                mh_asyn_s1 = float(row.get("MHASYN S1 DRIF", 0) or 0)
                mh_p_s2 = float(row.get("MHP S2 DRIF", 0) or 0)
                mh_syn_s2 = float(row.get("MHSYN S2 DRIF", 0) or 0)
                mh_asyn_s2 = float(row.get("MHASYN S2 DRIF", 0) or 0)

                mh_affectee_p = float(row.get("MH Affectée Présentiel", 0) or 0)
                mh_affectee_syn = float(row.get("MH Affectée Sync", 0) or 0)
                mh_affectee_globale = mh_affectee_p + mh_affectee_syn

                mh_realisee_p = float(row.get("MH Réalisée Présentiel", 0) or 0)
                mh_realisee_syn = float(row.get("MH Réalisée Sync", 0) or 0)
                mh_realisee_globale = mh_realisee_p + mh_realisee_syn

                taux_p = float(row.get("Taux Réalisation Présentiel", 0) or 0)
                taux_syn = float(row.get("Taux Réalisation Syn", 0) or 0)
                taux_global = float(row.get("Taux Réalisation (P & SYN )", 0) or 0)

                moy_absence = float(row.get("Moy Absence", 0) or 0)
                nb_cc = int(row.get("NB CC", 0) or 0)
                seance_efm = str(row.get("Séance EFM", "")).strip() or None
                validation_efm = str(row.get("Validation EFM", "")).strip() or None
                classe_teams = str(row.get("Classe Teams", "")).strip() or None

                # Upsert par (code_groupe, code_module)
                existing = db.execute(
                    select(Avancement).where(
                        (Avancement.code_groupe == groupe_code) &
                        (Avancement.code_module == module_code)
                    )
                ).scalar_one_or_none()

                if existing:
                    existing.formateur_pre_matricule = formateur_pre
                    existing.mh_affectee_p = mh_affectee_p
                    existing.mh_affectee_syn = mh_affectee_syn
                    existing.mh_affectee_globale = mh_affectee_globale
                    existing.mh_realisee_p = mh_realisee_p
                    existing.mh_realisee_syn = mh_realisee_syn
                    existing.mh_realisee_globale = mh_realisee_globale
                    existing.taux_realisation_p = taux_p
                    existing.taux_realisation_syn = taux_syn
                    existing.taux_realisation_global = taux_global
                    existing.moy_absence = moy_absence
                    existing.nb_cc = nb_cc
                    existing.seance_efm = seance_efm
                    existing.validation_efm = validation_efm
                    existing.classe_teams = classe_teams
                    stats["mises_a_jour"] += 1
                else:
                    new_avancement = Avancement(
                        code_efp=code_efp,
                        code_groupe=groupe_code,
                        code_module=module_code,
                        formateur_pre_matricule=formateur_pre,
                        mh_affectee_p=mh_affectee_p,
                        mh_affectee_syn=mh_affectee_syn,
                        mh_affectee_globale=mh_affectee_globale,
                        mh_realisee_p=mh_realisee_p,
                        mh_realisee_syn=mh_realisee_syn,
                        mh_realisee_globale=mh_realisee_globale,
                        taux_realisation_p=taux_p,
                        taux_realisation_syn=taux_syn,
                        taux_realisation_global=taux_global,
                        moy_absence=moy_absence,
                        nb_cc=nb_cc,
                        seance_efm=seance_efm,
                        validation_efm=validation_efm,
                        classe_teams=classe_teams,
                    )
                    db.add(new_avancement)
                    stats["inserees"] += 1
            except Exception as e:
                stats["erreurs"].append(f"Ligne {idx+2}: {str(e)}")

        db.commit()
        return stats
    except Exception as e:
        return {"lues": 0, "inserees": 0, "mises_a_jour": 0, "erreurs": [str(e)]}
