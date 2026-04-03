# Product Overview — Arjungeria AGNI Sangha Football Club

## Purpose
A Django-based web platform for the AGNI Sangha football club to manage and showcase club content publicly while providing admins a dashboard for content management.

## Key Features
- **Home Page** — Active announcements, media gallery, upcoming events, latest news
- **News** — Club news articles with cover images and file attachments
- **Events** — Upcoming matches and events with date, venue, opponent details
- **Team** — Player/staff profiles with photos, bios, and social links
- **Media Gallery** — Upload and display images, videos, and PDFs
- **Announcements** — Payment/fee announcements with UPI ID and QR code support
- **Contact Form** — Visitor messages saved to DB + email notifications to admin and visitor
- **Custom Admin Dashboard** — Login-protected CRUD interface at `/dashboard/` (separate from Django's `/admin/`)

## Target Users
- **Club members & fans** — Browse team info, news, events, media
- **Club admins** — Manage all content via the custom dashboard (restricted to a single configured email)

## Public URLs
| Path | Purpose |
|------|---------|
| `/` | Home page |
| `/news/` | News listing |
| `/events/` | Upcoming events |
| `/team/` | Team members |
| `/about/` | About the club |
| `/contact/` | Contact form (POST) |

## Admin URLs
| Path | Purpose |
|------|---------|
| `/admin-login/` | Custom admin login |
| `/dashboard/` | Dashboard overview |
| `/dashboard/news/` | Manage news |
| `/dashboard/media/` | Manage media |
| `/dashboard/announcements/` | Manage announcements |
| `/dashboard/events/` | Manage events |
| `/dashboard/team/` | Manage team members |
| `/admin/` | Django built-in admin |
