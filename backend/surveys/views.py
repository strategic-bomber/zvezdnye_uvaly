import json
from typing import List
import csv

from django.contrib.sessions.models import Session
from django.db import transaction
from django.db.models import QuerySet, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .forms import AboutUser
from .models import Survey, SurveyChoice, UserChoice
from .services import UnicodeJsonResponse, get_body, render_frontend


class MainPage(View):

    def get(self, request):
        return render(request, template_name="lending_page.html", context={"survey": 'fjdk'})


class SurveyPage(View):
    def get(self, request):
        return render_frontend(request)


@method_decorator(csrf_exempt, name='dispatch')
class About(View):

    def get(self, request):
        form = AboutUser()
        return render(request, 'about.html', context={'form': form})

    def post(self, request):
        # save user data
        form = AboutUser(request.POST)
        if form.is_valid():
            for k, vin in form.cleaned_data.items():
                request.session[k] = vin
        # save from form
        return HttpResponseRedirect("/survey/start")


class FinalPage(View):

    def get(self, request):
        return render(request, template_name="final.html", context={"final_page": 'fjdk'})

    def post(self, request):
        return HttpResponseRedirect("/")


class HistoryPage(View):

    def get(self, request):
        return render(request, template_name="history.html", context={"history_page": 'fjdk'})

    def post(self, request):
        return HttpResponseRedirect("/")


@method_decorator(csrf_exempt, name='dispatch')
class SurveyAPI(View):

    def get(self, request):
        """Показать опросник"""
        s = Survey.objects.get(id=1)  # хардкод - не приговор.

        choices: QuerySet[SurveyChoice] = s.choices.prefetch_related("images").all()
        coords = s.coordinates  # id, x, y, name, price
        return UnicodeJsonResponse({"coords": coords,
                                    "choices": [{
                                        "id": c.id,
                                        "name": c.name,
                                        "price": c.price,  # FIXME IMAGE.PATH
                                        "photos": [request.build_absolute_uri(p.image.url) for p in c.images.all()]
                                    }
                                        for c in choices
                                    ],
                                    "total_price": s.total_budget
                                    })

    @transaction.atomic
    def post(self, request):
        '''Сохранить заполненные поля'''
        body = get_body(request)
        survey: Survey = Survey.objects.get(id=1)
        available = {a.id: a for a in survey.choices.all()}
        coords = {c['id']: c for c in survey.coordinates}
        created = []
        if not request.session.session_key:
            request.session.save()

        session_id = request.session.session_key

        for choice in body['choices']:

            schoice_id, coord_id = choice['choice_id'], choice['coords_id']
            c: SurveyChoice = available.get(schoice_id)
            if c is None:
                continue
            if coords.get(coord_id) is None:
                continue
            # сохраняем

            # запоминаем выбор пользака

            new = UserChoice.objects.create(
                coordinates=coords[coord_id],
                choice=available[schoice_id],
                session_key=session_id,
                user=request.user if request.user.is_authenticated else None
            )
            created.append(new)
        #created = [c.id for c in created]

        return UnicodeJsonResponse({"success": True})

