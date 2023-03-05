from rest_framework import permissions
from plans.models import Plan
from commons.utils import is_valid_plan

class ReadonlyIfNotAdmin(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    else:
      return (request.user.is_authenticated and request.user.is_staff)


class CustomerHasPlan(permissions.BasePermission):
  def has_permission(self, request, view):
    for plan in Plan.objects.filter(user=request.user):
      if is_valid_plan(plan):
        return True
    if request.user.is_staff or request.user.is_superuser:
      return True
    return False