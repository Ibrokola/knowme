from django.http import Http404, HttpResponse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from jobs.models import Job, Employer, Location
from questions.models import Question, Answer, UserAnswer
from questions.forms import UserResponseForm

from likes.models import UserLike

from questions.forms import UserResponseForm

from matches.models import Match, PositionMatch, EmployerMatch, LocationMatch



# def home(request):
# 	template = "dashboard/home.html"
# 	context = {}
# 	if request.user.is_authenticated():
# 		template = "dashboard/home.html"
# 		# matches = Match.objects.matches_all(request.user)
# 		queryset = Question.objects.all().order_by('-timestamp')
# 		context = {}
# 		return render(request, template, context)
# 	return render(request, template, context)



#dashboard view
def dashboard_view(request):
	if request.user.is_authenticated():
		PositionMatch.objects.update_top_suggestions(request.user, 20)
		matches = Match.objects.get_matches_with_percent(request.user)[:6]
		positions = PositionMatch.objects.filter(user=request.user)[:6]
		if positions.count() > 0:
			positions[0].check_update(20) #20 matches total
		locations = LocationMatch.objects.filter(user=request.user)[:6]
		employers = EmployerMatch.objects.filter(user=request.user)[:6]
		mutual_likes = UserLike.objects.get_all_mutual_likes(request.user, 6)

		new_user = False
		if len(mutual_likes) == 0 and len(matches) == 0:
			new_user = True

		question_instance = None
		queryset = Question.objects.get_unanswered(request.user).order_by('-timestamp')

		if queryset.count() > 0:
			question_instance = queryset.order_by('?').first()

		question_form = UserResponseForm()
		template = "dashboard/dashboard.html"
		context = { 	
				'queryset': queryset,
				'matches': matches,
				'positions': positions,
				'locations': locations,
				'employers': employers,
				'mutual_likes': mutual_likes,
				'new_user': new_user,
				'question_form': question_form,
				'question_instance': question_instance,
			}
		return render(request, template, context)
	template = "dashboard/home.html"
	context = {}
	return render(request, template, context)