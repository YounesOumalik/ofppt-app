# ⚡ Guide de Démarrage Rapide - efp.app.ma

Déployez votre application OFPPT en 15 minutes sur Railway avec domaine personnalisé.

---

## 📋 Prérequis (5 min)

- [ ] **GitHub Account** (https://github.com - créer un compte gratuit si besoin)
- [ ] **Railway Account** (https://railway.app - se connecter avec GitHub)
- [ ] **Domaine efp.app.ma** (déjà enregistré? Vérifier l'accès)
- [ ] **Registrar DNS** (où vous avez enregistré le domaine)

---

## 🚀 Étape 1: Créer le Repo GitHub (2 min)

### 1.1 Initialiser Git localement

```bash
cd Application
git init
git config user.email "you@example.com"
git config user.name "Your Name"
git add .
git commit -m "feat: Initial OFPPT Management application"
```

### 1.2 Créer le repo sur GitHub

1. Aller à https://github.com/new
2. **Repository name**: `ofppt-app`
3. **Description**: "OFPPT Center Management System"
4. **Visibility**: Private (sécurité)
5. Cliquer **"Create repository"**

### 1.3 Pousser le code

```bash
git remote add origin https://github.com/YOUR_USERNAME/ofppt-app.git
git branch -M main
git push -u origin main
```

✅ **Code sur GitHub!**

---

## ☁️ Étape 2: Déployer sur Railway (5 min)

### 2.1 Créer le Projet Railway

1. Aller à https://railway.app
2. Cliquer **"New Project"** (en haut à droite)
3. Sélectionner **"Deploy from GitHub"**
4. Cliquer **"Connect GitHub"**
5. Autoriser Railway à accéder à vos repos
6. Sélectionner **`ofppt-app`**
7. Cliquer **"Deploy"**

### 2.2 Ajouter PostgreSQL

Railway vous demande d'ajouter un service:

1. Cliquer **"Add a Service"**
2. Chercher **"PostgreSQL"**
3. Cliquer **"PostgreSQL"** → **"Deploy"**
4. Attendre ~1 min (DB créée)

### 2.3 Configurer le Backend

1. Cliquer **"New Service"** → **"From GitHub"**
2. Sélectionner **`ofppt-app`** repo
3. **Settings**:
   - **Root Directory**: `backend`
   - **Framework**: `Python`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. Cliquer **"Deploy"**

### 2.4 Ajouter Variables d'Env Backend

Après que le backend se déploie:

1. Cliquer sur le **Service Backend**
2. Aller à **"Variables"**
3. Ajouter:

```
DATABASE_URL = ${{ POSTGRES_URL }}
JWT_SECRET = openssl_rand_hex_32_here
ADMIN_EMAIL = admin@efp.app.ma
ADMIN_PASSWORD = ChangeMe@2026
CORS_ORIGINS = https://efp.app.ma,https://www.efp.app.ma
```

Pour `JWT_SECRET`, générer une clé:
```bash
# Windows PowerShell
$bytes = New-Object byte[] 32; (New-Object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes); ([System.BitConverter]::ToString($bytes) -replace '-','').ToLower()

# macOS/Linux
openssl rand -hex 32
```

4. Cliquer **"Deploy"** pour appliquer

### 2.5 Ajouter le Frontend

1. Cliquer **"New Service"** → **"From GitHub"**
2. Sélectionner **`ofppt-app`** repo
3. **Settings**:
   - **Root Directory**: `frontend`
   - **Framework**: `Node.js`
   - **Build Command**: `npm run build`
   - **Start Command**: `npm run preview`

4. Ajouter Variable:
   - **VITE_API_URL**: `https://BACKEND-SERVICE.railway.app` (remplacer par l'URL réelle du backend)

5. Cliquer **"Deploy"**

✅ **Les deux services sont déployés!**

---

## 🌐 Étape 3: Configurer le Domaine efp.app.ma (5 min)

### 3.1 Obtenir les Enregistrements DNS

1. Dans Railway, cliquer sur le **Service Frontend**
2. Aller à **"Settings"** → **"Domains"**
3. Cliquer **"Add Domain"**
4. Entrer: `efp.app.ma`
5. Cliquer **"Add"**
6. Railway affiche les **enregistrements DNS**. Copier:
   - Type (CNAME ou A)
   - Valeur (railway.app hostname)
   - TTL

### 3.2 Ajouter les Enregistrements DNS

Chez votre registrar (OVH, Maroc Telecom, 1&1, etc.):

1. Se connecter au compte registrar
2. Chercher **"DNS"** ou **"Gestion des enregistrements"**
3. Ajouter un nouvel enregistrement:
   - **Type**: CNAME (ou A si spécifié)
   - **Domaine**: `efp.app.ma`
   - **Valeur**: `xxxx.railway.app` (copié de Railway)
   - **TTL**: 3600
4. Sauvegarder

⏳ **Attendre 1-24h pour la propagation DNS**

### 3.3 Vérifier le Domaine

```bash
nslookup efp.app.ma
# ou
ping efp.app.ma
```

Une fois résolu, Railway active automatiquement HTTPS (Let's Encrypt).

---

## ✅ Étape 4: Vérifier le Déploiement

### 4.1 Accéder à l'Application

Après propagation DNS (~1h):

1. Ouvrir https://efp.app.ma
2. Vous devriez voir la **page de login**

### 4.2 Se Connecter

- **Email**: `admin@efp.app.ma`
- **Mot de passe**: `ChangeMe@2026`
- Cliquer **"Se connecter"**

### 4.3 Vérifier les Services

- **Frontend**: https://efp.app.ma
- **API Docs**: https://efp.app.ma/api/docs ❌ (pas exposé)
- **Backend URL**: Aller dans Railway pour voir `https://backend-xxxx.railway.app/docs`

✅ **L'application est en ligne!**

---

## 🔒 Étape 5: Sécurité (Important!)

### 5.1 Changer le Mot de Passe Admin

1. Login: admin@efp.app.ma / ChangeMe@2026
2. Aller à **Settings** (gear icon)
3. Changer le mot de passe
4. **NE JAMAIS laisser le mot de passe par défaut!**

### 5.2 Ajouter d'Autres Admins

1. Aller à **Admin** → **Utilisateurs**
2. Cliquer **"Nouveau Compte"**
3. Rôle: `Directeur Complexe` (ou autre)
4. Statut: En attente
5. Admin valide le compte
6. Utilisateur peut se connecter

### 5.3 Vérifier HTTPS

- Tous les accès doivent être en **`https://`** (pas http://)
- Railway active Let's Encrypt automatiquement ✅

---

## 📊 Workflow Utilisateur Production

1. **Nouvel utilisateur** → Clique "S'inscrire"
2. **Remplit le formulaire** (email, nom, mot de passe, établissement)
3. **Attend validation** admin (statut: `PENDING_VALIDATION`)
4. **Admin valide** depuis le Dashboard → Admin Users → "Valider"
5. **Utilisateur reçoit notification** (optionnel)
6. **Peut se connecter** (statut: `ACTIVE`)
7. **Importe ses fichiers Excel**
8. **Utilise l'application** (Dashboard, Paramétrage, etc.)

---

## 🐛 Troubleshooting Rapide

| Problème | Solution |
|----------|----------|
| **"502 Bad Gateway"** | Backend pas prêt. Vérifier logs Railway. Attendre 2-3 min. |
| **"Cannot reach efp.app.ma"** | DNS pas propagé. Attendre 24h. Vérifier `nslookup efp.app.ma`. |
| **"CORS Error"** | Vérifier `CORS_ORIGINS` en variables d'env. Include `https://efp.app.ma`. |
| **Import Excel échoue** | Vérifier colonnes Excel matchent les parsers. Logs: Railway Backend → Logs. |
| **Login impossible** | Statut utilisateur: `PENDING_VALIDATION`? Admin doit valider le compte. |

---

## 📱 Test sur Mobile

Puisque c'est une **PWA** (Progressive Web App):

1. Ouvrir https://efp.app.ma sur téléphone
2. Cliquer **"Share"** → **"Add to Home Screen"** (iOS)
3. Ou cliquer les 3 points → **"Install app"** (Android/Chrome)
4. L'app s'ajoute comme une app native!

---

## 💰 Coûts Mensuels

| Service | Tarif |
|---------|-------|
| Railway Backend (Hobby Plan) | $5/mois |
| Railway PostgreSQL (Free 5GB) | Gratuit |
| Railway Frontend | Gratuit |
| Domaine efp.app.ma | ~200 DH/an (~17 DH/mois) |
| **TOTAL** | **~$6-7/mois** |

Facture disponible dans **Railway Dashboard** → **Billing**.

---

## 📖 Docs Complètes

- **DEPLOY.md** - Guide détaillé déploiement
- **README.md** - Architecture, API, roadmap
- **Swagger API**: https://backend-xxxx.railway.app/docs

---

## 🎉 Félicitations!

Votre application **OFPPT Management** est maintenant **en ligne et sécurisée** sur **efp.app.ma**!

### Prochaines Étapes

1. ✅ Inviter d'autres admins
2. ✅ Charger les fichiers Excel
3. ✅ Créer les comptes utilisateurs
4. ✅ Sprint 2: Implémenter l'EDT

---

## 📞 Support

- **Problèmes Railway?** → https://docs.railway.app
- **Erreurs API?** → Vérifier Swagger: `https://backend-xxxx.railway.app/docs`
- **Questions?** → admin@efp.app.ma

---

**Bon courage avec votre gestion de centre de formation! 🎓**
