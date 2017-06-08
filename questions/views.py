from django.http import Http404, HttpResponse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from jobs.models import Job, Employer, Location
from .models import Question, Answer, UserAnswer
from .forms import UserResponseForm

from matches.models import Match, PositionMatch, EmployerMatch, LocationMatch


def home(request):
	template = "questions/home.html"
	context = {}
	if request.user.is_authenticated():
		template = "questions/home.html"
		# matches = Match.objects.matches_all(request.user)
		queryset = Question.objects.all().order_by('-timestamp')
		context = {}
		return render(request, template, context)
	return render(request, template, context)


def dashboard_view(request):
	if request.user.is_authenticated():
		
		# PositionMatch.objects.update_top_suggestions(request.user, 20)
		matches = Match.objects.get_matches_with_percent(request.user)[:6]
		positions = PositionMatch.objects.filter(user=request.user)[:6]
		
		if positions.count() > 0:
			positions[0].check_update(20) #20 matches total
		locations = LocationMatch.objects.filter(user=request.user)[:6]
		employers = EmployerMatch.objects.filter(user=request.user)[:6]
		# for match in matches:
		# 	job_set = match[0].userjob_set.all()
		# 	if job_set.count() > 0:
		# 		for job in job_set:
		# 			if job.position not in positions:
		# 				positions.append(job.position)
		# 				try:
		# 					the_job = Job.objects.get(text__iexact=job.position)
		# 					jobmatch, created = PositionMatch.objects.get_or_create(user=request.user, job=the_job)
		# 				except:
		# 					pass
		# 					print(PositionMatch.objects.filter(user=request.user))
		# 			if job.location not in locations:
		# 				locations.append(job.location)
		# 				try:
		# 					the_loc = Location.objects.get(text__iexact=job.location)
		# 					locmatch, created = LocationMatch.objects.get_or_create(user=request.user, location=the_loc)
		# 					print(locmatch)
		# 				except:
		# 					pass
							
		# 			if job.employer_name not in employers:
		# 				employers.append(job.employer_name)
		# 				try:
		# 					the_employer = Employer.objects.get(text__iexact=job.employer_name)
		# 					employermatch, created = EmployerMatch.objects.get_or_create(user=request.user, employer=the_employer)
		# 					print(employermatch)
		# 				except:
		# 					pass
							




		queryset = Question.objects.all().order_by('-timestamp')
		template = "questions/dashboard.html"
		context = { 	
				'queryset': queryset,
				'matches': matches,
				'positions': positions,
				'locations': locations,
				'employers': employers,
			}
		return render(request, template, context)
	else:
		raise Http404


def single(request, id):
	if request.user.is_authenticated():
		queryset = Question.objects.all().order_by('timestamp')
		instance = get_object_or_404(Question, id=id)
		try:
			user_answer = UserAnswer.objects.get(user=request.user, question=instance)
		except UserAnswer.DoesNotExist:
			user_answer = UserAnswer()
		except UserAnswer.MultipleObjectsReturned:
			user_answer = UserAnswer.objects.filter(user=request.user, question=instance)[0]
		except:
			user_answer = UserAnswer()

		form = UserResponseForm(request.POST or None)
		if form.is_valid():
			# print(form.cleaned_data)
			# print(request.POST)
			question_id = form.cleaned_data.get('question_id')
			answer_id = form.cleaned_data.get('answer_id')
			importance_level = form.cleaned_data.get('importance_level')

			their_answer_id = form.cleaned_data.get('their_answer_id')	
			their_importance_level = form.cleaned_data.get('their_importance_level')

			question_instance = Question.objects.get(id=question_id)
			answer_instance = Answer.objects.get(id=answer_id)
			
			user_answer.user = request.user
			user_answer.question = question_instance
			user_answer.my_answer = answer_instance
			user_answer.my_answer_importance = importance_level
			if their_answer_id != -1:
				their_answer_instance = Answer.objects.get(id=their_answer_id)
				user_answer.their_answer = their_answer_instance
				user_answer.their_answer_importance = their_importance_level
			else:
				user_answer.their_answer = None
				user_answer.their_answer_importance = 'Not Important'
			user_answer.save()

			next_q = Question.objects.all().order_by("?").first()
			return redirect("question_single", id=next_q.id)


		template = "questions/single.html"
		context = {
			# "question": queryset,
			"form": form,
			"instance":instance,
			"user_answer": user_answer,
		}
		return render(request, template, context)
	else:
		raise Http404




def create_view(request):
	if request.user.is_authenticated():
		form = UserResponseForm(request.POST or None)
		if form.is_valid():
			print(form.cleaned_data)
			question_id = form.cleaned_data.get('question_id')
			answer_id = form.cleaned_data.get('answer_id')
			question_instance = Question.objects.get(id=question_id)
			answer_instance = Answer.objects.get(id=answer_id)
			print(question_instance.text, answer_instance.text)
		queryset = Question.objects.all().order_by('-timestamp')
		instance = queryset[1]
		template = "questions/questions.html"
		context = {
			# "question": queryset,
			"form": form,
			"instance":instance
		}
		return render(request, template, context)
	else:
		raise Http404