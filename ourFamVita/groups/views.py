from django.shortcuts import render

# Create your views here.
def group_main(request):
    return render(request, 'group/main.html')

def group_detail(request):
    return render(request, 'group/detail.html')
