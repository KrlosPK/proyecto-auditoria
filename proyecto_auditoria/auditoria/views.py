from django.shortcuts import render


# Create your views here.
def controles(request):
    return render(request, "controles.html", {})
