from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import News, Media, Announcement, Event, TeamMember, ContactMessage, JoinRequest
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import cloudinary.uploader


def _send_html_email(subject, to_email, html_content, plain_text):
    msg = EmailMultiAlternatives(subject, plain_text, settings.DEFAULT_FROM_EMAIL, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


def _cloudinary_delete(file_field):
    if file_field and hasattr(file_field, 'public_id') and file_field.public_id:
        try:
            cloudinary.uploader.destroy(file_field.public_id)
        except Exception as e:
            print(f'⚠️ Cloudinary delete error: {e}')


def home(request):
    announcements = Announcement.objects.filter(is_active=True)
    media_images = Media.objects.filter(file_type='image')
    media_videos = Media.objects.filter(file_type='video')
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')[:4]
    latest_news = News.objects.all().order_by('-created_at')[:3]
    join_members = JoinRequest.objects.all()
    return render(request, 'core/base.html', {
        'announcements': announcements,
        'media_images': media_images,
        'media_videos': media_videos,
        'upcoming_events': upcoming_events,
        'latest_news': latest_news,
        'join_members': join_members,
    })


def news_page(request):
    news_list = News.objects.all()
    return render(request, 'core/news_page.html', {'news_list': news_list})


def events_page(request):
    events = Event.objects.filter(date__gte=timezone.now().date())
    return render(request, 'core/events_page.html', {'events': events})


def team_page(request):
    team_members = TeamMember.objects.all()
    return render(request, 'core/team_page.html', {'team_members': team_members})


def about_page(request):
    return render(request, 'core/about_page.html')


def contact_message(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, email, message]):
            from django.contrib import messages
            messages.error(request, '❌ Please fill in all fields!')
            return redirect('home')

        try:
            ContactMessage.objects.create(name=name, email=email, message=message)

            try:
                admin_html = f"""
                <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;background:#0a2e1f;border-radius:16px;overflow:hidden;">
                    <div style="background:linear-gradient(135deg,#1a5c35,#0a2e1f);padding:30px;text-align:center;">
                        <div style="font-size:40px;">🔔</div>
                        <h2 style="color:#f0c15b;margin:8px 0 0;">New Contact Message</h2>
                    </div>
                    <div style="padding:30px;">
                        <div style="background:rgba(255,255,255,0.05);border-left:4px solid #50d268;border-radius:8px;padding:20px;margin-bottom:20px;">
                            <p style="color:#50d268;font-size:12px;font-weight:700;letter-spacing:1px;margin-bottom:12px;">SENDER DETAILS</p>
                            <p style="color:white;font-size:14px;margin:4px 0;"><strong>Name:</strong> {name}</p>
                            <p style="color:white;font-size:14px;margin:4px 0;"><strong>Email:</strong> {email}</p>
                        </div>
                        <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:20px;">
                            <p style="color:#f0c15b;font-size:12px;font-weight:700;letter-spacing:1px;margin-bottom:10px;">MESSAGE</p>
                            <p style="color:rgba(255,255,255,0.8);font-size:14px;line-height:1.7;">{message}</p>
                        </div>
                        <p style="color:rgba(255,255,255,0.3);font-size:11px;margin-top:20px;">Received at: {timezone.now().strftime('%d %b %Y, %I:%M %p')}</p>
                    </div>
                </div>
                """
                _send_html_email(f'🔔 New Message from {name}', settings.CONTACT_FORM_RECIPIENT_EMAIL, admin_html,
                    f"From: {name}\nEmail: {email}\nMessage: {message}")
                print(f"✅ Admin email sent to {settings.CONTACT_FORM_RECIPIENT_EMAIL}")
            except Exception as e:
                print(f"⚠️ Error sending admin email: {e}")

            try:
                visitor_html = f"""
                <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;background:#0a2e1f;border-radius:16px;overflow:hidden;">
                    <div style="background:linear-gradient(135deg,#1a5c35,#0a2e1f);padding:40px 30px;text-align:center;">
                        <div style="font-size:50px;">✅</div>
                        <h1 style="color:#f0c15b;font-size:22px;margin:10px 0 0;">Message Received!</h1>
                        <p style="color:rgba(255,255,255,0.5);font-size:13px;margin-top:6px;">Arjungeria AGNI Sangha Football Club</p>
                    </div>
                    <div style="padding:36px 30px;">
                        <p style="color:#dbe5d8;font-size:15px;">Hi <strong style="color:#50d268;">{name}</strong>,</p>
                        <p style="color:rgba(255,255,255,0.7);font-size:14px;line-height:1.8;margin:16px 0;">
                            Thank you for reaching out to us! We've received your message and our team will get back to you as soon as possible. 🙏
                        </p>
                        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px 20px;margin:20px 0;">
                            <p style="color:rgba(255,255,255,0.4);font-size:12px;margin-bottom:8px;">YOUR MESSAGE</p>
                            <p style="color:rgba(255,255,255,0.7);font-size:13px;line-height:1.7;font-style:italic;">"{message}"</p>
                        </div>
                        <p style="color:rgba(255,255,255,0.5);font-size:13px;">We typically respond within 24 hours. 🕒</p>
                    </div>
                    <div style="background:rgba(0,0,0,0.3);padding:20px 30px;text-align:center;border-top:1px solid rgba(255,255,255,0.05);">
                        <p style="color:#50d268;font-size:13px;font-weight:700;">AGNI Sangha — Igniting Passion, Inspiring Excellence</p>
                        <p style="color:rgba(255,255,255,0.3);font-size:11px;margin-top:4px;">Arjungeria, West Bengal, India</p>
                    </div>
                </div>
                """
                _send_html_email("✅ We've received your message!", email, visitor_html,
                    f"Hi {name},\n\nThank you for contacting Arjungeria AGNI Sangha. We'll get back to you soon.\n\nAGNI Sangha Team")
                print(f"✅ Confirmation email sent to {email}")
            except Exception as e:
                print(f"⚠️ Error sending confirmation email: {e}")

            from django.contrib import messages
            messages.success(request, '✅ Message sent successfully! We will contact you soon.')

        except Exception as e:
            print(f"❌ Error saving message: {e}")
            from django.contrib import messages
            messages.error(request, '❌ Error saving your message. Please try again.')

    return redirect('home')


