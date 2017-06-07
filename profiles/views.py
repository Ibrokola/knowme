from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Profile
from matches.models import Match

User = get_user_model()

@login_required
def profile_view(request, username):
	if request.user.is_authenticated():
		user = get_object_or_404(User, username=username)
		profile, created = Profile.objects.get_or_create(user=user)
		match, match_created = Match.objects.get_or_create_match(user_a=request.user, user_b=user)
		template = "profiles/profile_view.html"
		context = {
				"profile": profile,
				"match": match,
		}
		return render(request, template, context)
		# except ValueError:
		# 	user = get_object_or_404(User, username=username)
		# 	profile = Profile.objects.get_or_create(user=user)
		# 	match, match_created = Match.objects.get_or_create_match(user_a=request.user, user_b=user)
		# 	template = "profiles/profile_view.html"
		# 	context = {
		# 			"profile": profile,
		# 			"match": match,
		# 	}
		# 	return render(request, template, context)
	else:
		raise Http404