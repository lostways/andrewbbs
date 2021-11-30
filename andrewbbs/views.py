from django.shortcuts import render, redirect, get_object_or_404
from .models import Screen
from .models import AccessCode
from .forms import AccessCodeForm

# Create your views here.
def index(request):
    if 'codes' in request.session:
        codes = request.session['codes'] 
        screens = Screen.objects.filter(
            codes__code__in=codes,
            codes__valid=True
        ).distinct().order_by("-updated_at")

        context = {
            'screen_list': screens,
            'page_title': "Sreens"
        }
        return render(request, 'screens/screen_list.html', context)
    else:
        return access(request)

def detail(request, slug):
    screen = get_object_or_404(Screen, slug=slug)
    context = {
        'screen': screen,
        'page_title': screen.title
    }
    return render(request, 'screens/screen_detail.html', context)

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
                return redirect("screen-list")

    form = AccessCodeForm()
    msg = repr(request.session.get('codes',[]))
    context = {
        'form':form,
        'msg': msg,
        'page_title': "Enter Access Code"
    }
    return render(request, 'access.html', context)
