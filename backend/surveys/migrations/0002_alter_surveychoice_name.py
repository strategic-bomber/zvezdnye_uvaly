# Generated by Django 5.0.3 on 2024-04-04 15:41
from django.contrib.auth.models import User
from django.db import migrations
from src.helpers.init_points import coordinates
from src.helpers.init_survey_data import choices
from surveys.models import Survey, SurveyChoice, ImageModel


def add_base_data(apps, schema_editor):
    # Survey: Type[Model] = apps.get_model('surveys', 'Survey')
    s = Survey.objects.create(name="Звёздные увалы",
                              description="Опрос по обустройству территории 'Звёздные Увалы'",
                              total_budget=75_000_000,
                              map="si1488.png",
                              coordinates=coordinates)
    User.objects.create_superuser(username="user@username.ru", password="user@username.ru")


    # добавим ивенты
    for c in choices:
        name, price, images = c['name'], c['price'], c['images']
        sc = SurveyChoice.objects.create(name=name, price=price, survey=s)
        # Добавим фотографии
        for i in images:
            ImageModel.objects.create(choice=sc, image=i)


class Migration(migrations.Migration):
    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_base_data)
    ]
