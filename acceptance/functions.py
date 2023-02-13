from .models import Acceptance, UserAcceptance


def save_acceptance(user, acceptance_id):
  acceptance = Acceptance.objects.filter(id=acceptance_id).first()
  UserAcceptance.objects.create(
    user=user,
    acceptance=acceptance,
    accepted=True,
  ).save()
  pass