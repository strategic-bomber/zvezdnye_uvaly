import csv
import os
from collections import defaultdict
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.db import transaction
from django.http import FileResponse
from django.utils.html import format_html

from .forms import AChoiceForm
# Register your models here.


from django import forms
from django.contrib import admin
from .models import Survey, SurveyChoice, ImageModel, UserChoice




@admin.action(description="Выгрузить кол-во выбранных объектов")
def download_popular(modeladmin, request, queryset):
    s = queryset.first()
    s: Survey
    # собираем объекты
    variants = s.choices.all()
    data = {}
    for v in variants:
        data[v.name] = v.userchoice_set.count()
    ndata = {k: data.get(k) for k in sorted(data, key=lambda x: data.get(x))}
    ndata = [{"Объект": k, "Выбрано": v} for k, v in ndata.items()]

    field_names = ['Объект', 'Выбрано']

    # Open the file in write mode
    with open('survey_count.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        # Write the header
        writer.writeheader()
        # Write the rows
        writer.writerows(ndata)
    return FileResponse(open('survey_count.csv', "rb"))


class SurveyAdminForm(forms.ModelForm):


    class Meta:
        model = Survey
        fields = ['name', 'map', 'description', 'total_budget']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['map'].widget = forms.FileInput(attrs={'class': 'custom-map-widget'})


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    """"""
    actions = [download_popular]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(SurveyChoice)
class SurveyChoiceAdmin(admin.ModelAdmin):
    form = AChoiceForm
    readonly_fields = ['images_tag']

    def images_tag(self, obj: SurveyChoice):
        """Method to return store image for admin panel"""

        images = ''
        for img in obj.images.all():
            p = img.image.url
            images += '<img src="%s" height="150" width="150"/>' % p
        return format_html(images)

    images_tag.allow_tags = True

    @transaction.atomic
    def save_model(self, request, obj, form: AChoiceForm, change):
        super().save_model(request, obj, form, change)
        # add pictures
        if 'images' in form.cleaned_data and len(form.cleaned_data['images']) > 0:
            obj.images.all().delete()
            image_files = form.cleaned_data['images']
            for image_file in image_files:
                image_path = Path(settings.MEDIA_ROOT, image_file.name)
                with open(image_path, 'wb') as destination:
                    for chunk in image_file.chunks():
                        destination.write(chunk)
                to_save = str(image_path.relative_to(settings.MEDIA_ROOT))
                ImageModel.objects.create(choice=obj, image=to_save)


@admin.register(UserChoice)
class UserChoiceAdmin(admin.ModelAdmin):
    ...