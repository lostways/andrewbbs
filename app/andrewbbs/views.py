from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Screen
from .models import AccessCode
from .models import Member
from .forms import AccessCodeForm
from .forms import MemberForm
from .forms import LoginForm
from .forms import OTPForm
from .auth.verify import OTP

User = get_user_model()

# Create your views here.
def index(request):
    """Screen List"""

    # Unlocked codes set by AccessCodeMiddleware
    codes = request.unlocked_codes
    
    if codes:
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
    """Screen Detail"""

    # Unlocked codes set by AccessCodeMiddleware
    codes = request.unlocked_codes

    if codes:
        screen = Screen.objects.filter(slug=slug, codes__code__in=codes).distinct()
        screen = get_object_or_404(screen)
    else:
        # if no codes return 404
        raise Http404("No codes unlocked")

    context = {
        'screen': screen,
        'page_title': screen.title
    }
    return render(request, 'screens/screen_detail.html', context)

def access(request):
    """Enter Access Code"""

    # Unlocked codes set by AccessCodeMiddleware
    codes = request.unlocked_codes

    form = AccessCodeForm(request.POST or None)

    if form.is_valid():
        entered_code = form.cleaned_data['code']

        try:
            valid_code = AccessCode.objects.get(
                code=entered_code,
                enabled=True
            )
        except AccessCode.DoesNotExist:
            valid_code = None

        if valid_code and valid_code.has_screens():
            # add code if not already in codes
            if entered_code not in codes:
                codes.append(entered_code)

            #print (f"code: {entered_code} is valid")

            #if user is logged in, add code to unlocked_codes
            if request.user.is_authenticated:
                member = Member.objects.get(handle=request.user.handle)
                member.unlocked_codes = codes
                member.save()
            else:
                request.session['codes'] = codes

            return redirect("screen-list")
        else:
            messages.error(request, "Invalid Code")

    context = {
        'form':form,
        'page_title': "Enter Access Code"
    }
    return render(request, 'access.html', context)

def member_register(request):
    """Register as a member"""

    # if user is logged in or no codes are unlocked redirect to index
    if request.user.is_authenticated or request.unlocked_codes == []:
        return redirect("screen-list")

    form = MemberForm(request.POST or None)

    if form.is_valid():
        member = form.save(commit=False)

        # set unsable password
        member.set_unusable_password()

        # add codes in session to unclocked_codes
        member.unlocked_codes = request.session.get('codes', [])
        
        # save member
        member.save()

        context = {
            'member': member,
            'page_title': 'Login as a Member'
        }
        return redirect('member-login')

    context = {
        'form':form,
        'page_title': "Register as a Member"
    }
    return render(request, 'members/register.html', context)

def member_login(request):
    """Login as a member"""

    form = LoginForm(request.POST or None)

    if form.is_valid():
        handle = form.cleaned_data.get('handle')
        try:
            member = Member.objects.get(handle=handle)
            OTP.send_code(member.phone.as_e164)
            return redirect("/members/otp/{}".format(member.pk))
        except Member.DoesNotExist:
            messages.error(request, "Handle not found")

    context = {
        'form':form,
        'page_title': "Login as a Member"
    }
    return render(request, 'members/login.html', context)

def member_login_verify(request, pk):
    """Request OTP"""

    valid = ""

    form = OTPForm(request.POST or None)

    if form.is_valid():
        code = form.cleaned_data.get('code')
        member = Member.objects.get(pk=pk)
        otp_status = OTP.verify_code(member.phone.as_e164, code)
        if otp_status == "approved":
            valid = "True"
            user = authenticate(request, handle=member.handle)
            if user is not None:
                login(request, user, backend='andrewbbs.auth.member_backend.MemberBackend')
                return redirect("/")
            else:
                messages.error(request, "Invalid code")
        else:
            valid = otp_status
            messages.error(request, "Invalid code")

    context = {
        'form':form,
        'valid': valid,
        'pk': pk,
        'page_title': "Enter Authentication Code"
    }

    return render(request, 'members/verify.html', context)

def member_logout(request):
    """Logout Member"""

    logout(request)
    return redirect("/")