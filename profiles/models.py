from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, pre_save

User = settings.AUTH_USER_MODEL


def upload_location(instance, filename):
	# extension = fielname.split(".")[1]
	location = str(instance.user.username)
	return "%s/%s" %(location, filename)


class Profile(models.Model):
	user = models.OneToOneField(User)
	location = models.CharField(max_length=120, null=True, blank=True)
	picture = models.ImageField(upload_to=upload_location, null=True, blank=True)
	description = models.TextField()

	def __str__(self):
		return self.user.username


	def get_absolute_url(self):
		url = reverse("profile", kwargs={"username": self.user.username})
		return url


	def like_link(self):
		url = reverse("like_user", kwargs={"id": self.user.id})
		return url



class UserJob(models.Model):
	user = models.ForeignKey(User)
	position = models.CharField(max_length=220)
	location = models.CharField(max_length=220)
	employer_name = models.CharField(max_length=220)


	def __str__(self):
		return self.position



from jobs.models import Location, Job, Employer

def post_save_user_job(sender, instance, created, *args, **kwargs):
	job = instance.position.lower()
	location = instance.location.lower()
	employer_name = instance.employer_name.lower()
	new_job = Job.objects.get_or_create(text=job)
	new_location, created = Location.objects.get_or_create(name=location)
	new_employer = Employer.objects.get_or_create(location=new_location, name=employer_name)


post_save.connect(post_save_user_job, sender=UserJob) 