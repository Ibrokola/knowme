import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

from .utils import get_points, get_match

class MatchManager(models.Manager):
	def get_or_create_match(self, user_a=None, user_b=None):
		try:
			obj = self.get(user_a=user_a, user_b=user_b)
		except:
			obj = None
		try:
			obj_2 = self.get(user_a=user_b, user_b=user_a)
		except:
			obj_2 = None

		if obj and not obj_2:
			obj.check_update()
			return obj, False
		elif not obj and obj_2:
			obj_2.check_update()
			return obj_2, False
		else:
			new_instance = self.create(user_a=user_a, user_b=user_b)
			new_instance.do_match()
			return new_instance, True


class Match(models.Model):
	user_a = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='match_user_a')
	user_b = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='match_user_b')
	match_decimal = models.DecimalField(decimal_places=8, max_digits=12, default=0.00)
	questions_answered = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return "%.2f" %(self.match_decimal)

	objects = MatchManager()


	def do_match(self):
		user_a = self.user_a
		user_b = self.user_b
		match_decimal, questions_answered = get_match(user_a, user_b)
		match_decimal = self.match_decimal
		questions_answered = self.questions_answered
		self.save()

	def check_update(self):
		now = timezone.now()
		offset = now - datetime.timedelta(hours=12)
		if self.updated <= offset:
			self.do_match()
		else:
			print("already updated")