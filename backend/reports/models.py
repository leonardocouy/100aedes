from django.db import models
from django.utils import formats
from django.utils.translation import ugettext_lazy as _
from backend.core.models import City
from backend.accounts.models import User


REPORT_STATUS_CHOICES = (
    (0, 'Não Enviada'),
    (1, 'Enviada'),
    (2, 'Em análise'),
    (3, 'Foco tratado'),
    (4, 'Foco não encontrado')
)


class Report(models.Model):
    user = models.ForeignKey(User, related_name='reports')
    address = models.CharField('Endereço', max_length=255, null=False)
    district = models.CharField('Bairro', max_length=100, null=False)
    number = models.IntegerField('Número', null=False)
    city = models.ForeignKey(City, related_name='reports')
    description = models.TextField('Descrição')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    status = models.IntegerField('Status', choices=REPORT_STATUS_CHOICES, default=0, null=False)
    reason = models.TextField('Razão do Status', blank=True)
    image_url = models.ImageField(upload_to='denuncias/', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    modified_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = _("Denúncia")
        verbose_name_plural = _("Denúncias")

    def __str__(self):
        return 'Denúncia feita por - {} - {}'.format(self.user.first_name,
                                                    formats.date_format(self.created_at, "SHORT_DATE_FORMAT"))
