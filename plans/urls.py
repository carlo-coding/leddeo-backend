from django.urls import path
from . import views

urlpatterns = [
  path("create-checkout-session", views.CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
  path("create-portal-session", views.CreatePortalSessionView.as_view(), name="create-portal-session"),
  path("webhook-suscriptions", views.SubscriptionWebhook.as_view(), name="webhook-suscription")
]