def join_club(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()

        if not all([name, age, phone, email]):
            from django.contrib import messages
            messages.error(request, '❌ Please fill in all fields!')
            return redirect('home')

        if JoinRequest.objects.filter(email=email).exists():
            from django.contrib import messages
            messages.error(request, '❌ This email is already registered!')
            return redirect('home')

        try:
            JoinRequest.objects.create(name=name, age=int(age), phone=phone, email=email)
            try:
                html = f"""
                <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;background:#0a2e1f;border-radius:16px;overflow:hidden;">
                    <div style="background:linear-gradient(135deg,#1a5c35,#0a2e1f);padding:40px 30px;text-align:center;">
                        <div style="font-size:60px;margin-bottom:10px;">⚽</div>
                        <h1 style="color:#f0c15b;font-size:26px;margin:0;">Welcome to the Family!</h1>
                        <p style="color:rgba(255,255,255,0.6);margin-top:8px;font-size:14px;">Arjungeria AGNI Sangha Football Club</p>
                    </div>
                    <div style="padding:36px 30px;">
                        <p style="color:#dbe5d8;font-size:16px;margin-bottom:20px;">Hey <strong style="color:#50d268;">{name}</strong> 👋,</p>
                        <p style="color:rgba(255,255,255,0.7);font-size:14px;line-height:1.8;margin-bottom:24px;">
                            We are absolutely thrilled to have you on board! You've officially joined the <strong style="color:#f0c15b;">Arjungeria AGNI Sangha Football Club</strong> — a family built on passion, teamwork, and the love of the beautiful game. 🔥
                        </p>
                        <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(80,210,104,0.2);border-radius:12px;padding:20px;margin-bottom:24px;">
                            <p style="color:#50d268;font-size:13px;font-weight:700;margin-bottom:12px;letter-spacing:1px;">YOUR DETAILS</p>
                            <table style="width:100%;font-size:13px;color:rgba(255,255,255,0.7);">
                                <tr><td style="padding:4px 0;">👤 Name</td><td style="color:white;font-weight:600;">{name}</td></tr>
                                <tr><td style="padding:4px 0;">🎂 Age</td><td style="color:white;font-weight:600;">{age}</td></tr>
                                <tr><td style="padding:4px 0;">📞 Phone</td><td style="color:white;font-weight:600;">{phone}</td></tr>
                                <tr><td style="padding:4px 0;">📧 Email</td><td style="color:white;font-weight:600;">{email}</td></tr>
                            </table>
                        </div>
                        <p style="color:rgba(255,255,255,0.6);font-size:13px;line-height:1.7;">
                            Our team will reach out to you soon with further details about training sessions, matches, and club activities. Stay tuned! 🏆
                        </p>
                    </div>
                    <div style="background:rgba(0,0,0,0.3);padding:20px 30px;text-align:center;border-top:1px solid rgba(255,255,255,0.05);">
                        <p style="color:#50d268;font-size:13px;font-weight:700;margin-bottom:4px;">AGNI Sangha — Igniting Passion, Inspiring Excellence</p>
                        <p style="color:rgba(255,255,255,0.3);font-size:11px;">Arjungeria, West Bengal, India</p>
                    </div>
                </div>
                """
                plain = f"Hi {name},\n\nWelcome to Arjungeria AGNI Sangha Football Club!\nWe are thrilled to have you. Our team will contact you soon.\n\nAGNI Sangha Team"
                _send_html_email('⚽ Welcome to Arjungeria AGNI Sangha!', email, html, plain)
                print(f"✅ Welcome email sent to {email}")
            except Exception as e:
                print(f"⚠️ Error sending welcome email: {e}")

            from django.contrib import messages
            messages.success(request, f'✅ Welcome {name}! You have successfully joined the club. Check your email!')
        except Exception as e:
            print(f"❌ Error saving join request: {e}")
            from django.contrib import messages
            messages.error(request, '❌ Something went wrong. Please try again.')

    return redirect('home')


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    error = None
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        error = 'Invalid credentials or not an admin.'
    return render(request, 'core/admin/login.html', {'error': error})


@login_required(login_url='admin_login')
def admin_dashboard(request):
    return render(request, 'core/admin/dashboard.html', {
        'news_count': News.objects.count(),
        'media_count': Media.objects.count(),
        'announcement_count': Announcement.objects.filter(is_active=True).count(),
        'event_count': Event.objects.filter(date__gte=timezone.now().date()).count(),
        'team_count': TeamMember.objects.count(),
        'members_count': JoinRequest.objects.count(),
    })


@login_required(login_url='admin_login')
def members_manage(request):
    members = JoinRequest.objects.all()
    return render(request, 'core/admin/members_manage.html', {'members': members})


@login_required(login_url='admin_login')
def member_delete(request, pk):
    get_object_or_404(JoinRequest, pk=pk).delete()
    return redirect('members_manage')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required(login_url='admin_login')
def news_manage(request):
    if request.method == 'POST':
        News.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            cover_image=request.FILES.get('cover_image'),
            attachment=request.FILES.get('attachment')
        )
        return redirect('news_manage_success')
    news_list = News.objects.all()
    return render(request, 'core/admin/news_manage.html', {'news_list': news_list})


