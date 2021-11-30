from django.shortcuts import render
from .forms import UserRegisterForm, TransactionForm
from .models import *

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helpers import send_otp_to_phone

# Create your views here.

def home(request):
    return render(request, 'index.html', {})


def registerpage_view(request):

	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			
			# username = form.cleaned_data.get('username')
			
			# user = request.user
			# print(user)
			# customer = Customer.objects.create(user = username.id)
			# print(customer)
			# messages.success(request, f'Account has been created! You can now login.')
			# return redirect('/')			

			login(request, user)

			user = UserBankAccount.objects.get(user = request.user)
			mobile_no = form.cleaned_data.get('mobile_no')
			mobile_no = str(mobile_no)
			user.otp = send_otp_to_phone(mobile_no)
			print("user.otp: ", user.otp)
			user.save()

			return HttpResponseRedirect(
				reverse_lazy('verify-otp')
			)


	else:
		form = UserRegisterForm()

	return render(request, 'user_registration.html', {'form': form})


def verify_otp(request):
	data = request.data
	user = UserBankAccount.objects.get(user = request.user)

	if data == user.otp:

		messages.success(
			request,
			(
				f'Thank You For Linking Your Bank Account. '
			)
		)

		return HttpResponseRedirect(
			reverse_lazy('home-page')
		)



class UserLoginView(LoginView):
    template_name='user_login.html'
    redirect_authenticated_user = True


class LogoutView(RedirectView):
    pattern_name = 'home-page'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


# @api_view(['POST'])
# def send_otp(request):
# 	data = request.data

# 	if data.get('mobile_no') is None:
# 		return Response({
# 			'status': 400,
# 			'message': 'key mobile_no is required'
# 		})

	# if data.get('password') is None:
	# 	return Response({
	# 		'status': 400,
	# 		'message': 'key password is required'
	# 	})

	# user = UserBankAccount.objects.create(
	# 	mobile_no = data.get('mobile_no'),
	# 	otp = send_otp_to_phone(data.get('mobile_no'))
	# )

	# # user.set_password = data.get('set_password')
	# user.save()

	# return Response({
	# 	'status': 200,
	# 	'message': 'Otp sent'
	# })

	
def TransactionView(request):

	if request.user.is_authenticated:

		user = UserBankAccount.objects.get(user = request.user)

		if request.method == 'POST':

			# candidate = form.save(commit=False)
			# candidate.user = UserProfile.objects.get(user=self.request.user)  # use your own profile here
			# candidate.save()


			form = TransactionForm(request.POST)
			if form.is_valid():
				trans = form.save(commit=False)
				trans.userAccount = user
				trans.save()

				amount = form.cleaned_data.get('amount')
				user.balance -= amount
				user.save()
				
		else:
			form = TransactionForm()

	return render(request, 'transaction_form.html', {'form': form})

		