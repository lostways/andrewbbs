from django.shortcuts import render, redirect, get_object_or_404
from .models import Screen
from .models import AccessCode
from .forms import AccessCodeForm
from .forms import MemberForm

# Create your views here.
def index(request):
    if 'codes' in request.session:
        codes = request.session['codes'] 
        screens = Screen.objects.filter(
            codes__code__in=codes,
        ).distinct().order_by("-updated_at")

        if screens:
            screen_ids = [screen.pk for screen in screens]
            unlocked_screens = request.session.get('screens', [])
            for screen_id in screen_ids:
                unlocked_screens.append(screen_id)
            request.session['screens'] = list(set(unlocked_screens))

        context = {
            'screen_list': screens,
            'page_title': "Sreens"
        }
        return render(request, 'screens/screen_list.html', context)

    return access(request)

def detail(request, slug):
    codes = request.session.get('codes', [])
    screen = Screen.objects.filter(slug=slug, codes__code__in=codes).distinct()
    screen = get_object_or_404(screen)

    context = {
        'screen': screen,
        'page_title': screen.title
    }
    return render(request, 'screens/screen_detail.html', context)

def access(request):
    """Enter Access Code"""

    codes = request.session.get('codes', [])
    screens = request.session.get('screens', [])

    msg = repr(codes) + repr(screens)

    if request.method == 'POST':
        form = AccessCodeForm(data=request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']

            try:
                valid_code = AccessCode.objects.get(
                    code=entered_code,
                    enabled=True
                )
            except AccessCode.DoesNotExist:
                valid_code = None

            if valid_code:
                codes.append(entered_code)
                request.session['codes'] = list(set(codes))

                if valid_code.has_screens():
                    return redirect("screen-list")

    form = AccessCodeForm()
    context = {
        'form':form,
        'msg': msg,
        'page_title': "Enter Access Code"
    }
    return render(request, 'access.html', context)

def member_register(request):
    """Register as a member"""

    if request.method == 'POST':
        form = MemberForm(data=request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            return redirect("screen-list")
    else:
        form = MemberForm()

    context = {
        'form':form,
        'page_title': "Register as a Member"
    }
    return render(request, 'members/register.html', context)


