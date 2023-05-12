from django.shortcuts import get_object_or_404, render
from .models import BoardGame, Calendar, Table, Title, Person
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from django.core import serializers
import json


from django.core.files.storage import FileSystemStorage
#from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'boardgamecafe/index.html')
    #return HttpResponse("<h1>Esta é a página de entrada da app boardgamecafe </h1>")

def games(request):
    # if BoardGame.objects.all().count() > 0:
    # boardgames = BoardGame.objects.all()
    # return render(request, 'boardgamecafe/games.html', {'boardgames': boardgames})
    # return render(request, 'boardgamecafe/games.html')
    all_boardgames = BoardGame.objects.all()
    boardgames_list = []
    for boardgame in all_boardgames:
        # new_boardgame = [boardgame.id.__str__(), boardgame.name, boardgame.image.__str__()]
        new_boardgame = {'id': boardgame.id, 'name': boardgame.name, 'min_players': boardgame.min_players, 'max_players': boardgame.max_players, 'min_age': boardgame.min_age, 'min_playing_time': boardgame.min_playing_time, 'image': boardgame.image.__str__(), 'log_is_active': boardgame.log_is_active}
        boardgames_list.append(new_boardgame)
    return render(request, 'boardgamecafe/games.html', {'boardgames': json.dumps(boardgames_list)})
    # return render(request, 'boardgamecafe/games.html', {'boardgames': boardgames_list})
    #
    # boardgames_json = serializers.serialize('json', boardgames)
    # return

def game(request, boardgame_id):
    boardgame = get_object_or_404(BoardGame, pk=boardgame_id)
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/game.html', {'boardgame': boardgame, })
    # text = request.POST.get('new_comment')
    # person =

    # COPIADO DO EDIT PARA MODIFICAR:
    # name = request.POST.get('name')
    # release_year = request.POST.get('release_year')
    # min_players = request.POST.get('min_players')
    # max_players = request.POST.get('max_players')
    # min_age = request.POST.get('min_age')
    # min_playing_time = request.POST.get('min_playing_time')
    # avg_playing_time = request.POST.get('avg_playing_time')
    # complexity = request.POST.get('complexity')
    # number_of_copies = request.POST.get('number_of_copies')
    # description = request.POST.get('description')
    # link = request.POST.get('link')
    # image = request.FILES.get('image')
    # if request.POST.get('log_is_active'):
    #     log_is_active = True
    # else:
    #     log_is_active = False
    # if name and release_year and min_players and max_players and min_age and min_playing_time and avg_playing_time and complexity and number_of_copies and description and link and image:
    #     boardgame.name = name
    #     boardgame.release_year = release_year
    #     boardgame.min_players = min_players
    #     boardgame.max_players = max_players
    #     boardgame.min_age = min_age
    #     boardgame.min_playing_time = min_playing_time
    #     boardgame.avg_playing_time = avg_playing_time
    #     boardgame.complexity = complexity
    #     boardgame.number_of_copies = number_of_copies
    #     boardgame.description = description
    #     boardgame.link = link
    #     fs = FileSystemStorage()
    #     filename = fs.save('boardgame_image_' + str(boardgame.id) + '.webp', image)
    #     uploaded_file_url = fs.url(filename)
    #     boardgame.image = uploaded_file_url
    #     log_is_active = log_is_active
    #     log_date_last_update = timezone.now()
    #     boardgame.save()
    #     return HttpResponseRedirect(reverse('boardgamecafe:games'))
    # return render(request, 'boardgamecafe/managegame.html',
    #               {'boardgame_id': boardgame_id,
    #                'error_message': "Error editing board game. Be sure that all fields are filled correctly."})

