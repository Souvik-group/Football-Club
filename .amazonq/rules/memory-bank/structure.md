# Project Structure — Arjungeria AGNI Sangha Football Club

## Directory Layout
```
footbalClub/
├── core/                          # Main Django app
│   ├── migrations/                # 10 migration files (0001–0010)
│   ├── static/
│   │   ├── css/                   # Page-specific CSS (about, contact, hero, navbar)
│   │   ├── images/                # Static images (logo, team photos)
│   │   └── videos/                # Static video assets
│   ├── templates/core/
│   │   ├── admin/                 # Custom dashboard templates (login, dashboard, *_manage.html)
│   │   ├── components/            # Reusable template partials
│   │   ├── base.html              # Home page / base layout
│   │   ├── about_page.html
│   │   ├── events_page.html
│   │   ├── news_page.html
│   │   └── team_page.html
│   ├── models.py                  # All data models
│   ├── views.py                   # All view functions
│   ├── urls.py                    # App-level URL patterns
│   ├── admin.py                   # Django admin registrations + CustomAdminSite
│   └── apps.py
├── football_club/                 # Django project config
│   ├── settings.py                # All settings (env-driven)
│   ├── urls.py                    # Root URL config (includes core.urls)
│   ├── wsgi.py
│   └── asgi.py
├── media/                         # User-uploaded files (Cloudinary in prod)
│   ├── media_uploads/             # General media (images/videos/PDFs)
│   ├── news/                      # News cover images & attachments
│   ├── team/                      # Team member photos
│   └── qr_codes/                  # Announcement QR codes
├── static/                        # Project-level static source
├── staticfiles/                   # Collected static files (whitenoise serves these)
├── .amazonq/rules/memory-bank/    # Memory Bank documentation
├── .env.example                   # Environment variable template
├── requirements.txt               # Python dependencies
├── package.json                   # Node.js (Tailwind CSS)
├── runtime.txt                    # Python version for deployment
└── manage.py
```

## Core Models
| Model | Key Fields | Ordering |
|-------|-----------|---------|
| `News` | title, content, cover_image, attachment, created_at | `-created_at` |
| `Event` | type (match/event), title, date, time, venue, opponent | `date` |
| `Media` | title, file, file_type (image/video/pdf), uploaded_at | `-uploaded_at` |
| `Announcement` | title, description, amount, upi_id, qr_code, is_active | `-created_at` |
| `TeamMember` | name, role, photo, bio, social_facebook, social_instagram | `joined_date` |
| `ContactMessage` | name, email, message, is_read, created_at | `-created_at` |

## Architectural Patterns
- **Single-app architecture** — all logic lives in the `core` app
- **Function-based views (FBVs)** — no class-based views used
- **Dual admin system** — custom `/dashboard/` for club admins + Django's `/admin/` for superusers
- **POST-redirect-GET** — all form submissions redirect after success to prevent re-submission
- **Success URL pattern** — separate `*_manage_success` views/URLs to show success state
- **File cleanup on delete** — views manually call `file.delete(save=False)` before deleting model instances
- **Environment-driven config** — all secrets and service credentials via `os.getenv()`
