from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, AuthenticationForm, loginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import Records
from django.db.models import Q
import logging
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'web/index.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created successfully!')
            return redirect('login')
    else:
        form = CreateUserForm()

    context = {'form':form}

    return render(request, 'web/register.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('dashboard')
    else:
        form = loginForm()

    context = {'form':form}

    return render(request, 'web/login.html', context)


@login_required(login_url='login')
def dashboard(request):
    records = Records.objects.all()
    return render(request, 'web/dashboard.html', context={'records':records})



def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required(login_url='login')
def create_record(request):
    form = CreateRecordForm()

    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record added successfully!')
            return redirect('dashboard')
    else:
        form = CreateRecordForm()

    context = {'form':form}

    return render(request, 'web/create_record.html', context=context)


@login_required(login_url='login')
def veiw_record(request, record_id):
    all_records = get_object_or_404(Records, id=record_id)
    context = {'record':all_records}

    return render(request, 'web/veiw_record.html', context)


@login_required(login_url='login')
def update_record(request, record_id):
    record = get_object_or_404(Records, id=record_id)
    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully!')
            return redirect('dashboard')
    else:
        form = UpdateRecordForm(instance=record)

    context = {'form':form}

    return render(request, 'web/update_record.html', context)


@login_required(login_url='login')
def delete_record(request, record_id):
    record = get_object_or_404(Records, id=record_id)
    record.delete()
    messages.success(request, 'Record deleted successfully!')
    return redirect('dashboard')



logger = logging.getLogger(__name__)

@login_required(login_url='login')
def search(request):
    query = request.POST.get('query')
    results = []
    try:
        if query:
            results = Records.objects.filter(Q(first_name__icontains=query) | Q(id__icontains=query))
    except Exception as e:
        logger.error(f"Error searching for query: {query} - {e}")

    return render(request, 'web/search.html', context={'results':results, 'query':query})



def page_404(request, exception):
    return render(request, 'web/404.html', status=404)

