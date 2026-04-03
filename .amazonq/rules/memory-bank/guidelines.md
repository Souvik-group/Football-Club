# Development Guidelines — Arjungeria AGNI Sangha Football Club

## Code Quality Standards

### Python / Django Conventions
- All views are **function-based** — do not introduce class-based views
- Use `@login_required(login_url='admin_login')` on every admin/dashboard view
- Import `messages` locally inside the view function, not at module level:
  ```python
  from django.contrib import messages
  messages.success(request, '✅ Done!')
  ```
- Use emoji prefixes in user-facing messages: `✅` success, `❌` error, `⚠️` warning
- Use `print()` for server-side debug logging (not Python `logging` module)

### POST-Redirect-GET Pattern
All form submissions must redirect after processing — never render directly after POST:
```python
if request.method == 'POST':
    # process...
    return redirect('view_name_success')  # or redirect('view_name')
```
Success state is shown via a separate `*_manage_success` view that passes `success=True` to the template.

### File Deletion Pattern
Always clean up associated files before deleting a model instance:
```python
if instance.file_field:
    try:
        instance.file_field.delete(save=False)
    except OSError:
        pass
instance.delete()
```

### Model Conventions
- All models define `__str__` returning a human-readable string
- All models define `class Meta: ordering = [...]` — newest-first for content (`-created_at`), chronological for events/members (`date`, `joined_date`)
- Optional fields use `blank=True, null=True`
- Choice fields use a `TYPE_CHOICES` / `FILE_TYPES` list defined at class level
- Timestamps use `auto_now_add=True` (never `auto_now`)
- Primary keys use Django's default `BigAutoField` (set globally in settings)

### URL Naming Conventions
- Public pages: `home`, `news_page`, `events_page`, `team_page`, `about_page`
- Admin views: `admin_login`, `admin_dashboard`, `admin_logout`
- CRUD pattern: `{resource}_manage`, `{resource}_manage_success`, `{resource}_delete`
- Edit pattern: `{resource}_edit` (maps to same view as manage, with `pk` arg)
- Delete URLs always include `<int:pk>/`

## Template Patterns

### Template Organization
- `base.html` is the **home page** (not an abstract base) — it assembles all components via `{% include %}`
- Page templates (`*_page.html`) are standalone — they do NOT extend `base.html`
- Components live in `core/templates/core/components/` and are included with:
  ```django
  {% include "core/components/component_name.html" %}
  ```
- Admin templates live in `core/templates/core/admin/`

### Static Files
- Always use `{% load static %}` at the top of every template that references static assets
- Reference static files with `{% static 'css/file.css' %}` or `{% static 'images/file.png' %}`
- Page-specific CSS files exist for: `navbar.css`, `hero.css`, `about.css`, `contact.css`

### Django Messages Display
Messages are rendered in `base.html` as fixed-position toast notifications (top-right), auto-dismissed after ~4.8 seconds via JavaScript. Use Django's messages framework for all user feedback.

### JavaScript Style
- Vanilla JS only — no frameworks
- Scripts are inline within templates (no separate `.js` files for custom code)
- Use `localStorage` for one-time UI state (e.g., intro animation shown flag)
- Smooth scroll implemented manually via `window.scrollTo({ behavior: 'smooth' })`

## Settings & Configuration

### Environment Variables
All secrets and environment-specific values must come from `os.getenv()`:
```python
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```
Never hardcode credentials. Use `.env.example` as the reference template.

### Media Storage
- Dev: local filesystem (`MEDIA_ROOT`)
- Prod: Cloudinary via `DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'`
- Upload paths by content type: `news/`, `team/`, `qr_codes/`, `media_uploads/`

### File Upload Limits
Configured in settings — do not reduce without discussion:
- `DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600` (100 MB)
- `FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600` (100 MB)
- `DATA_UPLOAD_MAX_NUMBER_FILES = 100`

## Admin System

### Custom Admin Site
`CustomAdminSite` in `admin.py` restricts access to a single email (`settings.ADMIN_EMAIL`):
```python
class CustomAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.email == settings.ADMIN_EMAIL
```
The custom dashboard at `/dashboard/` uses `@login_required` + `is_staff` check (in `admin_login` view). These are two separate systems.

### Django Admin Registrations
Use `@admin.register(ModelClass)` decorator pattern. Always define `list_display`, add `search_fields` and `list_filter` where useful. Use `readonly_fields` for auto-set fields like `created_at`.

## Media Management

### Auto File Type Detection (media_manage view)
File type is inferred from extension — maintain this logic when adding new types:
```python
if name.endswith('.pdf'):
    file_type = 'pdf'
elif name.endswith(('.mp4', '.mov', '.avi', '.webm', '.mkv')):
    file_type = 'video'
else:
    file_type = 'image'
```

### Auto Title Generation
Titles are auto-generated from filenames: `f.name.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()`

## Contact Form & Email

### Dual Email Pattern
On contact form submission, two emails are sent:
1. Notification to admin (`settings.CONTACT_FORM_RECIPIENT_EMAIL`)
2. Confirmation to the visitor

Both are wrapped in `try/except` with `fail_silently=False` — email failures are logged via `print()` but do not block the user flow.

### Email Configuration
Production uses Gmail SMTP or SendGrid. Always configure via env vars. Never hardcode credentials.
