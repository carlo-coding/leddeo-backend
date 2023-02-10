from rest_framework.views import APIView
from rest_framework.response import Response
from commons.utils import utc_to_date_string
from .models import Plan
from account.models import UserInfo, User
import stripe
from ledeo.settings import (
  stripe_key, 
  checkout_cancel_url, 
  checkout_success_url, 
  stripe_portal_return_url,
)

stripe.api_key = stripe_key
class CreateCheckoutSessionView(APIView):

  def post(self, request):
    lookup_key=request.data.get("lookup_key")
    customer_id=request.data.get("customer_id")
    prices = stripe.Price.list(
      lookup_keys=[lookup_key],
      expand=['data.product']
    )
    checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': prices.data[0].id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=checkout_success_url,
            cancel_url=checkout_cancel_url,
            customer=customer_id,
        )
    return Response({
      "url": checkout_session.url
    })

class CreatePortalSessionView(APIView):
  def post(self, request):
    checkout_session_id = request.data.get("session_id", "")
    if checkout_session_id:
      checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
      portalSession = stripe.billing_portal.Session.create(
          customer=checkout_session.customer,
          return_url=stripe_portal_return_url
      )
      return Response({
        "url": portalSession.url
      })
    
    customer_id = request.data.get("customer_id", "")
    if not customer_id:
      return Response({"message": "session_id or customer_id were not provided"})
    portalSession = stripe.billing_portal.Session.create(
      customer=customer_id,
      return_url=stripe_portal_return_url
    )
    return Response({
      "url": portalSession.url
    })


class SubscriptionWebhook(APIView):
  def post(self, request):
    event = request.data
    payload = request.data

    if event['type'] == 'customer.subscription.created':
      data = payload["data"]["object"]
      subscription = data["items"]["data"][0]

      product = stripe.Product.retrieve(subscription["plan"]["product"])

      userInfo = UserInfo.objects.filter(customer_id=data.get("customer")).first()
      user = User.objects.filter(id=userInfo.user_id).first()
      plan = Plan(
        user=user,
        stripe_subscription_id=data.get("id"),
        stripe_plan_id=subscription.get("subscription"),
        active=subscription["plan"].get("active"),
        name=product["name"],
        billing_cycle_anchor=utc_to_date_string(data.get("billing_cycle_anchor")),
        start_date=utc_to_date_string(data.get("start_date")),
        trial_start=utc_to_date_string(data.get("trial_start")),
        trial_end=utc_to_date_string(data.get("trial_end")),
        current_period_end=utc_to_date_string(data.get("current_period_end")),
        current_period_start=utc_to_date_string(data.get("current_period_start")),
        cancel_at=utc_to_date_string(data.get("cancel_at")),
        canceled_at=utc_to_date_string(data.get("canceled_at")),
        ended_at=utc_to_date_string(data.get("ended_at")),
      )
      plan.save()
      return Response({"message": "suscription created"}, status=200)

    if event['type'] == 'customer.subscription.updated':
      data = payload["data"]["object"]
      subscription = data["items"]["data"][0]

      product = stripe.Product.retrieve(subscription["plan"]["product"])

      plan = Plan.objects.filter(stripe_subscription_id=data.get("id")).first()
      if not plan:
        return Response({"message": "plan not found"}, status=400)
      plan.stripe_plan_id = subscription.get("subscription")
      plan.active=subscription["plan"].get("active")
      plan.name=product["name"]
      plan.billing_cycle_anchor=utc_to_date_string(data.get("billing_cycle_anchor"))
      plan.start_date=utc_to_date_string(data.get("start_date"))
      plan.trial_start=utc_to_date_string(data.get("trial_start"))
      plan.trial_end=utc_to_date_string(data.get("trial_end"))
      plan.current_period_end=utc_to_date_string(data.get("current_period_end"))
      plan.current_period_start=utc_to_date_string(data.get("current_period_start"))
      plan.cancel_at=utc_to_date_string(data.get("cancel_at"))
      plan.canceled_at=utc_to_date_string(data.get("canceled_at"))
      plan.ended_at=utc_to_date_string(data.get("ended_at"))
      plan.save()

      return Response({"message": "suscription updated"}, status=200)

    return Response({"message": "unhandled event"}, status=200)