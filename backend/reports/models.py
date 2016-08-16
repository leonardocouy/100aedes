from django.db import models
from django.utils.translation import ugettext_lazy as _
from backend.core.models import City

REPORT_STATUS_CHOICES = (
    (1, 'Enviada'),
    (2, 'Em análise'),
    (3, 'Foco Tratado'),
    (4, 'Foco não encontrado')
)


class Report(models.Model):
    address = models.CharField(max_length=255, blank=False)
    district = models.CharField(max_length=100, blank=False)
    city = models.ForeignKey(City, related_name='reports')
    description = models.TextField(max_length=255, blank=True)
    landmark = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    status = models.IntegerField(choices=REPORT_STATUS_CHOICES, default=1)
    image_url = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = _("Denúncias")
        verbose_name_plural = _("Denúncias")