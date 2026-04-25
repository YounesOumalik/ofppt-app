# 🎓 OFPPT Management - Gestion Centre de Formation

Application web complète et sécurisée pour la gestion d'un centre de formation OFPPT, déployée sur **efp.app.ma**.

## 🌐 Accès Production

**URL**: https://efp.app.ma  
**Status**: ✅ Sécurisé - HTTPS/TLS - PostgreSQL Managé - Multi-tenant

---

## 📋 Table des Matières

- [Architecture](#architecture)
- [Démarrage Local](#démarrage-local)
- [Déploiement Cloud](#déploiement-cloud)
- [Workflow Utilisateur](#workflow-utilisateur)
- [Sécurité](#sécurité)
- [Roadmap](#roadmap)

---

## 🏗️ Architecture

```
efp.app.ma
├── Frontend (React 18 + Vite + Tailwind)
├── Backend (FastAPI + SQLAlchemy)
├── PostgreSQL Managé (Railway)
└── HTTPS/TLS Automatique (Let's Encrypt)
```

### Stack

| Couche | Technologie |
|--------|-------------|
| **Frontend** | React 18, Vite, TypeScript, Tailwind CSS, PWA |
| **Backend** | FastAPI, SQLAlchemy, Pydantic |
| **BDD** | PostgreSQL 15 (production), SQLite (dev) |
| **Auth** | JWT + RBAC (5 rôles) |
| **Déploiement** | Railway + Domaine Custom |
| **CI/CD** | Auto-déploiement GitHub |

---

## 🚀 Démarrage Local (Développement)

### 1. Cloner et Configurer

```bash
git clone https://github.com/YOUR_REPO/ofppt-app.git
cd ofppt-app
cp backend/.env.example backend/.env
```

### 2. Démarrer avec Docker Compose

```bash
docker-compose up
```

Services lancés automatiquement:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **API Docs**: http://localhost:8000/docs

### 3. Login par défaut

- Email: `admin@efp.app.ma`
- Mot de passe: `Admin@2026`

---

## ☁️ Déploiement Cloud sur Railway

**👉 Lire le guide complet**: [DEPLOY.md](./DEPLOY.md)

**Résumé rapide:**

1. Créer repo GitHub
2. Connecter à Railway.app
3. Configurer PostgreSQL
4. Ajouter domaine efp.app.ma
5. Variables d'env sécurisées
6. Deploy automatique via git push!

**Coût estimé**: ~$7-10/mois (PostgreSQL + Backend + Domaine)

---

## 👥 Workflow Utilisateur

```
┌─ Nouvel Utilisateur
├─ S'inscrire (/signup)
├─ Statut: PENDING_VALIDATION ⏳
├─ Admin valide le compte
├─ Statut: ACTIVE ✅
├─ Login possible
├─ Importe Excel (avancement + stagiaires)
├─ Utilise l'app (Dashboard, Paramétrage, etc.)
└─ Crée/Édite les données
```

**Rôles & Permissions:**

| Rôle | Inscription | Validation | Import | Paramétrage | Admin | Dashboard |
|------|:-----------:|:----------:|:------:|:-----------:|:-----:|:---------:|
| 👑 Directeur Complexe | ✅ | ✅ | ✅ tous | ✅ tous | ✅ | ✅ global |
| 🏢 Directeur Établissement | ✅ | ❌ | ✅ son EFP | ✅ son EFP | ✅ son | ✅ son |
| 📋 Gestionnaire Stagiaires | ✅ | ❌ | ❌ | ❌ | ❌ | Limité |
| 👨‍🏫 Formateur | ✅ | ❌ | ❌ | ❌ | ❌ | Ses données |
| 🎓 Stagiaire | ✅ | ❌ | ❌ | ❌ | ❌ | Lecture seule |

---

## 🔐 Sécurité

### 1. Authentification

- ✅ JWT + Refresh Tokens
- ✅ Password Hashing (Bcrypt)
- ✅ HTTPS/TLS (Let's Encrypt)
- ✅ Session Timeout (8 heures)

### 2. Autorisation (RBAC)

- ✅ 5 Rôles avec permissions granulaires
- ✅ Filtrage automatique données par établissement
- ✅ Multi-tenant strict

### 3. Validation des Comptes

- ✅ Inscription nécessite validation admin
- ✅ Email unique
- ✅ Statuts: PENDING_VALIDATION → ACTIVE → INACTIVE

### 4. Données

- ✅ PostgreSQL managé (backups quotidiens)
- ✅ Audit logs (import, validations, logins)
- ✅ Isolation par établissement/utilisateur
- ✅ Chiffrement données sensibles (optionnel)

### 5. API

- ✅ Rate Limiting (TODO)
- ✅ CORS Sécurisé (domaines whitelist)
- ✅ Input Validation (Pydantic)
- ✅ SQL Injection Protection (SQLAlchemy ORM)

---

## 📊 Modules Implémentés (Sprint 1)

✅ **Auth & Sécurité**
- Login/Signup/Logout
- Validation admin des comptes
- JWT + RBAC 5 rôles
- Password Reset (TODO)

✅ **Admin**
- Gestion des utilisateurs
- Validation des nouveaux comptes
- Attribution des rôles/établissements

✅ **Import Excel**
- Avancement de formation (idempotent)
- Stagiaires (idempotent)
- Audit logs import

✅ **Paramétrage**
- CRUD Salles
- CRUD Groupes
- CRUD Formateurs
- CRUD Modules
- CRUD Filières

✅ **Consultation**
- Lister Stagiaires (recherche)
- Lister Groupes
- Lister Formateurs
- Lister Modules
- Lister Avancement

✅ **Dashboard Direction**
- KPI: Groupes, Effectifs, Formateurs
- Donuts: MH Prévue/Affectée/Réalisée
- Taux Réalisation, Absences, EFM
- Filtres par EFP/Année/Filière

---

## 🛠️ Sprint 2 (Prochainement)

📅 **Module EDT Complet**
- Grille jour×heure (lundi-samedi, 08:30-18:30)
- Drag & drop séances
- Assignation formateur + local + groupe
- Prise en compte avancement (MH restantes)
- Détection conflits
- Suggestion auto-planification

---

## 📁 Structure du Projet

```
Application/
├── backend/
│   ├── app/
│   │   ├── models/          # ORM SQLAlchemy
│   │   ├── schemas/         # Pydantic
│   │   ├── routers/         # Routes FastAPI
│   │   ├── importers/       # Parsers Excel
│   │   ├── auth.py          # JWT + RBAC
│   │   ├── config.py        # Settings
│   │   ├── db.py            # Database
│   │   ├── main.py          # FastAPI app
│   │   └── seed.py          # Seed données
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── railway.json
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/             # Client HTTP
│   │   ├── auth/            # AuthContext
│   │   ├── components/      # Composants React
│   │   ├── pages/           # Pages
│   │   └── App.tsx
│   ├── package.json
│   ├── Dockerfile
│   └── vite.config.ts
├── docker-compose.yml       # Dev: Frontend + Backend + DB
├── DEPLOY.md                # Guide déploiement Railway
└── README.md                # Ce fichier
```

---

## 🌐 Endpoints API

### Auth
- `POST /api/auth/signup` — Inscription (nouvel utilisateur)
- `POST /api/auth/login` — Connexion
- `GET /api/auth/me` — Profil utilisateur courant
- `POST /api/auth/password-change` — Changer mot de passe

### Admin
- `GET /api/admin/users` — Lister utilisateurs
- `GET /api/admin/users/pending` — Lister en attente validation
- `POST /api/admin/users/{id}/validate` — Valider un compte
- `POST /api/admin/users/{id}/reject` — Rejeter un compte
- `PUT /api/admin/users/{id}` — Modifier utilisateur
- `DELETE /api/admin/users/{id}` — Désactiver utilisateur

### Import
- `POST /api/import/avancement` — Importer fichier avancement
- `POST /api/import/stagiaires` — Importer fichier stagiaires

### Paramétrage
- `GET/POST /api/parametrage/salles` — Gestion salles
- `GET/POST /api/parametrage/groupes` — Gestion groupes
- `GET/POST /api/parametrage/formateurs` — Gestion formateurs

### Consultation & Dashboard
- `GET /api/data/stagiaires` — Lister stagiaires
- `GET /api/data/groupes` — Lister groupes
- `GET /api/dashboard/kpi` — KPI direction

**Swagger complet**: https://efp.app.ma/docs (production)

---

## 💾 Variables d'Environnement

### Development (`.env`)
```
DATABASE_URL=sqlite:///./data/app.db
JWT_SECRET=dev-secret-key
ADMIN_EMAIL=admin@efp.app.ma
ADMIN_PASSWORD=Admin@2026
CORS_ORIGINS=http://localhost:5173
```

### Production (Railway)
```
DATABASE_URL=postgresql://user:pass@host:5432/db
JWT_SECRET=[générer: openssl rand -hex 32]
ADMIN_EMAIL=admin@efp.app.ma
ADMIN_PASSWORD=[sécurisé, à changer!]
CORS_ORIGINS=https://efp.app.ma,https://www.efp.app.ma
```

---

## 📝 Roadmap

### ✅ Sprint 1 (Fait)
- Scaffolding Backend + Frontend
- Auth JWT + RBAC 5 rôles
- Admin: Gestion comptes + Validation
- Import Excel idempotent
- Paramétrage (CRUD)
- Dashboard KPI
- Consultation données
- Multi-tenant strict

### 📅 Sprint 2
- Module EDT complet
- Grille jour×heure
- Drag & drop séances
- Prise en compte avancement
- Détection conflits

### 🔮 Sprint 3+
- Candidatures en ligne
- Finance (Paiements, Comptabilité)
- GED (Gestion documents)
- RH (Carrière, KPI formateurs)
- Qualité (Tableau de bord)
- Après-formation (Insertion, Partenariats)

---

## 🐛 Troubleshooting

### "CORS Error"
```
Frontend ne parle pas à l'API.
→ Vérifier CORS_ORIGINS en production
→ Vérifier VITE_API_URL en frontend
```

### "502 Bad Gateway"
```
Backend pas prêt.
→ Vérifier logs Railway: Backend Service → Logs
→ Vérifier DATABASE_URL
→ Vérifier migration DB
```

### "Erreur Import Excel"
```
Colonnes Excel ne matchent pas.
→ Vérifier noms en-tête Excel
→ Modifier parsers si besoin (backend/app/importers/)
```

---

## 📞 Support

- **Documentation**: Lire DEPLOY.md, README.md
- **API Docs**: https://efp.app.ma/docs (Swagger)
- **Issues**: GitHub Issues
- **Contact**: admin@efp.app.ma

---

## 📄 License

MIT License - Libre d'usage

---

**Merci d'utiliser OFPPT Management! 🎓**
