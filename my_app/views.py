from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from my_app.forms import AddUserForm, EventForm
from my_app.models import Event


@login_required(login_url='login')
def index(request):
    forms = EventForm()
    events = Event.objects.filter(user=request.user)
    event_list = []
    # start: '2020-09-16T16:00:00'
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_time.date().strftime("%Y-%m-%dT%H:%M:%S"),
            'end': event.end_time.date().strftime("%Y-%m-%dT%H:%M:%S"),
        })

    if request.method == 'POST':
        forms = EventForm(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('index')

    context = {
        'form': forms,
        'events': event_list,
    }
    return render(request, 'calendar.html', context)


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            loginUsername = request.POST.get('loginUsername')
            loginPassword = request.POST.get('loginPassword')

            user = authenticate(request, username=loginUsername, password=loginPassword)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'username or password is incorrect')

        return render(request, 'login.html')


def logoutuser(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = AddUserForm()

        if request.method == 'POST':
            form = AddUserForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('login')
        context = {'form': form, }
        return render(request, 'register.html', context)


def editevent(request, id):
    event = Event.objects.get(id=id)
    form = EventForm(instance=event)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            event.title = newform.title
            event.start_time = newform.start_time
            event.end_time = newform.end_time
            event.save()
            return redirect('index')
    context = {'form': form, }
    return render(request, 'editevent.html', context)
