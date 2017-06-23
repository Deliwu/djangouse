from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            response = redirect(request.GET.get('next', '/'))
            return response
        else:
            return HttpResponse('Error', status=401)
    else:
        if request.user.is_authenticated:
            request.session['color'] = 'red'
            session = ','.join(request.session.keys())
            response = HttpResponse('session: %s' % session)
            response.set_cookie('color', 'redhat')
            return response
        return render(request,'days/login.html')


def logout_viw(request):
    logout(request)
    return redirect('days:login')


@login_required
def index(request):
    return HttpResponse('This is index!')
