from . import views
from django.urls import path
urlpatterns = [
    path('LocTagPage',views.LocTagPage),
    path('PartTagPage',views.PartTagPage),
    path('home',views.HomePage),
    path('newlt',views.NewLocTag),
    path('newpt',views.NewPartTag),
    path('addlt',views.addLocTag),
    path('addpt',views.addPartTag),
    path('EditUserTags',views.EditUserTags),
    path('ModifyUser',views.ModifyUser),
    path('DeleteTag',views.DeleteTag),
    path('AddUserTag',views.AddUserTag),
    path('AddUTag',views.AddUTag),
    path('DelLocTag',views.DelLocTag),
    path('DelPartTag',views.DelPartTag)
]
