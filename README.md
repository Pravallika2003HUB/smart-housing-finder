# Smart Housing Finder

A full-stack housing platform where students and bachelors find affordable PGs, hostels and rental rooms with verified listings and real reviews. Built with Django, Django REST Framework and MySQL.

## Problem statement

Students moving to a new city face fake or outdated listings, no trustworthy reviews, broker commissions, and no easy way to compare rent and facilities. Smart Housing Finder puts owners, students and an admin moderation layer on one platform, so every listing is verified before it carries the verified badge and every review comes from a registered account.

## Features

**Student / bachelor**
- Register, login, logout, profile
- Search and filter by location, rent range, property type, gender preference, WiFi, food, parking, furnished, verified-only
- Sort by rent (low to high, high to low) and newest
- Property details with facilities, owner contact, reviews and average rating
- Save favourites, write one review per property, report suspicious listings
- Dashboard with favourites, reviews and reports counts plus recommendations

**Property owner**
- Register as owner, add / edit / delete listings with image upload
- Dashboard with totals: properties, verified, pending, reviews received
- See reports raised on their own properties

**Admin**
- Platform stats: users, students, owners, properties, verified, pending, reviews, pending reports
- Verify / reject / delete listings, manage reports and reviews
- Full Django admin at `/django-admin/`

## Tech stack

- Backend: Python 3.11+, Django 5, Django REST Framework
- Database: MySQL 8 (`smart_housing_db`)
- Frontend: Django templates, Bootstrap 5, custom CSS
- Auth: Django authentication (PBKDF2 password hashing, CSRF protection, login-required views, per-object permission checks)

## Architecture

```
Browser (Bootstrap templates / JSON clients)
        |
Django URLs -> Views (HTML) and DRF API views (JSON)
        |
Forms + Models (ORM)
        |
MySQL: smart_housing_db
```

## Database design

| Model | Key fields | Relationships |
| --- | --- | --- |
| `accounts.User` | email (unique, login field), full_name, phone, role (student/owner/admin) | 1 user -> many properties, reviews, reports, favourites |
| `properties.Property` | title, property_type, location, address, monthly_rent, security_deposit, description, gender_preference, food/wifi/parking/laundry/furnished, contact_number, image, is_verified, is_active, created_at, updated_at | FK owner -> User |
| `reviews.Review` | rating (1-5), comment, created_at | FK property, FK user, unique together (property, user) |
| `reports.Report` | reason, description, status (Pending/Investigating/Resolved/Rejected), created_at | FK property, FK user |
| `favourites.Favourite` | created_at | FK property, FK user, unique together (property, user) |

## Installation

```bash
git clone <your-repo-url>
cd smart_housing

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create the database in MySQL:

```sql
CREATE DATABASE smart_housing_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Copy the environment template and fill in your credentials:

```bash
cp .env.example .env
```

## Environment variables

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key |
| `DJANGO_DEBUG` | `True` locally, `False` in production |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames |
| `DB_NAME` | `smart_housing_db` |
| `DB_USER` | MySQL user |
| `DB_PASSWORD` | MySQL password (never committed) |
| `DB_HOST` | Usually `127.0.0.1` |
| `DB_PORT` | Usually `3306` |

## How to run locally

```bash
python manage.py makemigrations accounts properties reviews reports favourites
python manage.py migrate
python manage.py seed_data          # demo users + sample properties + reviews
python manage.py runserver
```

Open http://127.0.0.1:8000/

Demo logins created by `seed_data` (password `Shf#Housing2026x`):

- `student@demo.com` - student account
- `owner@demo.com` - owner account with sample listings
- `admin@demo.com` - admin / superuser

## API endpoints (DRF)

| Method | Endpoint | Description | Success code |
| --- | --- | --- | --- |
| GET | `/api/properties/` | List active properties (query: `location`, `max_rent`, `property_type`) | 200 |
| POST | `/api/properties/` | Create a listing (owner only, starts unverified) | 201 |
| GET | `/api/properties/<id>/` | Property details | 200 |
| PUT | `/api/properties/<id>/` | Update a listing (owner or admin) | 200 |
| DELETE | `/api/properties/<id>/` | Delete a listing (owner or admin) | 204 |
| POST | `/api/reviews/` | Add or update the caller's review | 201 / 200 |
| POST | `/api/reports/` | Report a property | 201 |
| POST | `/api/favourites/` | Save a property to favourites | 201 / 200 |

Unauthenticated writes return 403, unknown ids return 404.

## Pages

Home, Register, Login, Student Dashboard, Owner Dashboard, Admin Dashboard, Property Search, Property Details, Add Property, Edit Property, My Properties, Favourites, My Reviews, Report Property (on the details page), User Profile, About, Contact, Privacy, Terms, 404.

## Verification workflow

Every new listing is saved with `is_verified = False` and shows "Verification Pending". An admin verifies it from the admin dashboard or Django admin, after which it shows "Verified Listing" and becomes eligible for the featured section on the home page.

## Testing checklist

1. Register a student and an owner; confirm duplicate emails are rejected.
2. Login and logout both accounts.
3. As owner: add, edit and delete a property; confirm it starts as pending.
4. As student: search and filter, sort by rent, open a property.
5. Add a review (twice - the second submission updates, never duplicates).
6. Save and remove a favourite.
7. Report a property and confirm it appears under My Reports as Pending.
8. As admin: verify the pending listing and change the report status.
9. Confirm a student cannot open the add-property page and cannot edit another owner's listing (403).
10. Confirm logout clears the session.

## Future enhancements

Google Maps integration, WhatsApp contact button, AI-based fake listing detection, personalised recommendations, online payments, email notifications, location-based suggestions, analytics for owners.

## Author

Built as a full-stack portfolio project.
