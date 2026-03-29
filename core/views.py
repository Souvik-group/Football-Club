from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import News, Media, Announcement, Event, TeamMember
from django.utils import timezone


def home(request):
    announcements = Announcement.objects.filter(is_active=True)
    media_images = Media.objects.filter(file_type='image')
    media_videos = Media.objects.filter(file_type='video')
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')[:4]
    latest_news = News.objects.all().order_by('-created_at')[:3]
    return render(request, 'core/base.html', {
        'announcements': announcements,
        'media_images': media_images,
        'media_videos': media_videos,
        'upcoming_events': upcoming_events,
        'latest_news': latest_news,
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
    })


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
    if news.cover_image:
        try:
            news.cover_image.delete(save=False)
        except OSError:
            pass
    if getattr(news, 'attachment', None):
        try:
            news.attachment.delete(save=False)
        except OSError:
            pass
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
    if media.file:
        try:
            media.file.delete(save=False)
        except OSError:
            pass
    media.delete()
    return redirect('media_manage')


@login_required(login_url='admin_login')
def announcement_manage(request):
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            ann = get_object_or_404(Announcement, pk=request.POST['delete_id'])
            if getattr(ann, 'qr_code', None):
                try:
                    ann.qr_code.delete(save=False)
                except OSError:
                    pass
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
                if edit_member.photo:
                    try:
                        edit_member.photo.delete(save=False)
                    except OSError:
                        pass
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
    if member.photo:
        try:
            member.photo.delete(save=False)
        except OSError:
            pass
    member.delete()
    return redirect('team_manage')


@login_required(login_url='admin_login')
def team_manage_success(request):
    team_members = TeamMember.objects.all()
    return render(request, 'core/admin/team_manage.html', {
        'team_members': team_members,
        'success': True
    })
