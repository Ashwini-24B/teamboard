TeamBoard – B2B Knowledge Base API Platform
Overview

TeamBoard is a Django REST Framework-based B2B Knowledge Base API platform. It provides authenticated knowledge-base management, search functionality, query logging, and admin usage analytics.

Tech Stack
Python 3.14
Django 6.1
Django REST Framework
PostgreSQL 16
Docker Compose
JWT Authentication
Simple JWT
Features
User registration and JWT authentication
Knowledge-base entry creation, retrieval, updating, and deletion
Search knowledge-base questions and answers
Query logging with result counts and company association
Admin-only usage summary and company-level analytics
PostgreSQL database running through Docker Compose
Project Structure
teamboard/
├── api/
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── views.py
│   └── urls.py
├── knowledge/
├── teamboard/
│   ├── settings.py
│   └── urls.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
Prerequisites
Python 3.14 or compatible version
Docker Desktop with Docker Compose
Git
Setup Instructions
1. Clone the repository
git clone <your-repository-url>
cd teamboard
2. Create and activate a virtual environment
python -m venv venv

Windows PowerShell:

.\venv\Scripts\Activate.ps1

If activation is restricted, use the environment's Python executable directly:

.\venv\Scripts\python.exe
3. Install dependencies
pip install -r requirements.txt
### 4. Configure environment variables

Create a `.env` file in the project root by copying `.env.example`.

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

Open the `.env` file and replace the placeholder values with your own database credentials and a securely generated Django secret key.

The following environment variables are required:

- `DJANGO_SECRET_KEY`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

**Security:** Never commit your `.env` file or share your actual credentials. The `.env.example` file contains placeholders only.

### 5. Start PostgreSQL

Start the PostgreSQL database using Docker Compose:

```powershell
docker compose up -d
```

### 6. Apply database migrations

```powershell
python manage.py migrate
```

### 7. Start the development server

```powershell
python manage.py runserver
```

The API will be available at:
http://127.0.0.1:8000/

API Endpoints
Method	Endpoint	Description
POST	/api/auth/register/	Register a user
POST	/api/token/	Obtain JWT access and refresh tokens
POST	/api/token/refresh/	Refresh an access token
GET	/api/knowledge/	List knowledge-base entries
POST	/api/knowledge/	Create a knowledge-base entry
GET	/api/knowledge/<id>/	Retrieve an entry
PATCH	/api/knowledge/<id>/	Update an entry
DELETE	/api/knowledge/<id>/	Delete an entry
POST	/api/kb/query/	Search the knowledge base
GET	/api/admin/usage-summary/	Retrieve admin usage analytics

Protected endpoints require a JWT access token in the request's Authorization header:

Authorization: Bearer <access_token>
Knowledge Base Search

Send a POST request to /api/kb/query/ with a JSON body:

{
  "search": "database"
}

The response includes the search term, matching result count, and matching knowledge-base entries. Each search is logged with its result count and associated company.

An empty search term returns a 400 Bad Request response.

Admin Usage Summary

The admin usage summary endpoint provides:

Total number of logged queries
Total number of results returned across queries
Query and result counts grouped by company

Access is restricted to authenticated users with the admin role.

Testing

Run Django's system checks:

python manage.py check

Run the automated test suite:

python manage.py test

API endpoints can also be tested using Postman or PowerShell.

Security Notes
Keep .env out of version control.
Use secure, unique passwords and secret keys.
Do not share JWT tokens or database credentials.
Configure production security settings before deployment.
License

Add the applicable license or assignment-specific terms here.
