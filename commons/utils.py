from ledeo.settings import SECRET_KEY as secretkey
from django.contrib.auth.models import User
import jwt
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from ledeo.settings import EMAIL_HOST_USER as emailuser

def utc_to_date_string(utc_timestamp):
    if utc_timestamp is None:
        return None
    try:
        # Convertir el timestamp UTC a un objeto datetime
        date_time = datetime.datetime.utcfromtimestamp(utc_timestamp)
        # Formatear la fecha y hora en el formato YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]
        date_string = date_time.strftime('%Y-%m-%d %H:%M:%S')
        return date_string
    except ValueError:
        # El timestamp no es una fecha válida
        return None

def user_from_request(request):
  token = request.headers.get('Authorization').split(" ")[1]
  payload = jwt.decode(jwt=token, key=secretkey, algorithms=['HS256']) 
  user_id = payload.get("user_id")
  return User.objects.filter(id=user_id).first()


def send_mail(subject, to, template, body="",template_context={}):
    html_template = get_template(template)
    html_content = html_template.render(template_context)
    msg = EmailMultiAlternatives(subject, body, emailuser, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()