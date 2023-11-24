from django.core.serializers import json
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
import json


def get_notifications(request):
    notification = Notification.objects.all()
    nt_count = notification.count()
    return {'notification': notification, 'nt_count':nt_count}