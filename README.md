Live -https://agnisangha-club.onrender.com/

# 🏆 Arjungeria AGNI Sangha - Football Club Website

A Django-based web platform for managing a football club's team, events, news, media, and announcements.

## 📋 Project Overview

**AGNI Sangha** is a passionate football club website that showcases:
- Team member profiles
- Upcoming events and matches
- News and announcements
- Media gallery (images & videos)
- Admin dashboard for content management

## 🛠️ Tech Stack

- **Backend:** Django 5.2.7
- **Database:** SQLite3
- **Frontend:** HTML, CSS, Tailwind CSS 4.2.1
- **Media Handling:** Pillow

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js (for Tailwind CSS)

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd footbalClub
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node dependencies:**
   ```bash
   npm install
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Build Tailwind CSS (if making style changes):**
   ```bash
   npx tailwindcss -i ./input.css -o ./output.css --watch
   ```

## 🌐 Access the Application

- **Website:** `http://127.0.0.1:8000/`
- **Admin Dashboard:** `http://127.0.0.1:8000/admin/`

## 📁 Project Structure

```
footbalClub/
├── core/                      # Main app
│   ├── models.py             # Database models (Team, News, Events, etc.)
│   ├── views.py              # View logic
│   ├── urls.py               # URL routing
│   ├── admin.py              # Admin interface configuration
│   ├── templates/
│   │   └── core/
│   │       ├── base.html     # Base template
│   │       ├── *_page.html   # Page templates
│   │       ├── admin/        # Admin dashboard templates
│   │       └── components/   # Reusable components
│   └── static/
│       ├── css/              # Stylesheets
│       ├── images/           # Static images
│       └── videos/           # Static videos
├── football_club/             # Project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py               # Main URL config
│   └── wsgi.py               # WSGI configuration
├── media/                     # User-uploaded media
│   ├── media_uploads/
│   ├── news/
│   ├── team/
│   └── qr_codes/
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── package.json              # Node.js dependencies
└── requirements.txt          # Python dependencies
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Use `python-decouple` to load these variables in `settings.py`.

## 📚 Key Features

✅ **Team Management** - Add/edit player profiles  
✅ **News & Announcements** - Post club updates  
✅ **Events Calendar** - Manage upcoming matches & events  
✅ **Media Gallery** - Upload and showcase photos/videos  
✅ **Admin Dashboard** - Centralized management interface  
✅ **Responsive Design** - Mobile-friendly UI  

## 🚀 Deployment

For production deployment:
1. Set `DEBUG = False` in `settings.py`
2. Configure allowed hosts
3. Use a production database (PostgreSQL recommended)
4. Set up static files with `python manage.py collectstatic`
5. Use a WSGI server (Gunicorn, uWSGI)

## 📝 License

ISC

## 👨‍💻 Author

Arjungeria AGNI Sangha Team

---

**Last Updated:** March 2026
