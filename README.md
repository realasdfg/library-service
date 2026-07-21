# Library Service API

A REST API for managing a library catalogue and book borrowings. It provides JWT-based authentication, public access to
browse books, administrator-only catalogue management, and user-scoped borrowing records.

## Features

- Register users and authenticate with JSON Web Tokens (JWT).
- Browse the book catalogue without an account.
- Create, update, and delete books as an administrator.
- Create borrowings for the authenticated user while safely reducing available inventory.
- View active or historical borrowings; regular users see only their own records, while administrators can view all
  records.
- Explore the API interactively through Swagger UI.

## Tech stack

- Python 3.13
- Django 6
- Django REST Framework
- Simple JWT
- drf-spectacular / Swagger UI
- SQLite (default development database)

## Quick start with Docker

1. Create your environment file:

   ```powershell
   Copy-Item .env.template .env
   ```

2. Set the PostgreSQL variables in `.env`. For the included Compose setup, use:

   ```env
   SECRET_KEY=your-key
   DEBUG=True
   POSTGRES_DB=library
   POSTGRES_USER=library_user
   POSTGRES_PASSWORD=change-me
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   PGDATA=/var/lib/postgresql/data/pgdata
   ```

3. Build and start the services:

   ```powershell
   docker-compose up --build
   ```

   Migrations are applied automatically. The API will be available at `http://localhost:8000/`.

4. Optionally create an administrator:

   ```powershell
   docker-compose exec app python manage.py createsuperuser
   ```

## Local development

Ensure PostgreSQL is running and provide its connection settings as environment variables (the `.env` file is used by
Docker Compose). Then:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

To create an administrator who can manage books:

```bash
python manage.py createsuperuser
```

## API documentation

With the development server running, open Swagger UI:

`http://127.0.0.1:8000/api/v1/schema/swagger/`

The OpenAPI schema is available at:

`http://127.0.0.1:8000/api/v1/schema/`

## Authentication

Register a user:

```http
POST /api/v1/users/
Content-Type: application/json

{
  "email": "reader@example.com",
  "password": "secure-password",
  "first_name": "Ada",
  "last_name": "Lovelace"
}
```

Obtain an access and refresh token:

```http
POST /api/v1/users/token/
Content-Type: application/json

{
  "email": "reader@example.com",
  "password": "secure-password"
}
```

Send the access token on protected requests:

```http
Authorization: Bearer <access_token>
```

Access tokens expire after 24 hours; refresh tokens expire after 7 days. Use `POST /api/v1/users/token/refresh/` with
`{ "refresh": "<refresh_token>" }` to obtain a new access token.

## Endpoints

| Resource   | Method                   | Endpoint                       | Access        | Description                                  |
|------------|--------------------------|--------------------------------|---------------|----------------------------------------------|
| Users      | `POST`                   | `/api/v1/users/`               | Public        | Register a user.                             |
| Users      | `POST`                   | `/api/v1/users/token/`         | Public        | Obtain JWT access and refresh tokens.        |
| Users      | `POST`                   | `/api/v1/users/token/refresh/` | Public        | Refresh an access token.                     |
| Users      | `GET`, `PUT`, `PATCH`    | `/api/v1/users/me/`            | Authenticated | Retrieve or update the current user.         |
| Books      | `GET`                    | `/api/v1/books/`               | Public        | List books.                                  |
| Books      | `GET`                    | `/api/v1/books/{id}/`          | Public        | Retrieve a book.                             |
| Books      | `POST`                   | `/api/v1/books/`               | Admin         | Create a book.                               |
| Books      | `PUT`, `PATCH`, `DELETE` | `/api/v1/books/{id}/`          | Admin         | Update or delete a book.                     |
| Borrowings | `GET`                    | `/api/v1/borrowings/`          | Authenticated | List borrowings visible to the current user. |
| Borrowings | `GET`                    | `/api/v1/borrowings/{id}/`     | Authenticated | Retrieve a visible borrowing.                |
| Borrowings | `POST`                   | `/api/v1/borrowings/`          | Authenticated | Borrow an in-stock book.                     |

## Example requests

Create a book as an administrator:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/books/ \
  -H "Authorization: Bearer <admin_access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"The Left Hand of Darkness","author":"Ursula K. Le Guin","cover":"Hard","inventory":3,"daily_fee":"1.50"}'
```

Create a borrowing. `expected_return_date` must be today or later, and the book must have inventory available:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/borrowings/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"book":1,"expected_return_date":"2026-08-01"}'
```

Filter borrowings by active status:

```http
GET /api/v1/borrowings/?is_active=true
```

An active borrowing has no `actual_return_date`. Administrators may additionally filter by borrower, for example
`GET /api/v1/borrowings/?user_id=2`. Regular users are always restricted to their own borrowings.

## Tests

Run the automated test suite with:

```bash
python manage.py test
```
