# Tech Stack — Arjungeria AGNI Sangha Football Club

## Languages & Runtime
- **Python** 3.11.9 (runtime.txt)
- **JavaScript** (Tailwind CLI only, no custom JS framework)
- **HTML/CSS** with Tailwind CSS 4.2.1

## Backend Framework
- **Django** 5.2.7

## Python Dependencies (requirements.txt)
| Package | Version | Purpose |
|---------|---------|---------|
| Django | 5.2.7 | Web framework |
| gunicorn | 25.3.0 | Production WSGI server |
| whitenoise | 6.12.0 | Static file serving |
| dj-database-url | 3.1.2 | DATABASE_URL parsing |
| psycopg[binary] | 3.3.3 | PostgreSQL adapter |
| django-cors-headers | 4.9.0 | CORS support |
| djangorestframework | 3.16.1 | REST API support |
| Pillow | 10.4.0 | Image processing |
| cloudinary | (installed) | Cloud media storage |
| cloudinary_storage | (installed) | Django Cloudinary integration |

## Frontend
- **Tailwind CSS** 4.2.1 via `@tailwindcss/cli`
- Build: `npx tailwindcss -i ./input.css -o ./output.css --watch`

## Database
- **Development:** SQLite3 (`db.sqlite3`)
- **Production:** PostgreSQL via `DATABASE_URL` env var (dj-database-url)

## Media Storage
- **Development:** Local filesystem (`MEDIA_ROOT = BASE_DIR / 'media'`)
- **Production:** Cloudinary (`DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'`)

## Static Files
- Collected to `staticfiles/` via `python manage.py collectstatic`
- Served by **WhiteNoise** (`CompressedManifestStaticFilesStorage`)

## Email
- **Development:** Console backend or SMTP (Gmail)
- **Production:** SMTP (SendGrid recommended) via env vars

## Deployment Target
- **Render.com** (`.onrender.com` in ALLOWED_HOSTS)

## Required Environment Variables
```
SECRET_KEY=
DEBUG=True|False
DATABASE_URL=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
CONTACT_FORM_RECIPIENT_EMAIL=
```

## Development Commands
```bash
# Run dev server
python manage.py runserver

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Build Tailwind CSS
npx tailwindcss -i ./input.css -o ./output.css --watch

# Dump/load data
python manage.py dumpdata > local_backup.json
python manage.py loaddata local_backup.json
```
