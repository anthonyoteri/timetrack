from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import Timer


def get_active_timer(user):
    try:
        return Timer.objects.get(project__user=user, stop=None)
    except ObjectDoesNotExist:
        return None


def clear_active_timer(user, timestamp):
    current = get_active_timer(user)

    if current is None:
        return

    current.stop = timestamp