def addgame(request):
    # return render(request, 'boardgamecafe/managegame.html')
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/managegame.html')
    name = request.POST.get('name')
    release_year = request.POST.get('release_year')
    min_players = request.POST.get('min_players')
    max_players = request.POST.get('max_players')
    min_age = request.POST.get('min_age')
    min_playing_time = request.POST.get('min_playing_time')
    avg_playing_time = request.POST.get('avg_playing_time')
    complexity = request.POST.get('complexity')
    number_of_copies = request.POST.get('number_of_copies')
    description = request.POST.get('description')
    link = request.POST.get('link')
    image = request.FILES.get('image')
    # image = request.POST.get('image')
    if request.POST.get('log_is_active'):
        log_is_active = True
    else:
        log_is_active = False
    if name and release_year and min_players and max_players and min_age and min_playing_time and avg_playing_time and complexity and number_of_copies and description and link and image:
        boardgame = BoardGame(name=name, release_year=release_year, min_players=min_players, max_players=max_players,
                              min_age=min_age, min_playing_time=min_playing_time, avg_playing_time=avg_playing_time,
                              complexity=complexity, number_of_copies=number_of_copies, description=description,
                              link=link, image="temp", log_is_active=log_is_active, log_date_created=timezone.now(),
                              log_date_last_update=timezone.now())
        boardgame.save()
        fs = FileSystemStorage()
        filename = fs.save('boardgame_image_' + str(boardgame.id) + '.webp', image)
        uploaded_file_url = fs.url(filename)
        boardgame.image = uploaded_file_url
        boardgame.save()
        return HttpResponseRedirect(reverse('boardgamecafe:games'))
    return render(request, 'boardgamecafe/managegame.html', {'error_message': "Error adding new board game. Be sure that all fields are filled correctly."})
    # return HttpResponseRedirect(reverse('boargamecafe:addgame')) # adicionar mensagem de erro?

def editgame(request, boardgame_id):
    boardgame = get_object_or_404(BoardGame, pk=boardgame_id)
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/managegame.html', {'boardgame': boardgame,})
    name = request.POST.get('name')
    release_year = request.POST.get('release_year')
    min_players = request.POST.get('min_players')
    max_players = request.POST.get('max_players')
    min_age = request.POST.get('min_age')
    min_playing_time = request.POST.get('min_playing_time')
    avg_playing_time = request.POST.get('avg_playing_time')
    complexity = request.POST.get('complexity')
    number_of_copies = request.POST.get('number_of_copies')
    description = request.POST.get('description')
    link = request.POST.get('link')
    image = request.FILES.get('image')
    if request.POST.get('log_is_active'):
        log_is_active = True
    else:
        log_is_active = False
    if name and release_year and min_players and max_players and min_age and min_playing_time and avg_playing_time and complexity and number_of_copies and description and link and image:
        boardgame.name = name
        boardgame.release_year = release_year
        boardgame.min_players = min_players
        boardgame.max_players = max_players
        boardgame.min_age = min_age
        boardgame.min_playing_time = min_playing_time
        boardgame.avg_playing_time = avg_playing_time
        boardgame.complexity = complexity
        boardgame.number_of_copies = number_of_copies
        boardgame.description = description
        boardgame.link = link
        fs = FileSystemStorage()
        filename = fs.save('boardgame_image_' + str(boardgame.id) + '.webp', image)
        uploaded_file_url = fs.url(filename)
        boardgame.image = uploaded_file_url
        boardgame.log_is_active = log_is_active
        boardgame.log_date_last_update = timezone.now()
        boardgame.save()
        return HttpResponseRedirect(reverse('boardgamecafe:games'))
    return render(request, 'boardgamecafe/managegame.html',
                  {'boardgame_id': boardgame_id, 'error_message': "Error editing board game. Be sure that all fields are filled correctly."})

def titles(request):

    if Title.objects.all().count() > 0:
        titles = Title.objects.all()
        # ENVIAR INFORMACAO SE O PERSON LOGIN TEM O TITLE
    # boardgames_list = []
    # for boardgame in all_boardgames:
    #     # new_boardgame = [boardgame.id.__str__(), boardgame.name, boardgame.image.__str__()]
    #     new_boardgame = {'id': boardgame.id, 'name': boardgame.name, 'min_players': boardgame.min_players, 'max_players': boardgame.max_players, 'min_age': boardgame.min_age, 'min_playing_time': boardgame.min_playing_time, 'image': boardgame.image.__str__(), 'log_is_active': boardgame.log_is_active}
    #     boardgames_list.append(new_boardgame)
        return render(request, 'boardgamecafe/titles.html', {'titles': titles})
    return render(request, 'boardgamecafe/titles.html')

def addtitle(request):
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/managetitle.html')
    designation = request.POST.get('designation')
    unlock_conditions = request.POST.get('unlock_conditions')
    if request.POST.get('log_is_active'):
        log_is_active = True
    else:
        log_is_active = False
    if designation and unlock_conditions:
        title = Title(designation=designation, unlock_conditions=unlock_conditions, log_is_active=log_is_active, log_date_created=timezone.now(), log_date_last_update=timezone.now())
        title.save()
        if unlock_conditions == "None":
            people = Person.objects.all()
            for person in people:
                person.unlocked_titles.add(title) #julgo não ser preciso fazer save quando se faz add, mas algo a testar
        return HttpResponseRedirect(reverse('boardgamecafe:titles'))
    return render(request, 'boardgamecafe/managegame.html', {'error_message': "Error adding new title. Be sure that all fields are filled correctly."})

