#  SoftDesk Support - API RESTful destinée à la gestion de projets

API REST pour la gestion collaborative de projets, issues et commentaires, développée avec Django REST Framework.

---

## Fonctionnalités

- **Gestion des projets** : Création et suivi de projets
- **Système d'issues** : Bugs, tâches et features avec statut et priorité
- **Commentaires** : Discussion sur les issues
- **Permissions granulaires** : Rôles d'auteur, contributeur et authentification via JsonWebToken.

---

## Installation et lancement en Local

### 1. Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.8+** : [Télécharger ici](https://www.python.org/downloads/)
- **Git** : [Télécharger ici](https://git-scm.com/)


Les dépendances Python requises sont :

asgiref==3.8.1,
Django==5.1.7,
djangorestframework==3.15.2,
sqlparse==0.5.3,
tzdata==2025.1,
djangorestframework-simplejwt==4.7.2

### 2. Cloner le projet

Ouvrez un terminal et exécutez :

```sh
git clone https://github.com/Jeremuller/Softdesk.git
```

### 3. Gestion des dépendances avec pipenv

Ce projet utilise pipenv pour la gestion des dépendances et des environnements virtuels.


#### Installation et configuration:

1. Installe pipenv (si ce n'est pas déjà fait) :

```bash
pip install pipenv
```

2. Installe toutes les dépendances (y compris celles de développement) :

```bash
pipenv install --dev
```

3. Active l'environnement virtuel:

```bash
pipenv shell
```

### 4. Commandes essentielles

Avant d’exécuter les migrations, assurez-vous que toutes les migrations nécessaires ont été générées :

```sh
pipenv run python manage.py makemigrations
```

Ensuite, appliquez-les avec:

```sh
pipenv run python manage.py migrate
```

Vous pouvez également créer un super-utilisateur pour accéder à l’administration :

```sh
pipenv run python manage.py createsuperuser
```

Une fois la base de données configurée, vous pouvez démarrer le serveur Django avec la commande suivante :

```sh
pipenv run python manage.py runserver
```

Mettre à jour les dépendances:

```sh
pipenv update
```

Ajouter un package:

```sh
pipenv install <nom_du_package>
```
Cliquez sur le lien pour accéder à l'application.


### 5. Bonnes pratiques

- Toujours travailler dans l'environnement virtuel activé (pipenv shell)
- Utiliser pipenv install pour ajouter des dépendances
- Mettre à jour régulièrement avec pipenv update


### 6. JsonWebToken

#### 1. Obtenir un token

Connexion
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "username": "votre_utilisateur",
  "password": "votre_mot_de_passe"
}
```

Réponse
```bash
{
  "access": "votre_token_jwt",
  "refresh": "votre_token_rafraîchissement"
}
```

#### 2. Utiliser le token

Ajoutez l'en-tête à toutes vos requêtes:
```bash
Authorization: Bearer votre_token_jwt
```

#### 3. Rafraîchir le token

```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "votre_token_rafraîchissement"
}
```

#### 4. Informations complémentaires

- Durée de validité : 5 min (access) / 24h (refresh)
- Toujours utiliser HTTPS
- Ne jamais exposer le token

## Fonctionnement de l'API:

### Endpoints

#### Authentification
- `POST /api/auth/register/` - Inscription d'un nouvel utilisateur
- `POST /api/auth/login/` - Connexion et obtention d'un token JWT

#### Projets
- `GET /api/projects/` - Liste tous les projets accessibles
- `POST /api/projects/` - Crée un nouveau projet
- `GET /api/projects/{id}/` - Détails d'un projet spécifique
- `PUT /api/projects/{id}/` - Met à jour un projet
- `DELETE /api/projects/{id}/` - Supprime un projet

#### Issues
- `GET /api/projects/{project_id}/issues/` - Liste les issues d'un projet
- `POST /api/projects/{project_id}/issues/` - Crée une nouvelle issue
- `GET /api/projects/{project_id}/issues/{id}/` - Détails d'une issue
- `PUT /api/projects/{project_id}/issues/{id}/` - Met à jour une issue
- `DELETE /api/projects/{project_id}/issues/{id}/` - Supprime une issue
- `POST /api/projects/{project_id}/issues/{id}/assign/` - Assigne une issue à un contributeur

#### Commentaires
- `GET /api/projects/{project_id}/issues/{issue_id}/comments/` - Liste les commentaires d'une issue
- `POST /api/projects/{project_id}/issues/{issue_id}/comments/` - Ajoute un commentaire
- `GET /api/projects/{project_id}/issues/{issue_id}/comments/{id}/` - Détails d'un commentaire
- `PUT /api/projects/{project_id}/issues/{issue_id}/comments/{id}/` - Met à jour un commentaire
- `DELETE /api/projects/{project_id}/issues/{issue_id}/comments/{id}/` - Supprime un commentaire

### Permissions

#### Rôles
- **Author** : Créateur du projet (pleins droits)
- **Contributor** : Contributeur au projet (droits limités)
- **Authenticated User** : Utilisateur connecté (accès restreint)

#### Tableau des permissions
 |   Ressource                          | GET         | POST | PUT | DELETE |
 |--------------------------------------|-------------|------|-----|--------|
 | /projects/                           | Contributor | Auth | Author | Author |
 | /projects/{id}/                      | Contributor | - | Author | Author |
 | /issues/               | Contributor | Contributor | Author | Author |
 | /issues/{id}/          | Contributor | - | Author | Author |
 | /projects/{id}/issues/{id}/assign/   | Contributor | Author | - | - |
 | /comments/ | Contributor | Contributor | Author | Author |

### Exemples de requêtes

Créer un projet
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Mon projet", "description": "Description du projet"}'
```

### Modèles de données

#### Project
- title (CharField)
- description (TextField)
- author (ForeignKey to User)
- created_at (DateTimeField)

#### Issue
- title (CharField)
- description (TextField)
- project (ForeignKey to Project)
- status (ChoiceField: TODO, IN_PROGRESS, DONE)
- priority (ChoiceField: LOW, MEDIUM, HIGH)
- tag (ChoiceField: BUG, TASK, FEATURE)
- assigned_to (ForeignKey to User)
- author (ForeignKey to User)
- created_at (DateTimeField)

#### Comment
- content (TextField)
- issue (ForeignKey to Issue)
- author (ForeignKey to User)
- created_at (DateTimeField)