@login_required(login_url='admin_login')
def news_manage_success(request):
    news_list = News.objects.all()
    return render(request, 'core/admin/news_manage.html', {'news_list': news_list, 'success': True})


@login_required(login_url='admin_login')
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    _cloudinary_delete(news.cover_image)
    _cloudinary_delete(news.attachment)
    news.delete()
    return redirect('news_manage')


@login_required(login_url='admin_login')
def media_manage(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for f in files:
            name = f.name.lower()
            if name.endswith('.pdf'):
                file_type = 'pdf'
            elif name.endswith(('.mp4', '.mov', '.avi', '.webm', '.mkv')):
                file_type = 'video'
            else:
                file_type = 'image'
            title = f.name.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
            Media.objects.create(title=title, file=f, file_type=file_type)
        return redirect('media_manage_success')
    media_list = Media.objects.all()
    return render(request, 'core/admin/media_manage.html', {'media_list': media_list})


@login_required(login_url='admin_login')
def media_manage_success(request):
    if request.method == 'POST':
        return redirect('media_manage')
    media_list = Media.objects.all()
    return render(request, 'core/admin/media_manage.html', {'media_list': media_list, 'success': True})


@login_required(login_url='admin_login')
def media_delete(request, pk):
    media = get_object_or_404(Media, pk=pk)
    _cloudinary_delete(media.file)
    media.delete()
    return redirect('media_manage')


@login_required(login_url='admin_login')
def announcement_manage(request):
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            ann = get_object_or_404(Announcement, pk=request.POST['delete_id'])
            _cloudinary_delete(ann.qr_code)
            ann.delete()
        else:
            Announcement.objects.create(
                title=request.POST['title'],
                amount=request.POST['amount'],
                upi_id=request.POST['upi_id'],
                qr_code=request.FILES.get('qr_code'),
                is_active='is_active' in request.POST
            )
        return redirect('announcement_manage_success')
    announcements = Announcement.objects.all()
    return render(request, 'core/admin/announcement_manage.html', {'announcements': announcements})


@login_required(login_url='admin_login')
def announcement_manage_success(request):
    announcements = Announcement.objects.all()
    return render(request, 'core/admin/announcement_manage.html', {'announcements': announcements, 'success': True})


@login_required(login_url='admin_login')
def event_manage(request):
    if request.method == 'POST':
        Event.objects.create(
            type=request.POST['type'],
            title=request.POST['title'],
            date=request.POST['date'],
            time=request.POST.get('time') or None,
            venue=request.POST.get('venue'),
            opponent=request.POST.get('opponent'),
            description=request.POST.get('description'),
        )
        return redirect('event_manage_success')
    events = Event.objects.all()
    return render(request, 'core/admin/event_manage.html', {'events': events})


@login_required(login_url='admin_login')
def event_manage_success(request):
    events = Event.objects.all()
    return render(request, 'core/admin/event_manage.html', {'events': events, 'success': True})


@login_required(login_url='admin_login')
def event_delete(request, pk):
    get_object_or_404(Event, pk=pk).delete()
    return redirect('event_manage')


@login_required(login_url='admin_login')
def team_manage(request, pk=None):
    edit_member = None
    if pk:
        edit_member = get_object_or_404(TeamMember, pk=pk)

    if request.method == 'POST':
        if edit_member:
            edit_member.name = request.POST['name']
            edit_member.role = request.POST.get('role', 'Player')
            if 'photo' in request.FILES:
                _cloudinary_delete(edit_member.photo)
                edit_member.photo = request.FILES['photo']
            edit_member.bio = request.POST.get('bio')
            edit_member.social_facebook = request.POST.get('social_facebook')
            edit_member.social_instagram = request.POST.get('social_instagram')
            edit_member.save()
            return redirect('team_manage')
        else:
            TeamMember.objects.create(
                name=request.POST['name'],
                role=request.POST.get('role', 'Player'),
                photo=request.FILES.get('photo'),
                bio=request.POST.get('bio'),
                social_facebook=request.POST.get('social_facebook'),
                social_instagram=request.POST.get('social_instagram'),
            )
            return redirect('team_manage_success')
    team_members = TeamMember.objects.all()
    return render(request, 'core/admin/team_manage.html', {
        'team_members': team_members,
        'edit_member': edit_member
    })


@login_required(login_url='admin_login')
def team_manage_success(request):
    team_members = TeamMember.objects.all()
    return render(request, 'core/admin/team_manage.html', {
        'team_members': team_members,
        'success': True
    })


@login_required(login_url='admin_login')
def team_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    _cloudinary_delete(member.photo)
    member.delete()
    return redirect('team_manage')