def edittitle(request, title_id):
    title = get_object_or_404(Title, pk=title_id)
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/managetitle.html', {'title': title,})
    designation = request.POST.get('designation')
    unlock_conditions = request.POST.get('unlock_conditions')
    previous_unlock_conditions = title.unlock_conditions
    if request.POST.get('log_is_active'):
        log_is_active = True
    else:
        log_is_active = False
    if designation and unlock_conditions:
        title.designation = designation
        title.unlock_conditions = unlock_conditions
        title.log_is_active = log_is_active
        title.log_date_last_update = timezone.now()
        title.save()
        if unlock_conditions != previous_unlock_conditions and unlock_conditions == "None":
            all_people = Person.objects.all()
            for person in all_people:
                if not title.people.filter(pk=person.id).exists():
                    person.unlocked_titles.add(title) #julgo não ser preciso fazer save quando se faz add, mas algo a testar;
        return HttpResponseRedirect(reverse('boardgamecafe:titles'))
    return render(request, 'boardgamecafe/managetitle.html',
                  {'title_id': title_id, 'error_message': "Error editing title. Be sure that all fields are filled correctly."})


def addremovecalendar(request):
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/managecalendar.html')

    if request.POST.get('log_is_active'):
        log_is_active = False
    else:
        log_is_active = True

    # Para adicionar registos
    if log_is_active:
        startdate = datetime.strptime(request.POST.get('startdate'), '%Y-%m-%d').date()
        enddate = datetime.strptime(request.POST.get('enddate'), '%Y-%m-%d').date()
        numbers_days = (enddate - startdate).days + 1
        dates_to_add = [startdate + timedelta(days=x) for x in range(numbers_days)]

        opentime = datetime.strptime(request.POST.get('opentime'), '%H:%M').time()
        closetime = datetime.strptime(request.POST.get('closetime'), '%H:%M').time()

        weekdays = [False] * 7
        if request.POST.get('monday'):
            weekdays[0] = True
        if request.POST.get('tuesday'):
            weekdays[1] = True
        if request.POST.get('wednesday'):
            weekdays[2] = True
        if request.POST.get('thursday'):
            weekdays[3] = True
        if request.POST.get('friday'):
            weekdays[4] = True
        if request.POST.get('saturday'):
            weekdays[5] = True
        if request.POST.get('sunday'):
            weekdays[6] = True

        # Verifica se a data já está na base de dados, se sim actualiza os valores
        date_list_objects = Calendar.objects.all()
        aux = dates_to_add.copy()
        for d in date_list_objects:
            if d.date in dates_to_add:
                i_weekday = d.date.weekday()  # segunda é 0 e domingo é 6
                if weekdays[i_weekday]:
                    calendar = Calendar.objects.get(id=d.id)
                    print(calendar)
                    calendar.open_time = opentime
                    calendar.close_time = closetime
                    calendar.log_is_active = log_is_active
                    calendar.log_date_last_update = timezone.now()
                    calendar.save()
                    aux.remove(d.date)

        # Para as datas que não existem na base de dados, cria novo registos
        for i in aux:
            i_weekday = i.weekday()  # segunda é 0 e domingo é 6
            if weekdays[i_weekday]:
                calendar = Calendar(date=i, open_time=opentime, close_time=closetime, log_is_active=log_is_active, log_date_created=timezone.now(), log_date_last_update=timezone.now())
                calendar.save()

    # Para remover registos
    else:
        startdate = datetime.strptime(request.POST.get('startdate'), '%Y-%m-%d').date()
        enddate = datetime.strptime(request.POST.get('enddate'), '%Y-%m-%d').date()
        numbers_days = (enddate - startdate).days + 1
        dates_to_remove = [startdate + timedelta(days=x) for x in range(numbers_days)]
        date_list_objects = Calendar.objects.all()
        for d in date_list_objects:
            if d.date in dates_to_remove:
                # Calendar.objects.filter(id=d.id).delete()
                calendar = Calendar.objects.get(id=d.id)
                calendar.log_is_active = log_is_active
                calendar.log_date_last_update = timezone.now()
                calendar.save()

    return render(request, 'boardgamecafe/managecalendar.html')

