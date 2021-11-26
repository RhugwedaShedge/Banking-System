from django.shortcuts import render
from .forms import UserRegisterForm

# Create your views here.

def home(request):
    return render(request, 'index.html', {})


def registerpage_view(request):

	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()

			username = form.cleaned_data.get('username')
			# user = request.user
			# print(user)
			# customer = Customer.objects.create(user = username.id)
			# print(customer)
			messages.success(request, f'Account has been created! You can now login.')
			return redirect('/farmers/login/')
	else:
		form = UserRegisterForm()

	return render(request, 'user_registration.html', {'form': form})
