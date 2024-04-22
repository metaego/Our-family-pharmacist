from django.shortcuts import render

# Create your views here.
def home_main(request):
    return render(request, 'main.html')