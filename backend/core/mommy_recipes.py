from backend.core.models import City
from backend.accounts.models import User
from backend.reports.models import Report
from django.contrib.auth.models import Group, ContentType, Permission
from model_mommy.recipe import Recipe, foreign_key, related
from django.contrib.auth.hashers import make_password


group = Recipe(
    Group,
    name='Test Group',
)

permission = Recipe(
    Permission,
    content_type=ContentType.objects.get_for_model(Report)
)

city = Recipe(
    City,
    name='Bom Despacho',
    state='MG'
)

user = Recipe(
    User,
    username='leonardo',
    first_name='Leonardo',
    last_name='Flores',
    email='leonardo@leo.com',
    password=make_password('leo'),
    is_active=True,
    city=foreign_key(city),


)

