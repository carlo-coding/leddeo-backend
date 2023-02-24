from rest_framework.views import APIView
from rest_framework.response import Response
from commons.utils import utc_to_date_string, is_valid_plan
from .models import Plan
from account.models import UserInfo, User
import stripe
from ledeo.settings import (
  CHECKOUT_CANCEL_URL,
  CHECKOUT_SUCCESS_URL,
  STRIPE_PORTAL_RETURN_URL
)
from rest_framework.permissions import IsAuthenticated
from commons.utils import user_from_request, userid_from_request
class CreateCheckoutSessionView(APIView):
  permission_classes=[IsAuthenticated]
  def post(self, request):
    user = user_from_request(request)
    lookup_key=request.data.get("lookup_key")
    customer_id=request.data.get("customer_id")
    prices = stripe.Price.list(
      lookup_keys=[lookup_key],
      expand=['data.product']
    )
    plans = Plan.objects.filter(user=user)
    plan = None
    for p in plans:
      if is_valid_plan(p):
        plan = p
        break
    
    if plan and plan.lookup_key == lookup_key:
      return Response({ "error": "User already has this plan" }, status=400)
    elif plan:
      subscription = stripe.Subscription.retrieve(plan.stripe_subscription_id)
      if not subscription:
        return Response({"error": "Subscription not found"}, status=404)
      stripe.Subscription.modify(
        subscription.id,
        cancel_at_period_end=False,
        proration_behavior='always_invoice',
        items=[{
          "id": subscription['items']['data'][0].id,
          "price": prices.data[0].id,
        }],
      )
      return Response({ "url": CHECKOUT_SUCCESS_URL })
    checkout_session = stripe.checkout.Session.create(
      line_items=[
        {
          'price': prices.data[0].id,
          'quantity': 1,
        },
      ],
      mode='subscription',
      success_url=CHECKOUT_SUCCESS_URL,
      cancel_url=CHECKOUT_CANCEL_URL,
      customer=customer_id,
      allow_promotion_codes=True,
      subscription_data={
        "trial_period_days": prices.data[0]["recurring"].get("trial_period_days")
      }
    )
    return Response({
      "url": checkout_session.url
    })

class HandleSubscription(APIView):
  permission_classes=[IsAuthenticated]
  def delete(self, request):
    subscription_id = request.data.get("subscription_id")
    user_id = userid_from_request(request)
    plan = Plan.objects.filter(
      user_id=user_id, 
      stripe_subscription_id=subscription_id
    ).first()
    if not plan:
      return Response({ "error": "Subscription not found" }, status=404)
    result = stripe.Subscription.modify(
      plan.stripe_subscription_id,
      cancel_at_period_end=True,
      proration_behavior='always_invoice'
    )
    return Response(result)

  def patch(self, request):
    subscription_id = request.data.get("subscription_id")
    user_id = userid_from_request(request)
    plan = Plan.objects.filter(
      user_id=user_id, 
      stripe_subscription_id=subscription_id
    ).first()
    if not plan:
      return Response({ "error": "Subscription not found" }, status=404)
    result = stripe.Subscription.modify(
      plan.stripe_subscription_id,
      cancel_at_period_end=False,
      proration_behavior='always_invoice'
    )
    return Response(result)

class CreatePortalSessionView(APIView):
  def post(self, request):
    checkout_session_id = request.data.get("session_id", "")
    if checkout_session_id:
      checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
      portalSession = stripe.billing_portal.Session.create(
          customer=checkout_session.customer,
          return_url=STRIPE_PORTAL_RETURN_URL
      )
      return Response({
        "url": portalSession.url
      })
    
    customer_id = request.data.get("customer_id", "")
    if not customer_id:
      return Response({"message": "session_id or customer_id were not provided"})
    portalSession = stripe.billing_portal.Session.create(
      customer=customer_id,
      return_url=STRIPE_PORTAL_RETURN_URL
    )
    return Response({
      "url": portalSession.url
    })


class GetPricesView(APIView):
  def get(self, request):
    prices = stripe.Price.list(active=True)
    return Response(prices)

class GetInvoicesView(APIView):
  permission_classes=[IsAuthenticated]
  def get(self, request, *args, **kwargs):
    user_id = userid_from_request(request)
    info = UserInfo.objects.filter(user_id=user_id).first()
    if not info:
      return Response({ "error": "user not found" }, status=404)
    invoices = stripe.Invoice.list(
      customer=info.customer_id,
      limit=100
    )
    return Response(invoices)

class SubscriptionWebhook(APIView):
  def post(self, request):
    event = request.data
    payload = request.data

    if event["type"] == "customer.updated":
      data = payload["data"]["object"]
      info = UserInfo.objects.filter(customer_id=data.get("id")).first()
      info.balance = data.get("balance")
      info.save()

    if event['type'] == 'customer.subscription.created':
      data = payload["data"]["object"]
      subscription = data["items"]["data"][0]

      userInfo = UserInfo.objects.filter(customer_id=data.get("customer")).first()
      user = User.objects.filter(id=userInfo.user_id).first()

      plan = Plan(
        user=user,
        lookup_key=subscription["price"].get("lookup_key", ""),
        stripe_subscription_id=data.get("id"),
        name=subscription["price"].get("nickname", ""),
        unit_amount=subscription["price"].get("unit_amount", ""),
        billing_cycle_anchor=utc_to_date_string(data.get("billing_cycle_anchor")),
        start_date=utc_to_date_string(data.get("start_date")),
        trial_start=utc_to_date_string(data.get("trial_start")),
        trial_end=utc_to_date_string(data.get("trial_end")),
        current_period_end=utc_to_date_string(data.get("current_period_end")),
        current_period_start=utc_to_date_string(data.get("current_period_start")),
        cancel_at=utc_to_date_string(data.get("cancel_at")),
        canceled_at=utc_to_date_string(data.get("canceled_at")),
        ended_at=utc_to_date_string(data.get("ended_at")),
        interval=subscription["price"]["recurring"].get("interval"),
        currency=subscription["price"].get("currency"),
        status=data.get("status")
      )
      plan.save()
      return Response({"message": "suscription created"}, status=200)

    if event['type'] == 'customer.subscription.updated' or event["type"] == "customer.subscription.deleted":
      data = payload["data"]["object"]
      subscription = data["items"]["data"][0]

      plan = Plan.objects.filter(stripe_subscription_id=data.get("id")).first()
      if not plan:
        return Response({"message": "plan not found"}, status=400)
      plan.status=data.get("status")
      plan.name=subscription["price"].get("nickname", "")
      plan.billing_cycle_anchor=utc_to_date_string(data.get("billing_cycle_anchor"))
      plan.start_date=utc_to_date_string(data.get("start_date"))
      plan.trial_start=utc_to_date_string(data.get("trial_start"))
      plan.trial_end=utc_to_date_string(data.get("trial_end"))
      plan.current_period_end=utc_to_date_string(data.get("current_period_end"))
      plan.current_period_start=utc_to_date_string(data.get("current_period_start"))
      plan.cancel_at=utc_to_date_string(data.get("cancel_at"))
      plan.canceled_at=utc_to_date_string(data.get("canceled_at"))
      plan.ended_at=utc_to_date_string(data.get("ended_at"))
      plan.lookup_key=subscription["price"].get("lookup_key", "")
      plan.unit_amount=subscription["price"].get("unit_amount", "")
      plan.interval=subscription["price"]["recurring"].get("interval")
      plan.currency=subscription["price"].get("currency")
      plan.save()

      return Response({"message": "suscription updated"}, status=200)

    return Response({"message": "unhandled event"}, status=200)