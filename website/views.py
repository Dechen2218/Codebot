from django.shortcuts import render, redirect
from django.contrib import messages
import openai
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code

# Create your views here.
def home(request):
	# API = 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
	lang_list = ['asharp', 'c', 'css', 'django', 'go', 'html', 'javascripts', 'markup', 'mongodb', 'perl', 'php', 'powershell', 'python', 'regex', 'ruby', 'rust', 'sql', 'yaml']
	
	if request.method == "POST":
		code = request.POST['code']
		lang = request.POST['lang']
	
        # check to make sure to select the language
		if lang == "Select Programming Language":
			messages.success(request, 'hey! you have forgot to enter language')
			return render(request, 'home.html', {'lang_list': lang_list, 'response':code, 'code':code, 'lang':lang})
		else:   	
          # OPENAI!!!
			openai.api_key = "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"
			# create openai Instance
			openai.Model.list()
			# make an openai request

			try:
				response = openai.Completion.create(
					engine = 'text-davinci-003',
					prompt = f"Response only with code. Fix this {lang} code: {code}",
	                temperature = 0,
	                max_tokens = 1000,
	                top_p = 1.0,
	                frequency_penalty = 0.0,
	                presence_penalty = 0.0,

					)
				response = (response["choices"][0]["text"]).strip()
				 # save to database
				record = Code(question = code, code_answer=response, language=lang, user=request.user)
				record.save()

				return render(request, 'home.html', {'lang_list':lang_list, 'response':response, 'lang':lang})

			except Exception as e:
				return render(request, 'home.html', {'lang_list':lang_list, 'response':e, 'lang':lang})
    

	return render(request, 'home.html', {'lang_list':lang_list})


def suggest(request):
	lang_list = ['asharp', 'c', 'css', 'django', 'go', 'html', 'javascripts', 'markup', 'mongodb', 'perl', 'php', 'powershell', 'python', 'regex', 'ruby', 'rust', 'sql', 'yaml']
	
	if request.method == "POST":
		code = request.POST['code']
		lang = request.POST['lang']
	
        # check to make sure to select the language
		if lang == "Select Programming Language":
			messages.success(request, 'hey! you have forgot to enter language')
			return render(request, 'home.html', {'lang_list': lang_list, 'response':code, 'code':code, 'lang':lang})
		else:   	
          # OPENAI!!!
			openai.api_key = "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"
			# create openai Instance
			openai.Model.list()
			# make an openai request

			try:
				response = openai.Completion.create(
					engine = 'text-davinci-003',
					prompt = f"Response only with code. Fix this  code: {code}",
	                temperature = 0,
	                max_tokens = 1000,
	                top_p = 1.0,
	                frequency_penalty = 0.0,
	                presence_penalty = 0.0,

					)
				# parse the response
				response = (response["choices"][0]["text"]).strip()
				 # save to database
				record = Code(question = code, code_answer=response, Language=lang, user=request.user)
				record.save()

				return render(request, 'suggest.html', {'lang_list':lang_list, 'response':response, 'lang':lang})
                # save to database
               
			except Exception as e:
				return render(request, 'suggest.html', {'lang_list':lang_list, 'response':e, 'lang':lang})
    

	return render(request, 'suggest.html', {'lang_list':lang_list})


def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!  Woohoo!")
			return redirect('home')
		else:
			messages.success(request, "Error Logging In. Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out... Have A Nice Day!")
	return redirect('home')


def register_user(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Registered...Congrats!!")
			return redirect('home')

	else:
		form = SignUpForm()

	return render(request, 'register.html', {"form": form})


def past(request):
	if request.user.is_authenticated:
		code = Code.objects.filter(user_id=request.user.id)
		return render(request, 'past.html', {"code":code})
	else:
		messages.success(request, "You must be logged in to view this page")
		return redirect('home')


def delete_past(request, Past_id):
	past = Code.objects.get(pk=Past_id)
	past.delete()
	messages.success(request, "Deleted Successfully...")
	return redirect('past')