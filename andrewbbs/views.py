from django.shortcuts import render, get_object_or_404
from .models import Screen

# Create your views here.
def index(request):
    queryset = Screen.objects.all().order_by("-created_at")
    context = {'screen_list': queryset}
    return render(request, 'screens/screen_list.html', context)

def detail(request, slug):
    screen = get_object_or_404(Screen, slug=slug)
    return render(request, 'screens/screen_detail.html', {'screen': screen})
