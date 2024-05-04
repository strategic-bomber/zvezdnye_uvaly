from django.urls import path

from .views import About, MainPage, FinalPage, HistoryPage
from .views import SurveyPage, SurveyAPI

urlpatterns = [
    path('', MainPage.as_view()),
    path('survey/about/', About.as_view()),
    path('survey/start/', SurveyPage.as_view()),
    path("api/survey/", SurveyAPI.as_view()),
    path('survey/end/', FinalPage.as_view()),
    path('history/', HistoryPage.as_view()),
    #path('survey/end/')
    #    )
]
