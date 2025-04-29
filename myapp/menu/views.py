from django.shortcuts import render

def home(request):
    return render(request, 'menu/home.html')

def blog(request):
    return render(request, 'menu/blog.html')

def about(request):
    return render(request, 'menu/about.html')

def page1(request):
    return render(request, 'menu/page1.html')

def page2(request):
    return render(request, 'menu/page2.html')