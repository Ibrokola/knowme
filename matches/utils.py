from decimal import Decimal
from django.contrib.auth import get_user_model
from questions.models import UserAnswer


# User = get_user_model()
# users = User.objects.all() #[user1, user2]


# all_user_answers = UserAnswer.objects.all().order_by("user__id")

# ibro = users[0]
# babajide = users[1]

# userc = users[2]
# userd = users[3]

# UserAnswer.objects.filter(user=ibro)
# UserAnswer.objects.filter(user=babajide)

# ians = ibro.useranswer_set.all()[0]
# bans = babajide.useranswer_set.all()[0]


def get_points(user_a, user_b):
	a_answers = UserAnswer.objects.filter(user=user_a)
	b_answers = UserAnswer.objects.filter(user=user_b)
	a_total_awarded = 0
	a_points_possible = 0
	num_question = 0
	for a in a_answers:
		for b in b_answers:
			if a.question.id == b.question.id:
				num_question += 1
				a_pref = a.their_answer
				b_answer = b.my_answer
				if a_pref == b_answer:
					a_total_awarded == a.their_points
				a_points_possible += a.their_points
			print("%s has awarded %s points of %s to %s" %(user_a, a_total_awarded, a_points_possible, user_b))
	percent = a_total_awarded / Decimal(a_points_possible)
	print(percent)
	if percent == 0:
		percent = 0.000001
	return percent, num_question



# a = get_points(ibro, userd)
# b = get_points(babajide, userd)
# c = get_points(userd, babajide)
# # get_points(userc, userd)
# # get_points(userd, userc)


# match_percentage = "%.2f" %(Decimal(a[0]) * Decimal(b[0])) ** (1/Decimal(b[1]))
# print(match_percentage)



def get_match(user_a, user_b):
	a = get_points(user_a, user_b)
	b = get_points(user_a, user_b)
	number_of_questions = b[1]
	match_decimal = (Decimal(a[0]) * Decimal(b[0])) ** (1/Decimal(number_of_questions))
	return match_decimal, number_of_questions