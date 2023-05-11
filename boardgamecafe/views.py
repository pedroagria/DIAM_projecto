from django.shortcuts import get_object_or_404, render
from .models import BoardGame, Calendar, Table
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta


from django.core.files.storage import FileSystemStorage
#from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'boardgamecafe/index.html')
    #return HttpResponse("<h1>Esta é a página de entrada da app boardgamecafe </h1>")

def games(request):
    if BoardGame.objects.all().count() > 0:
        boardgames = BoardGame.objects.all()
        return render(request, 'boardgamecafe/games.html', {'boardgames': boardgames})
    return render(request, 'boardgamecafe/games.html')
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
        log_is_active = log_is_active
        log_date_last_update = timezone.now()
        boardgame.save()
        return HttpResponseRedirect(reverse('boardgamecafe:games'))
    return render(request, 'boardgamecafe/managegame.html',
                  {'boardgame_id': boardgame_id, 'error_message': "Error editing board game. Be sure that all fields are filled correctly."})





def addcalendar(request):
    # TODO - Falta validações tanto na view como no html
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/managecalendar.html')
    startdate = datetime.strptime(request.POST.get('startdate'), '%Y-%m-%d').date()
    enddate = datetime.strptime(request.POST.get('enddate'), '%Y-%m-%d').date()
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
    print(weekdays)
    numbers_days = (enddate-startdate).days + 1
    list_dates = [startdate + timedelta(days=x) for x in range(numbers_days)]
    for i in list_dates:
        i_weekday = i.weekday() # segunda é 0 e domingo é 6
        if weekdays[i_weekday]:
            calendar = Calendar(date=i, open_time=opentime, close_time=closetime, log_is_active=True, log_date_created=timezone.now(), log_date_last_update=timezone.now())
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
