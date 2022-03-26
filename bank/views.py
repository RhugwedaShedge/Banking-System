from django.shortcuts import render
from .forms import UserRegisterForm, TransactionForm, OTPForm
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

	if request.user.is_authenticated:
		useracc = UserBankAccount.objects.get(user = request.user)
	
		return render(request, 'index.html', {'useracc':useracc})
	else:
		return render(request, 'index.html')


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
			user.save()
			print("user.otp: ", user.otp)

			return HttpResponseRedirect(
				reverse_lazy('verify-otp')
			)


	else:
		form = UserRegisterForm()

	return render(request, 'user_registration.html', {'form': form})


def verify_otp(request):
	form = OTPForm()
	if request.method=='POST':
		form = OTPForm(request.POST)
		if form.is_valid():
			otp = form.cleaned_data.get('verifyOTP')
			print("otp: ", otp)
			print("otp: ", type(otp))


			user = UserBankAccount.objects.get(user = request.user)

			print("user.otp: ", user.otp)
			print("user.otp: ", type(user.otp))

			if otp == user.otp:

				user.is_mobile_verified = True
				user.save()

				logout(request)
				messages.success(
					request,
					(
						f'Thank You For Linking Your Bank Account. '
					)
				)
				return HttpResponseRedirect(
					reverse_lazy('user_login')
				)
			else:
				messages.error(
					request,
					(
						f'Your OTP is wrong.'
					)
				)

	else:
		form = OTPForm()
	
	return render(request, 'otp_verification.html', {'form': form})



class UserLoginView(LoginView):
    template_name='user_login.html'
    redirect_authenticated_user = True


class LogoutView(RedirectView):
    pattern_name = 'home-page'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

	
def TransactionView(request):

	if request.user.is_authenticated:

		user = UserBankAccount.objects.get(user = request.user)

		if request.method == 'POST':

			form = TransactionForm(request.POST)
			if form.is_valid():
				trans = form.save(commit=False)
				trans.userAccount = user
				trans.save()

				amount = form.cleaned_data.get('amount')
				user.balance -= amount

				payeeAccount = form.cleaned_data.get('payeeAccount')
				payeeuser = UserBankAccount.objects.get(account_no = payeeAccount)
				payeeuser.balance += amount
				payeeuser.save()
				user.save()
		else:
			form = TransactionForm()

	return render(request, 'transaction_form.html', {'form': form})


def TransactionReport(request):

	if request.user.is_authenticated:
		user = UserBankAccount.objects.get(user = request.user)
		accounts = UserBankAccount.objects.all() 

		transactions = Transaction.objects.filter(userAccount=user)

		context = {
			'transactions': transactions,
			'bankuser': user,
			'accounts': accounts
		}
	else:
		context = {}

	return render(request, 'transaction_report.html', context)

