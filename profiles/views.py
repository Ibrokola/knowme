from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.forms.models import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect

from .models import Profile, UserJob
from matches.models import Match
from .forms import UserJobForm, ProfileForm
from likes.models import UserLike


User = get_user_model()






@login_required
def profile_user(request):
	if request.user.is_authenticated():
		user = get_object_or_404(User, username=request.user)
		profile, created = Profile.objects.get_or_create(user=user)
		jobs = user.userjob_set.all()
		template = "profiles/profile_user.html"
		context = {
				"profile": profile,
				"jobs": jobs,
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
	# else:
	# 	raise Http404





@login_required
def profile_view(request, username):
	if request.user.is_authenticated():
		user = get_object_or_404(User, username=username)
		profile, created = Profile.objects.get_or_create(user=user)
		user_like, user_like_created = UserLike.objects.get_or_create(user=request.user)
		do_i_like = False
		if user in user_like.liked_users.all():
			do_i_like = True
		mututal_like = user_like.get_mutual_like(user)
		# print(UserLike.objects.get_all_mutual_likes(request.user, 6))
		match, match_created = Match.objects.get_or_create_match(user_a=request.user, user_b=user)
		jobs = user.userjob_set.all()
		template = "profiles/profile_view.html"
		context = {
				"profile": profile,
				"match": match,
				"jobs": jobs,
				"mutual_like": mututal_like,
				"do_i_like": do_i_like,
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
	# else:
	# 	raise Http404



@login_required
def profile_edit(request):
	title = "Update your profile"
	profile, created = Profile.objects.get_or_create(user=request.user)
	form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		return redirect("profile_user")
	template = "profiles/forms.html"
	context = {
		# "form": form,
		"form": form,
		"title": title,
	}
	return render(request, template, context)




@login_required
def job_add(request):
	title = "Add Job"
	job = UserJob.objects.all()[0]
	form = UserJobForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		return redirect("profile_user")
	template = "profiles/forms.html"
	context = {
		# "form": form,
		"form": form,
		"title": title,
	}
	return render(request, template, context)



@login_required
# def job_edit(request, id):  individual edit
# job = UserJob.objects.get(id=id)
def job_edit(request):
	title = "Edit Jobs"
	UserJobFormset = modelformset_factory(UserJob, form=UserJobForm, extra=0)
	queryset = UserJob.objects.filter(user=request.user)
	formset = UserJobFormset(request.POST or None, queryset=queryset)

	if formset.is_valid():
		instances = formset.save(commit=False)
		for instance in instances:
			instance.user = request.user
			instance.save()
		return redirect("profile_user")	
	# form = UserJobForm(request.POST or None, instance=job)
	# if form.is_valid():
	# 	instance = form.save(commit=False)
	# 	instance.user = request.user
	# 	instance.save()
	template = "profiles/formset.html"
	context = {
		# "form": form,
		"formset": formset,
		"title": title,
	}
	return render(request, template, context)