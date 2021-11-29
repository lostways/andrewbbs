from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Screen
from .models import AccessCode
from .forms import AccessCodeForm

# Create your views here.
def index(request):
    queryset = Screen.objects.all().order_by("-created_at")
    context = {'screen_list': queryset}
    return render(request, 'screens/screen_list.html', context)

def detail(request, slug):
    screen = get_object_or_404(Screen, slug=slug)
    return render(request, 'screens/screen_detail.html', {'screen': screen})

def access(request):
    """Enter Access Code"""
    msg = "Initial"
    if request.method == 'POST':
        form = AccessCodeForm(data=request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']
            if AccessCode.objects.filter(
                code=entered_code,
                valid=True
            ).exists():
                codes = request.session.get('codes', [])
                codes.append(entered_code)
                request.session['codes'] = list(set(codes))

    form = AccessCodeForm()
    msg = repr(request.session.get('codes',[]))
    context = {'form':form, 'msg': msg}
    return render(request, 'access.html', context)
