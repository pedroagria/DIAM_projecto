from django.urls import path
from .import views

app_name = 'boardgamecafe'
urlpatterns = [
    path('', views.index, name='index'),
    path('games', views.games, name='games'),
    path('game/<int:boardgame_id>', views.game, name='game'),
    path('titles', views.titles, name='titles'),

    # sign in, sign up and personal area
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.signout, name='logout'),
    path('personalarea', views.personalarea, name='personalarea'),
    path('userdetails', views.userdetails, name='userdetails'),
    path('bookinguser', views.bookinguser, name='bookinguser'),

    # admin management
    path('users', views.users, name='users'),
    path('createuser', views.createuser, name='createuser'),
    path('addgame', views.addgame, name='addgame'),
    path('editgame/<int:boardgame_id>', views.editgame, name='editgame'),
    path('addtitle', views.addtitle, name='addtitle'),
    path('edittitle/<int:title_id>', views.edittitle, name='edittitle'),
    path('managecalendar', views.managecalendar, name='managecalendar'),
    path('addtable', views.addtable, name='addtable'),
    path('edittable/<int:table_id>', views.edittable, name='edittable'),
    path('calendar', views.calendar, name='calendar'),
    path('nextdate/<str:date_str>/<int:ispreviousdate_int>', views.nextdate, name='nextdate'),
    path('tables', views.tables, name='tables'),

    # booking
    path('newbooking', views.newbooking, name='newbooking'),
    path('newbooking2', views.newbooking2, name='newbooking2'),
    path('newbooking3', views.newbooking3, name='newbooking3'),
    path('newbooking4', views.newbooking4, name='newbooking4'),
    path('bookingerror', views.bookingerror, name='bookingerror'),
    path('bookingdetails/<int:booking_id>', views.bookingdetails, name='bookingdetails'),

    # REACT
    path('api/tables/', views.tables_list),
    path('api/tables/<int:pk>', views.table_edit),
]