from django.shortcuts import render

# Create your views here.

#@login_required(login_url='/aep/login')
def index(request):
    return render(request, 'index.html', {'userInfo':'cure'})
