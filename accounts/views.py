from django.shortcuts import render
from .forms import CustomUserCreationForm, CustomUserChangeForm

def new_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
    else:
        form = CustomUserCreationForm()
    return render(request, 'new_user_form.html', {'form':form})
