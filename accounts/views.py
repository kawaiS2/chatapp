from django.shortcuts import render, redirect
from .forms import SignUpForm

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'account/signup.html', context)