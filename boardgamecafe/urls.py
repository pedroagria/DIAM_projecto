from django.urls import path
from .import views

app_name = 'boardgamecafe'
urlpatterns = [
    path('', views.index, name='index'),
    path('games', views.games, name='games'),
    # admin
    path('addgame', views.addgame, name='addgame'),
    path('editgame/<int:boardgame_id>', views.editgame, name='editgame'),
    path('game/<int:boardgame_id>', views.game, name='game'),
    # path('editgame', views.addeditgame, name='editgame'),
    path('addremovecalendar', views.addremovecalendar, name='addremovecalendar'),
    path('addtable', views.addtable, name='addtable'),
    path('edittable/<int:table_id>', views.edittable, name='edittable'),
    path('calendar', views.calendar, name='calendar'),
    path('titles', views.titles, name='titles'),
    path('addtitle', views.addtitle, name='addtitle'),
    path('edittitle/<int:title_id>', views.edittitle, name='edittitle'),
    #templates for inspiration
    path('tempband', views.tempband, name='tempband'),
    path('tempcafe', views.tempcafe, name='tempcafe'),
    path('tempfoodblog', views.tempfoodblog, name='tempfoodblog'),
    path('tempgourmetcatering', views.tempgourmetcatering, name='tempgourmetcatering'),
    path('tempstartpage', views.tempstartpage, name='tempstartpage'),
    path('tempstartup', views.tempstartup, name='tempstartup'),
    path('tempsocialmedia', views.tempsocialmedia, name='tempsocialmedia'),
]