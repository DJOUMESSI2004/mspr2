# Documentation Docker et Docker Compose - Projet MSPR2

## bjectif

Ce document décrit comment nous avons configuré notre projet MSPR2 pour fonctionner avec Docker et Docker Compose. Il inclut les instructions pour construire, lancer et gérer les conteneurs de l'application.

## Structure simplifiée du projet

```
MSPR2/
├── etl/                        # Contient les scripts SQL pour PostgreSQL
├── ml/                         # Contient app.py (FastAPI)
├── frontend/client_mspr/       # Contient l'application front-end (React/Vite)
├── docker-compose.yml          # Fichier central de déploiement
```

## Services conteneurisés

### 1. backend (FastAPI)

* Localisé dans : `ml/`
* Fichier d’entrée : `app.py`
* Port : `8000`
* Dockerfile :

```dockerfile
FROM python:3.10
WORKDIR /ml
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. etl\_db (PostgreSQL avec scripts SQL)

* Localisé dans : `etl/`
* Image officielle : `postgres:16`
* Port : `5432`
* Les fichiers `.sql` sont automatiquement exécutés au démarrage

### 3. frontend (React ou Vite)

* Localisé dans : `frontend/client_mspr/`
* Port : `3000`
* Dockerfile :

```dockerfile
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
EXPOSE 3000
CMD ["npm", "run", "dev"]
```

## docker-compose.yml

Voici la version complète du fichier :

```yaml
version: '3.9'

services:
  backend:
    build:
      context: ./ml
    container_name: backend
    ports:
      - "8000:8000"
    volumes:
      - ./ml:/ml
    working_dir: /ml
    command: ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

  etl_db:
    image: postgres:16
    container_name: etl_db
    environment:
      POSTGRES_DB: etldb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - ./etl:/docker-entrypoint-initdb.d

  frontend:
    build:
      context: ./frontend/client_mspr
    container_name: frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/client_mspr:/app
    working_dir: /app
    command: ["npm", "run", "dev"]
```

## Commandes utiles pour la gestion des conteneurs

### 1. Construire les images

```bash
docker-compose build
```

### 2. Lancer tous les services

```bash
docker-compose up
```

### 3. Arrêter tous les services

```bash
docker-compose down
```

### 4. Accéder aux conteneurs

```bash
docker exec -it backend bash
```

## 💡 Accès aux applications

* API FastAPI : [http://localhost:8000](http://localhost:8000)
* Frontend (React/Vite) : [http://localhost:3000](http://localhost:3000)
* PostgreSQL : port `5432`, utilisateur `user`, mot de passe `password`, base `etldb`

```bash

psql -h localhost -p 5432 -U user -d etldb

note : psql doute être installé sur votre machine pour exécuter cette commande

```
