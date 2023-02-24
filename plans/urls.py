from django.urls import path
from . import views

urlpatterns = [
  path("create-checkout-session", views.CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
  path("create-portal-session", views.CreatePortalSessionView.as_view(), name="create-portal-session"),
  path("webhook-suscriptions", views.SubscriptionWebhook.as_view(), name="webhook-suscription"),
  path("prices", views.GetPricesView.as_view(), name="Get prices"),
  path("invoices", views.GetInvoicesView.as_view(), name="Get invoices"),
  path("", views.HandleSubscription.as_view(), name="Cancel subscription")
]