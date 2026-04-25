# 🚀 Déploiement sur Railway (efp.app.ma)

## Architecture Cloud

```
efp.app.ma
├── Frontend (Vercel ou Railway)
├── Backend FastAPI (Railway)
├── PostgreSQL Managé (Railway)
└── HTTPS/TLS Automatique
```

## Prérequis

- Compte GitHub (pour la source)
- Compte Railway.app (gratuit)
- Domaine efp.app.ma enregistré
- Registrar pour les DNS

---

## Étape 1: Créer un repo GitHub

```bash
git init
git add .
git commit -m "Initial commit: OFPPT Management App"
git remote add origin https://github.com/YOUR_USERNAME/ofppt-app.git
git push -u origin main
```

---

## Étape 2: Configurer Railway

### 2.1 Créer un projet Railway

1. Aller à https://railway.app
2. Cliquer **"New Project"**
3. Sélectionner **"Deploy from GitHub"**
4. Connecter votre repo GitHub
5. Autoriser Railway à accéder aux repos

### 2.2 Ajouter PostgreSQL

1. Cliquer **"Add a Service"**
2. Chercher **"PostgreSQL"**
3. Cliquer **"Deploy"**
4. Attendre que la DB soit créée

### 2.3 Configurer le Backend

1. Cliquer **"Add a Service"**
2. Sélectionner **"Deploy from GitHub"**
3. Sélectionner votre repo
4. Configurer:
   - **Root Directory**: `backend/`
   - **Dockerfile**: `Dockerfile`

### 2.4 Ajouter Variables d'Env Backend

Dans Railway, aller à **Variables** et ajouter:

```
DATABASE_URL = ${POSTGRES_URL}
JWT_SECRET = [générer une longue chaîne aléatoire, ex: openssl rand -hex 32]
ADMIN_EMAIL = admin@efp.app.ma
ADMIN_PASSWORD = [mot de passe sécurisé, à changer au 1er login]
CORS_ORIGINS = https://efp.app.ma,https://www.efp.app.ma
```

### 2.5 Configurer le Frontend

1. Cliquer **"Add a Service"**
2. Sélectionner **"Deploy from GitHub"**
3. Sélectionner votre repo
4. Configurer:
   - **Root Directory**: `frontend/`
   - **Build Command**: `npm run build`
   - **Start Command**: `npm run preview`

### 2.6 Ajouter Variables d'Env Frontend

```
VITE_API_URL = https://backend-url-railway.railway.app
```

---

## Étape 3: Configurer le Domaine Personnalisé

### 3.1 Dans Railway

1. Aller à **Frontend Service** → **Settings**
2. Chercher **"Custom Domain"**
3. Entrer: `efp.app.ma`
4. Cliquer **"Add"**
5. Railway affichera les **enregistrements DNS à ajouter**

### 3.2 Configurer DNS chez le Registrar

Chez votre registrar (Maroc Telecom, OVH, etc.):

1. Aller à **Gestion DNS**
2. Ajouter les enregistrements donnés par Railway:
   - **Type**: CNAME ou A record
   - **Valeur**: railway.app DNS
3. Sauvegarder

⏳ **Attendre 24-48h pour la propagation DNS**

---

## Étape 4: Vérifier le Déploiement

### Accès

- **Frontend**: https://efp.app.ma
- **Backend API**: https://backend-xxx.railway.app
- **API Docs**: https://backend-xxx.railway.app/docs

### Test Login

- Email: `admin@efp.app.ma`
- Mot de passe: [celui configuré en Étape 2.4]

---

## Étape 5: Sécurité Post-Déploiement

### Actions urgentes

1. **Changer le mot de passe admin**:
   - Login avec admin@efp.app.ma
   - Aller à `/api/auth/me` pour vérifier
   - Appeler `/api/auth/password-change` avec nouveau MDP

2. **Régénérer JWT_SECRET**:
   ```bash
   openssl rand -hex 32
   # ou
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Mettre à jour dans Railway **Variables**

3. **Ajouter utilisateurs admin**:
   - Inscriptions → Validation admin → Activation
   - Puis assigner rôle `directeur_complexe`

4. **HTTPS automatique**:
   - Railway active Let's Encrypt HTTPS par défaut ✅

5. **Backups PostgreSQL**:
   - Railway offre backups quotidiens automatiques
   - Vérifier dans **PostgreSQL Service** → **Backups**

---

## Flux Utilisateur en Production

1. **Nouvel utilisateur** → `/signup` (inscription)
2. **Status**: `pending_validation` (en attente)
3. **Admin valide** → Dashboard → Admin Users → Valider
4. **User devient** `active` → Peut se connecter
5. **Importe données** → Import Excel
6. **Utilise l'app** → Dashboard, Paramétrage, Consultation

---

## Troubleshooting

### "502 Bad Gateway"

Backend pas prêt:
- Vérifier logs: Railway → Backend Service → Logs
- Vérifier DATABASE_URL correcte
- Vérifier migrations executées

### "Erreur CORS"

Frontend ne parle pas à backend:
- Vérifier CORS_ORIGINS dans Django
- Vérifier VITE_API_URL correct dans frontend

### "Connexion DB impossible"

- Vérifier DATABASE_URL format: `postgresql://user:pass@host:5432/db`
- Vérifier PostgreSQL service actif
- Vérifier variables d'env synchronisées

---

## Coûts Estimés

| Service | Tier | Coût |
|---------|------|------|
| Railway PostgreSQL | Free (5GB) | Gratuit |
| Railway Backend | Hobby | $5/mois |
| Railway Frontend | Hobby | Gratuit/5$/mois |
| Domaine efp.app.ma | .ma | ~200 DH/an (~20 DH/mois) |
| **TOTAL** | | **~$7-10/mois** |

---

## Monitoring

Railway fournit:
- **Logs en temps réel**: Dashboard
- **Metrics**: CPU, Memory, Requests
- **Alertes**: Sur erreurs/downtime
- **Analytics**: Traffic, Response Times

---

## Mise à jour de l'App

```bash
git commit -am "Update feature XYZ"
git push origin main
# Railway redéploie automatiquement!
```

---

## Support

- **Railway Docs**: https://docs.railway.app
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev

---

**✅ Application sécurisée, scalable, et prête pour la production!**
