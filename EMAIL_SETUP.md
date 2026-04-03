# Contact Form → Email Pipeline Setup Guide 📬

Your contact form is now fully wired to send emails! Here's how to configure it for production.

---

## What's Been Set Up

✅ **Contact Form Model** - Messages are saved to database
✅ **Email Notifications** - Admin gets notified on new messages
✅ **Auto-Replies** - Visitors get confirmation emails
✅ **Admin Dashboard** - View all messages in Django admin
✅ **URL Endpoint** - `/contact/` receives form submissions

---

## Configuration Steps

### Option 1: Using Gmail (Recommended for Development)

#### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification

#### Step 2: Generate App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select **Mail** and **Windows Computer**
3. Google will generate a 16-character password
4. Copy this password

#### Step 3: Add to Environment Variables
Create a `.env` file in your project root:

```bash
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here
DEFAULT_FROM_EMAIL=your-gmail@gmail.com
CONTACT_FORM_RECIPIENT_EMAIL=barammanik@gmail.com
```

#### Step 4: Install python-decouple (Optional, for .env management)
```bash
pip install python-decouple
```

Then update `settings.py`:
```python
from decouple import config

EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
```

---

### Option 2: Using SendGrid (Recommended for Production)

#### Step 1: Create SendGrid Account
1. Sign up at [SendGrid](https://sendgrid.com)
2. Go to Settings → API Keys
3. Create a new API key and copy it

#### Step 2: Update Settings
Add to `.env`:
```bash
EMAIL_BACKEND=sendgrid_backend.SendgridBackend
SENDGRID_API_KEY=your-api-key-here
DEFAULT_FROM_EMAIL=noreply@footballclub.com
CONTACT_FORM_RECIPIENT_EMAIL=barammanik@gmail.com
```

#### Step 3: Install SendGrid Backend
```bash
pip install sendgrid-backend
```

---

### Option 3: Using Render (If Deployed on Render)

Render provides built-in SMTP:

```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_API_KEY', '')
```

---

### Option 4: Using Mailgun

```bash
pip install django-anymail[mailgun]
```

```python
# In settings.py
ANYMAIL = {
    "MAILGUN_API_KEY": os.getenv('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": os.getenv('MAILGUN_SENDER_DOMAIN'),
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@footballclub.com"
```

---

## Testing Locally

To test without sending real emails, use the console backend:

```bash
# In settings.py (default during development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Emails will print to your console instead!

Or use file backend to save emails as files:
```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
```

---

## Production Deployment Checklist

When deploying to Render or production:

1. ✅ Add environment variables in platform settings:
   - `EMAIL_HOST_USER`
   - `EMAIL_HOST_PASSWORD`
   - `CONTACT_FORM_RECIPIENT_EMAIL`
   - `EMAIL_BACKEND` (if using custom backend)

2. ✅ Set `DEBUG = False` in production

3. ✅ Test form submission before going live

4. ✅ Monitor email delivery in admin dashboard

---

## Viewing Contact Messages

### In Django Admin
1. Login to `/admin/`
2. Go to **Contact Messages**
3. Click any message to view details
4. Mark as read/unread

### In Database (via Management Command)
Create a custom admin command or visit admin panel directly.

---

## Troubleshooting

### Emails Not Sending?

**Check 1: Email Backend**
```python
# settings.py - check you're not using console backend in production
print(settings.EMAIL_BACKEND)
```

**Check 2: Environment Variables**
```bash
# In terminal, verify they're loaded
python manage.py shell
>>> from django.conf import settings
>>> print(settings.EMAIL_HOST_USER)
>>> print(settings.EMAIL_HOST_PASSWORD)
```

**Check 3: Gmail Security**
- Less secure apps might fail
- Use App Passwords instead
- Check if 2FA is enabled

**Check 4: SMTP Connection**
```python
# Test SMTP connection
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

### Still Getting Errors?

Check server logs:
```bash
# For Render deployment
# Visit Render dashboard → Logs
```

---

## Email Template Customization

Want to customize the emails? Edit the `contact_message` view in `core/views.py`:

```python
# Line ~70-85 in views.py
admin_email_body = f"""
Your custom email here...
Name: {name}
Email: {email}
Message: {message}
"""
```

---

## Security Notes

⚠️ **Never commit credentials to git!**
- Always use `.env` files or environment variables
- Add `.env` to `.gitignore`
- Never share API keys or app passwords

---

## Next Steps

1. Choose your email provider (Gmail for dev, SendGrid for prod)
2. Add credentials to `.env` file
3. Test by submitting the contact form
4. Check Django admin for received messages
5. Verify emails arrive in your inbox

Questions? Check Django's [Email Documentation](https://docs.djangoproject.com/en/5.2/topics/email/)
