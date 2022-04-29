
from django.db import models
import uuid
from django.contrib.auth.models import User

from datetime import datetime, timezone, timedelta

class BugReport(models.Model):

    class Status(models.TextChoices):
        new='Новый'
        open = 'Открыт'
        closed = 'Закрытый'

    class Priority(models.TextChoices):
        P1 = 'Высокий'
        P2 = 'Средний'
        P3 = 'Низкий'
            
    class Severity(models.TextChoices):   
        S1 = 'Блокирующий'
        S2 = 'Критический'
        S3 = 'Значительный'
        S4 = 'Незначительный'
        S5 = 'Тривиальный'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner= models.ForeignKey(User, on_delete=models.CASCADE, related_name='bugreports')
    index = models.IntegerField()
    name = models.TextField()
    steps = models.TextField(default = '', blank=True)
    fact_result =  models.TextField(default = '', blank=True)
    exp_result = models.TextField(default = '', blank=True)
    desc = models.TextField(default = '', blank=True)
    priority = models.TextField(choices=Priority.choices)
    severity = models.TextField(choices=Severity.choices)
    status = models.TextField(choices=Status.choices)
    url = models.TextField(default = '', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


