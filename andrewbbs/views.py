from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Screen
from .models import AccessCode
from .models import Member
from .forms import AccessCodeForm
from .forms import MemberForm
from .forms import LoginForm
from .forms import OTPForm
from .auth.verify import OTP

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

            # add codes in session to unclocked_codes
            member.unlocked_codes = request.session.get('codes', [])
            member.save()

            context = {
                'member': member,
                'page_title': 'Thank You'
            }
            return render(request, 'members/login.html', context)
    else:
        form = MemberForm()

    context = {
        'form':form,
        'page_title': "Register as a Member"
    }
    return render(request, 'members/register.html', context)

def member_login(request):
    """Login as a member"""

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            handle = form.cleaned_data.get('handle')
            try:
                member = Member.objects.get(handle=handle)
                OTP.send_code(member.phone.as_e164)
                return redirect("/members/otp/{}".format(member.pk))
            except Member.DoesNotExist:
                messages.error(request, "Handle not found")

            context = {
                'member': member,
                'page_title': 'Thank You'
            }
            return redirect("screen-list")
    else:
        form = LoginForm()

    context = {
        'form':form,
        'page_title': "Login as a Member"
    }
    return render(request, 'members/login.html', context)

def member_otp(request, pk):
    """Request OTP"""
    valid = ""
    if request.method == 'POST':
        form = OTPForm(data=request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            member = Member.objects.get(pk=pk)
            otp_status = OTP.verify_code(member.phone.as_e164, code)
            if otp_status == "approved":
                valid = "True"
                user = authenticate(request, handle=member.handle)
                if user is not None:
                    login(request, member, backend='andrewbbs.auth.member_backend.MemberBackend')
                    return redirect("/")
            else:
                valid = otp_status
                #messages.error(request, "Invalid code")

    form = OTPForm()
    context = {
        'form':form,
        'valid': valid,
        'pk': pk,
        'page_title': "Enter Authentication Code"
    }
    return render(request, 'members/otp.html', context)