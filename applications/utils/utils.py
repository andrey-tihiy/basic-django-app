from django.core.mail import send_mail
from applications.userprofile.models import UserProfile
from basic.settings import FRONTEND_HOST


def send_activation_email(user_pk):
    try:
        email = UserProfile.objects.get(id=user_pk).user.email
        link = f"{FRONTEND_HOST}/signup/{user_pk}"
        data = f"Hello there!\nIt's your activation link:\n{link}"

        send_mail('Activate account!', data, "Wombat",
                  [email], fail_silently=False)

        return {'status': 'email send'}

    except Exception:
        return {'status': 'mail dont send'}
