from django.shortcuts import render
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

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
			# messages.success(request, f'Account has been created! You can now login.')
			# return redirect('/')


			login(self.request, user)
			messages.success(
				self.request,
				(
					f'Thank You For Creating A Bank Account. '
                    # f'Your Account Number is {user}. '
				)
			)
			return HttpResponseRedirect(
				reverse_lazy('transactions:deposit_money')
			)


	else:
		form = UserRegisterForm()

	return render(request, 'user_registration.html', {'form': form})


class UserLoginView(LoginView):
    template_name='user_login.html'
    redirect_authenticated_user = True


class LogoutView(RedirectView):
    pattern_name = 'home-page'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
