from django import forms

class AboutUser(forms.Form):
    surname = forms.CharField(label="Фамилия", max_length=100)
    name = forms.CharField(label="Имя", max_length=100)
    patronymic = forms.CharField(label="Отчество", max_length=100)
    birth_year = forms.IntegerField(label='Год рождения', min_value=1900, max_value=2024)
    CHOICES = [("М", 'Мужской'), ('Ж', 'Женский')]
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label="Пол")
    job = forms.CharField(label='Сфера деятельности', max_length=100)



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'multiple': True, 'accept': 'image/*'}  # Allow multiple files and accept only images
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class AChoiceForm(forms.ModelForm):
    name = forms.CharField(max_length=255, label="Название объекта")
    price = forms.FloatField(label="Стоимость в р.")
    images = MultipleFileField(label="Фотографии объекта")