def addtable(request):
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/managetable.html')
    name = request.POST.get('name')
    capacity = request.POST.get('capacity')
    if request.POST.get('log_is_active'):
        log_is_active = True
    else:
        log_is_active = False
    if name and capacity:
        table = Table(name=name, capacity=capacity, log_is_active=log_is_active, log_date_created=timezone.now(), log_date_last_update=timezone.now())
        table.save()
        return HttpResponseRedirect(reverse('boardgamecafe:index'))
    return render(request, 'boardgamecafe/managetable.html', {'error_message': "Error adding new table. Be sure that all fields are filled correctly."})


def edittable(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/managetable.html', {'table': table, })
    name = request.POST.get('name')
    capacity = request.POST.get('capacity')
    if request.POST.get('log_is_active'):
        log_is_active = True
    else:
        log_is_active = False
    if name and capacity:
        table.name = name
        table.capacity = capacity
        table.log_is_active = log_is_active
        table.save()
        return HttpResponseRedirect(reverse('boardgamecafe:index'))
    return render(request, 'boardgamecafe/managetable.html', {'table': table, 'error_message': "Error editing table. Be sure that all fields are filled correctly."})


def calendar(request):
    # Vai buscar todas as mesas à base de dados
    all_tables = Table.objects.all()
    tables_list = []
    for table in all_tables:
        new_table = {'id': table.id, 'name': table.name, 'capacity': table.capacity, 'log_is_active': table.log_is_active}
        tables_list.append(new_table)

    # Vai buscar a data de hoje
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    date = Calendar.objects.filter(date=today).values('id', 'date', 'open_time', 'close_time', 'log_is_active')
    slots_list = []
    for d in date:
        if date.count() > 0 and d['log_is_active']:
            ot_aux = int(d['open_time'].strftime('%H:%M').split(':')[0])
            ct_aux = int(d['close_time'].strftime('%H:%M').split(':')[0])
            for i in range(ot_aux, ct_aux + 1):
                if i < 10:
                    aux = "0" + str(i) + ":00"
                else:
                    aux = str(i) + ":00"
                slots_list.append(aux)

            return render(request, 'boardgamecafe/calendar.html', {'tables': tables_list, 'date': date, 'slots_list': slots_list})
        else:
            return render(request, 'boardgamecafe/calendar.html')

    return render(request, 'boardgamecafe/calendar.html')


# Vai buscar todas as mesas à base de dados
def alltables():
    all_tables = Table.objects.all()
    tables_list = []
    for table in all_tables:
        new_table = {'id': table.id, 'name': table.name, 'capacity': table.capacity, 'log_is_active': table.log_is_active}
        tables_list.append(new_table)
    return tables_list


def newdate(date, ispreviousdate):
    if ispreviousdate:
        return datetime.strptime(date, '%Y-%m-%d').date() - timedelta(days=1)
    else:
        return datetime.strptime(date, '%Y-%m-%d').date() + timedelta(days=1)


def allslots(date):
    slots_list = []
    for d in date:
        if date.count() > 0 and d['log_is_active']:
            ot_aux = int(d['open_time'].strftime('%H:%M').split(':')[0])
            ct_aux = int(d['close_time'].strftime('%H:%M').split(':')[0])
            for i in range(ot_aux, ct_aux + 1):
                if i < 10:
                    aux = "0" + str(i) + ":00"
                else:
                    aux = str(i) + ":00"
                slots_list.append(aux)
    return slots_list

def nextdate(request, date_str, ispreviousdate_int):
    tables_list = alltables()
    if ispreviousdate_int == 1:
        nextdate = newdate(date_str, True)
    else:
        nextdate = newdate(date_str, False)
    date = Calendar.objects.filter(date=nextdate).values('id', 'date', 'open_time', 'close_time', 'log_is_active')
    for d in date:
        if date.count() > 0 and d['log_is_active']:
            slots_list = allslots(date)
            return render(request, 'boardgamecafe/calendar.html', {'tables': tables_list, 'date': date, 'slots_list': slots_list})
        else:
            return render(request, 'boardgamecafe/calendar.html')
    return render(request, 'boardgamecafe/calendar.html')







# Templates
def tempband(request):
    return render(request, 'boardgamecafe/tempband.html')

def tempcafe(request):
    return render(request, 'boardgamecafe/tempcafe.html')

def tempfoodblog(request):
    return render(request, 'boardgamecafe/tempfoodblog.html')

def tempgourmetcatering(request):
    return render(request, 'boardgamecafe/tempgourmetcatering.html')

def tempstartpage(request):
    return render(request, 'boardgamecafe/tempstartpage.html')

def tempstartup(request):
    return render(request, 'boardgamecafe/tempstartup.html')

def tempsocialmedia(request):
    return render(request, 'boardgamecafe/tempsocialmedia.html')
