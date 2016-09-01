from django.db import models
from django.contrib.auth.models import AbstractUser

from backend.core.models import City

USER_TYPE_CHOICES = (
    (0, 'Cidadão'),
    (1, 'Agente')
)


class User(AbstractUser):
    phone = models.CharField('Telefone', max_length=15)
    city = models.ForeignKey(City, related_name='users')
    user_type = models.IntegerField('Tipo de Usuário', choices=USER_TYPE_CHOICES, default=0)

    def __str__(self):
        return '{} - {}'.format(self.get_full_name(), self.city.__str__())