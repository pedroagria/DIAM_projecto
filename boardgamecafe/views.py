from django.shortcuts import get_object_or_404, render
from .models import BoardGame, Calendar, Table, Title, Person, Comment, BoardGameLove, CommentLove, Review, Booking
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout


from django.core.files.storage import FileSystemStorage
#from django.http import HttpResponse


def index(request):
    return render(request, 'boardgamecafe/index.html')

def games(request):
    all_boardgames = BoardGame.objects.all()
    boardgames_list = []
    for boardgame in all_boardgames:
        new_boardgame = {'id': boardgame.id, 'name': boardgame.name, 'min_players': boardgame.min_players, 'max_players': boardgame.max_players, 'min_age': boardgame.min_age, 'min_playing_time': boardgame.min_playing_time, 'image': boardgame.image.__str__(), 'log_is_active': boardgame.log_is_active}
        boardgames_list.append(new_boardgame)
    return render(request, 'boardgamecafe/games.html', {'boardgames': json.dumps(boardgames_list)})


def game(request, boardgame_id):
    boardgame = get_object_or_404(BoardGame, pk=boardgame_id)
    # SE NÃO FOR AUTENTICADO
    if not request.user.is_authenticated:
        boardgame_love_count = boardgame.boardgamelove_set.filter(log_is_active=True).count()
        all_comments = boardgame.comment_set.all().filter(log_is_active=True).order_by('-log_date_created')
        boardgame_reviews = boardgame.review_set.all().filter(log_is_active=True)
        boardgame_review_count = boardgame_reviews.count()
        boardgame_review_rating = 0
        if boardgame_review_count != 0:
            for review in boardgame_reviews:
                boardgame_review_rating += review.rate
            boardgame_review_rating = boardgame_review_rating/boardgame_review_count
        if not all_comments:
            return render(request, 'boardgamecafe/game.html', {'boardgame': boardgame, 'boardgame_love_count': boardgame_love_count, 'boardgame_review_count': boardgame_review_count, 'boardgame_review_rating': boardgame_review_rating,})
        comments = []
        for comment in all_comments:
            comment_love_count = comment.commentlove_set.filter(log_is_active=True).count()
            new_comment = {'id': comment.id, 'person': comment.person, 'text': comment.text, 'comment_love_count': comment_love_count, 'log_date_created': comment.log_date_created}
            comments.append(new_comment)
        return render(request, 'boardgamecafe/game.html', {'boardgame': boardgame, 'boardgame_love_count': boardgame_love_count, 'boardgame_review_count': boardgame_review_count, 'boardgame_review_rating': boardgame_review_rating, 'comments': comments,})
    # FAZER ALTERAÇÕES DE ACORDO COM POST
    if request.method == 'POST':
        love_boardgame = request.POST.get('love_boardgame')
        review_boardgame = request.POST.get('review_boardgame')
        love_comment = request.POST.get('love_comment')
        add_comment = request.POST.get('add_comment')
        if love_boardgame:
            if love_boardgame == "love":
                love = True
            else:
                love = False
            love_found = boardgame.boardgamelove_set.all().filter(person=request.user.person)
            if love_found:
                love_found[0].log_is_active = love
                love_found[0].save()
            else:
                boardgamelove = BoardGameLove(person=request.user.person, boardgame=boardgame, log_is_active=love, log_date_created=timezone.now(), log_date_last_update=timezone.now())
                boardgamelove.save()
        elif review_boardgame:
            review_found = boardgame.review_set.all().filter(person=request.user.person)
            if review_found:
                if int(review_boardgame) == review_found[0].rate:
                    review_found[0].log_is_active = not review_found[0].log_is_active
                else:
                    review_found[0].rate = review_boardgame
                    review_found[0].log_is_active = True
                review_found[0].save()
            else:
                review_to_add = Review(boardgame=boardgame, person=request.user.person, rate=review_boardgame, text="", log_is_active=True, log_date_created=timezone.now(), log_date_last_update=timezone.now())
                review_to_add.save()
        elif love_comment:
            splitlove = love_comment.split(" ")
            if splitlove[1] == "love":
                love = True
            else:
                love = False
            comment_to_love = Comment.objects.get(pk=splitlove[0]) # mensagem de erro? não é suposto dar erro...
            love_found = comment_to_love.commentlove_set.all().filter(person=request.user.person)
            if love_found:
                love_found[0].log_is_active = love
                love_found[0].save()
            else:
                commentlove = CommentLove(person=request.user.person, comment=comment_to_love, log_is_active=love, log_date_created=timezone.now(), log_date_last_update=timezone.now())
                commentlove.save()
        elif add_comment:
            comment_to_add = Comment(boardgame=boardgame, person=request.user.person, text=add_comment, log_is_active=True, log_date_created=timezone.now(), log_date_last_update=timezone.now())
            comment_to_add.save()
    # RECOLHER TODA A INFORMACAO NECESSARIA
    boardgame_love_count = boardgame.boardgamelove_set.filter(log_is_active=True).count()
    loved_boardgame = False
    love_exists_boardgame = boardgame.boardgamelove_set.all().filter(person=request.user.person)
    if love_exists_boardgame:
        loved_boardgame = love_exists_boardgame[0].log_is_active
    boardgame_reviews = boardgame.review_set.all().filter(log_is_active=True)
    boardgame_review_count = boardgame_reviews.count()
    boardgame_review_rating = 0
    if boardgame_review_count != 0:
        for review in boardgame_reviews:
            boardgame_review_rating += review.rate
        boardgame_review_rating = boardgame_review_rating / boardgame_review_count
    review_exists_boardgame = boardgame_reviews.filter(person=request.user.person)
    all_comments = boardgame.comment_set.all().filter(log_is_active=True).order_by('-log_date_created')
    if not all_comments:
        if review_exists_boardgame:
            return render(request, 'boardgamecafe/game.html', {'boardgame': boardgame, 'boardgame_love_count': boardgame_love_count, 'loved_boardgame': loved_boardgame, 'boardgame_review_count': boardgame_review_count, 'boardgame_review_rating': boardgame_review_rating, 'boardgame_user_review': review_exists_boardgame[0].rate,})
        return render(request, 'boardgamecafe/game.html',
                  {'boardgame': boardgame, 'boardgame_love_count': boardgame_love_count,
                   'loved_boardgame': loved_boardgame, 'boardgame_review_count': boardgame_review_count,
                   'boardgame_review_rating': boardgame_review_rating})
    comments = []
    for comment in all_comments:
        comment_love_count = comment.commentlove_set.filter(log_is_active=True).count()
        loved_comment = False
        love_exists_comment = comment.commentlove_set.all().filter(person=request.user.person)
        if love_exists_comment:
            loved_comment = love_exists_comment[0].log_is_active
        new_comment = {'id': comment.id, 'person': comment.person, 'text': comment.text, 'loved': loved_comment, 'comment_love_count': comment_love_count, 'log_date_created': comment.log_date_created}
        comments.append(new_comment)
    if review_exists_boardgame:
        return render(request, 'boardgamecafe/game.html', {'boardgame': boardgame, 'boardgame_love_count': boardgame_love_count, 'loved_boardgame': loved_boardgame, 'boardgame_review_count': boardgame_review_count, 'boardgame_review_rating': boardgame_review_rating, 'boardgame_user_review': review_exists_boardgame[0].rate, 'comments': comments,})
    return render(request, 'boardgamecafe/game.html',
                  {'boardgame': boardgame, 'boardgame_love_count': boardgame_love_count,
                   'loved_boardgame': loved_boardgame, 'boardgame_review_count': boardgame_review_count,
                   'boardgame_review_rating': boardgame_review_rating, 'comments': comments, })

@permission_required('boardgamecafe.add_boardgame', raise_exception=True)
@login_required
def addgame(request):
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

@permission_required('boardgamecafe.change_boardgame', raise_exception=True)
@login_required()
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
                  {'boardgame': boardgame, 'error_message': "Error editing board game. Be sure that all fields are filled correctly."})

@login_required
def titles(request):
    # RECECAO DE POST - user_id_title_id
    if request.method == 'POST':
        selected_user_id = request.POST.get('selected_user_id')
        selected_user = get_object_or_404(User, pk=selected_user_id)
        if not request.user.is_superuser and selected_user != request.user:
            selected_user = request.user
        show_edit = False;
    else:
        selected_user = request.user
        show_edit = True;
    if Title.objects.all().count() > 0:
        all_titles = Title.objects.all()
        titles = []
        for title in all_titles:
            new_title = {'id': title.id, 'designation': title.designation, 'unlock_conditions': title.unlock_conditions, 'unlocked': selected_user.person.unlocked_titles.filter(pk=title.id).exists(), 'log_is_active': title.log_is_active}
            titles.append(new_title)
        return render(request, 'boardgamecafe/titles.html', {'selected_user': selected_user, 'titles': titles, 'show_edit': show_edit,})
    return render(request, 'boardgamecafe/titles.html', {'selected_user': selected_user, 'show_edit': show_edit,})

@permission_required('boardgamecafe.add_title', raise_exception=True)
@login_required
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

@permission_required('boardgamecafe.edit_title', raise_exception=True)
@login_required
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
    if designation and unlock_conditions and designation != "None":
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
                  {'title': title, 'error_message': "Error editing title. Be sure that all fields are filled correctly. Note that title 'None' can not be changed"})

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
        return HttpResponseRedirect(reverse('boardgamecafe:tables'))
    return render(request, 'boardgamecafe/managetable.html', {'table': table, 'error_message': "Error editing table. Be sure that all fields are filled correctly."})


def calendar(request):
    # Vai buscar todas as mesas à base de dados
    tables_list = Table.objects.all().filter(log_is_active=True)
    # Vai buscar a data de hoje e coloca no formato yyyy-mm-dd (output é strin)
    today_str = datetime.strftime(datetime.now(), '%Y-%m-%d')
    # Coloca no formato datetime.date
    today_date = datetime.strptime(today_str, '%Y-%m-%d').date()
    date = Calendar.objects.filter(date=today_date).values('id', 'date', 'open_time', 'close_time', 'log_is_active')
    # Vai buscar os slots para a data
    if date.count() > 0:
        for d in date:
            if d['log_is_active']:
                slots_list = allslots(date)
                # Vai buscar reservas à base de dados para o dia actual
                booking_list = Booking.objects.all().filter(log_is_active=True).filter(calendar_id=int(d['id']))
                calendar_list = getCalendar(slots_list, tables_list, booking_list)
                return render(request, 'boardgamecafe/calendar.html', {'date': today_date, 'dateobj': date, 'calendar_list': calendar_list})
            else:
                return render(request, 'boardgamecafe/calendar.html', {'date': today_date})
    else:
        return render(request, 'boardgamecafe/calendar.html', {'date': today_date})


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
                aux2 = datetime.strptime(aux, '%H:%M').time()
                slots_list.append(aux2)
    return slots_list

def nextdate(request, date_str, ispreviousdate_int):
    tables_list = Table.objects.all().filter(log_is_active=True)
    if ispreviousdate_int == 1:
        nextdate = newdate(date_str, True)
    else:
        nextdate = newdate(date_str, False)
    date = Calendar.objects.filter(date=nextdate).values('id', 'date', 'open_time', 'close_time', 'log_is_active')
    if date.count() > 0:
        for d in date:
            if d['log_is_active']:
                slots_list = allslots(date)
                booking_list = Booking.objects.all().filter(log_is_active=True).filter(calendar_id=int(d['id']))
                calendar_list = getCalendar(slots_list, tables_list, booking_list)
                return render(request, 'boardgamecafe/calendar.html', {'date': nextdate, 'dateobj': date, 'calendar_list': calendar_list})
            else:
                return render(request, 'boardgamecafe/calendar.html', {'date': nextdate})
    else:
        return render(request, 'boardgamecafe/calendar.html', {'date': nextdate})



def getCalendar(slots_list, tables_list, booking_list):
    calendar_list = []
    global there_is_booking
    there_is_booking = False
    for s in slots_list:
        for t in tables_list:
            if booking_list:
                count = 0
                for b in booking_list:
                    count = count + 1
                    if t.id == b.table_id and b.start_time <= s and b.end_time > s:
                        person = Person.objects.filter(id=b.person_id)
                        for p in person:
                            row = {'slot': s, 'name': t.name, 'link': str(b.id), 'nickname': p.nickname}
                            calendar_list.append(row)  # quando existe reserva
                        break
                    if count == len(booking_list):
                        row = {'slot': s, 'name': t.name, 'link': "Free", 'nickname': ""}
                        calendar_list.append(row)  # quando existe reserva
            else:
                row = {'slot': s, 'name': t.name, 'link': "Free", 'nickname': ""}
                calendar_list.append(row)  # quando existe reserva
    return calendar_list




def tables(request):
    if Table.objects.all().count() > 0:
        tables = Table.objects.all()
        return render(request, 'boardgamecafe/tables.html', {'tables': tables})
    return render(request, 'boardgamecafe/tables.html')


data_booking = []
def newbooking(request):
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/newbooking.html')
    global data_booking
    data_booking = []
    data_booking.append(request.POST.get('date'))
    data_booking.append(request.POST.get('starttime'))
    data_booking.append(request.POST.get('endtime'))
    data_booking.append(request.POST.get('players'))
    data_booking.append(request.POST.get('age'))
    # print(data_booking)
    # Procura o id do calendário para a data escolhida pelo utilizador
    start_hour = data_booking[1].split(':')[0]
    end_hour = data_booking[2].split(':')[0]
    date_obj = getcalendardate(start_hour, end_hour)
    date_id = []
    for d in date_obj:
        date_id = d["id"]
    # print(date_obj)
    # Procura as reservas para a data hora escolhida pelo utilizador
    if date_id:
        booking_date = getbookings(start_hour, end_hour, date_id)
        # Lista das mesas ocupadas
        not_available_tables_list = []
        for b in booking_date:
            not_available_tables_list.append(b['table_id'])
        # Lista das mesas não ocupadas que verificam o número de jogadores
        available_tables_list = []
        # tables_list = alltables()
        tables_list = Table.objects.all()
        for i in tables_list:
            if i.id not in not_available_tables_list and i.log_is_active and i.capacity >= int(data_booking[3]):
                available_tables_list.append(i)
        # print(available_tables_list)
        return render(request, 'boardgamecafe/newbooking2.html', {'tables': available_tables_list})
    return render(request, 'boardgamecafe/newbooking2.html')


data_booking2 = []
def newbooking2(request):
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/newbooking2.html')
    global data_booking2
    data_booking2 = []
    # print(data_booking2)
    data_booking2.append(request.POST.get('chosen_table'))
    # print(data_booking2)
    # Procura o id do calendário para a data escolhida pelo utilizador
    start_hour = data_booking[1].split(':')[0]
    end_hour = data_booking[2].split(':')[0]
    date_obj = getcalendardate(start_hour, end_hour)
    date_id = []
    for d in date_obj:
        date_id = d["id"]
    # print(date_obj)
    # Procura as reservas para a data hora escolhida pelo utilizador
    if date_id:
        booking_date = getbookings(start_hour, end_hour, date_id)
        # Lista dos jogos ocupados
        not_available_games_list = []
        for b in booking_date:
            not_available_games_list.append(b['boardgame_id'])
        # Lista dos jogos não ocupados
        available_games_list = []
        games_list = BoardGame.objects.all()
        for i in games_list:
            count_game = not_available_games_list.count(i.id)
            time_available = (int(end_hour) - int(start_hour)) * 60
            if count_game < i.number_of_copies and i.log_is_active and i.min_playing_time <= time_available and i.min_age <= int(data_booking[4]) and i.min_players <= int(data_booking[3]) and i.max_players >= int(data_booking[3]):
                available_games_list.append(i)
        # print(available_games_list)
        return render(request, 'boardgamecafe/newbooking3.html', {'boardgames': available_games_list})
    return render(request, 'boardgamecafe/newbooking3.html')


# Procura calendário para a data escolhida pelo utilizador
def getcalendardate(start_hour, end_hour):
    return Calendar.objects.filter(date=data_booking[0]).filter(open_time__hour__lte=start_hour).\
        filter(close_time__hour__gte=end_hour).filter(log_is_active=True).\
        values('id', 'date', 'open_time', 'close_time','log_is_active')


# Procura as reservas para a data hora escolhida pelo utilizador
def getbookings(start_hour, end_hour, date_id):
    # Reservas que começam antes e terminam depois
    booking_date1 = Booking.objects.all().filter(calendar_id=date_id).filter(start_time__hour__lte=start_hour).\
        filter(end_time__hour__gte=end_hour).filter(log_is_active=True).\
        values('id', 'start_time', 'end_time', 'calendar_id', 'table_id', 'boardgame_id', 'log_is_active')
    # Reservas que começam depois e terminam antes
    booking_date2 = Booking.objects.all().filter(calendar_id=date_id).filter(start_time__hour__gte=start_hour).\
        filter(end_time__hour__lte=end_hour).filter(log_is_active=True).\
        values('id', 'start_time', 'end_time', 'calendar_id', 'table_id', 'boardgame_id', 'log_is_active')
    # Reservas que começam antes e terminam antes
    booking_date3 = Booking.objects.all().filter(calendar_id=date_id).filter(start_time__hour__lte=start_hour).\
        filter(end_time__hour__gte=start_hour).filter(end_time__hour__lte=end_hour).filter(log_is_active=True).\
        values('id', 'start_time', 'end_time', 'calendar_id', 'table_id', 'boardgame_id', 'log_is_active')
    # Reservas que começão depois e terminam depois
    booking_date4 = Booking.objects.all().filter(calendar_id=date_id).filter(start_time__hour__gte=start_hour).\
        filter(start_time__hour__lte=end_hour).filter(end_time__hour__gte=end_hour).filter(log_is_active=True).\
        values('id', 'start_time', 'end_time', 'calendar_id', 'table_id', 'boardgame_id', 'log_is_active')
    # União das 4 queries
    return booking_date1 | booking_date2 | booking_date3 | booking_date4


data_booking3 = []
def newbooking3(request):
    if not request.method == 'POST':
        return render(request, 'boardgamecafe/newbooking3.html')
    global data_booking3
    data_booking3 = []
    # print(data_booking3)
    data_booking3.append(request.POST.get('chosen_game'))
    # print(data_booking3)
    print("data_booking", data_booking)
    print("data_booking2", data_booking2)
    print("data_booking3", data_booking3)
    date = datetime.strptime(data_booking[0], '%Y-%m-%d').date()
    table_obj = Table.objects.filter(id=data_booking2[0])
    table_name = []
    for i in table_obj:
        table_name = i.name
    game_obj = BoardGame.objects.filter(id=data_booking3[0])
    game_name = []
    for i in game_obj:
        game_name = i.name
    return render(request, 'boardgamecafe/newbooking4.html', {'date': date,'start_time': data_booking[1], 'end_time': data_booking[2], 'boardgame': game_name, 'table': table_name})


def newbooking4(request):
    # Procura o id do calendário para a data escolhida pelo utilizador
    start_hour = data_booking[1].split(':')[0]
    end_hour = data_booking[2].split(':')[0]
    date_obj = getcalendardate(start_hour, end_hour)
    date_id = []
    for d in date_obj:
        date_id = d["id"]
    # Dados para criar reserva
    start_time = datetime.strptime(data_booking[1], '%H:%M').time()
    end_time = datetime.strptime(data_booking[2], '%H:%M').time()
    value_paid = 0
    is_paid = False
    log_is_active = True
    log_date_created = datetime.now()
    log_date_last_update = datetime.now()
    boardgame_id = int(data_booking3[0])
    calendar_id = date_id
    person_id = request.user.person.id
    table_id = int(data_booking2[0])
    # Procura o id do calendário para a data escolhida pelo utilizador
    start_hour = data_booking[1].split(':')[0]
    end_hour = data_booking[2].split(':')[0]
    date_obj = getcalendardate(start_hour, end_hour)
    date_id = []
    for d in date_obj:
        date_id = d["id"]
    # Procura as reservas para a data hora escolhida pelo utilizador
    if date_id:
        booking_date = getbookings(start_hour, end_hour, date_id)
        # Lista das mesas ocupadas e dos jogos ocupados
        not_available_tables_list = []
        not_available_games_list = []
        for b in booking_date:
            not_available_tables_list.append(b['table_id'])
            not_available_games_list.append(b['boardgame_id'])
        # Verifica disponibilidade da mesa
        if table_id in not_available_tables_list:
            return render(request, 'boardgamecafe/bookingerror.html')
        # Verifica disponibilidade do jogo
        count_game = not_available_games_list.count(boardgame_id)
        boardgame = BoardGame.objects.filter(id=boardgame_id)
        for b in boardgame:
            if count_game >= b.number_of_copies:
                return render(request, 'boardgamecafe/bookingerror.html')
    # Cria reserva
    booking = Booking(start_time=start_time, end_time=end_time, value_paid=value_paid, is_paid=is_paid,
                      log_is_active=log_is_active, log_date_created=log_date_created,
                      log_date_last_update=log_date_last_update, boardgame_id=boardgame_id, calendar_id=calendar_id,
                      person_id=person_id, table_id=table_id)
    booking.save()
    return render(request, 'boardgamecafe/index.html')


def bookingerror(request):
    return render(request, 'boardgamecafe/bookingerror.html')











# ADMIN USERS CHECK SECTION

@permission_required('view_user', raise_exception=True)
@login_required
def users(request):
    users = User.objects.all().order_by('person__nickname')
    return render(request, 'boardgamecafe/users.html',
                  {'users': users, })

#superuser defaults to true in permissions regardless of its existance
@permission_required('add_user', raise_exception=True)
@login_required
def createuser(request):
    if not request.method == 'POST':
        titles = Title.objects.all().filter(unlock_conditions__exact="None", log_is_active__exact=True)
        return render(request, 'boardgamecafe/signup.html', {'titles': titles})
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    nickname = request.POST.get('nickname')
    chosen_title_id = request.POST.get('chosen_title') # REVER
    date_of_birth = request.POST.get('date_of_birth')
    email = request.POST.get('email')
    vat = request.POST.get('vat')
    phone_number = request.POST.get('phone_number')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')
    if first_name and last_name and nickname and chosen_title_id and date_of_birth and email and vat and phone_number and username and password and password_confirm:
        error_message = "Error registering new user. "
        error_occured = False
        all_users = User.objects.all()
        for user in all_users:
            if user.username == username:
                if error_occured:
                    error_message += "<br>"
                error_occured = True
                error_message += "The username " + username + " already exists."
            if user.email == email:
                if error_occured:
                    error_message += "<br>"
                error_occured = True
                error_message += "The email " + email + " already exists."
        if password != password_confirm:
            if error_occured:
                error_message += "<br>"
            error_occured = True
            error_message += "The password does not match the confirmation password."
        try:
            chosen_title = Title.objects.get(pk=chosen_title_id)
        except Title.DoesNotExist:
            if error_occured:
                error_message += "<br>"
            error_occured = True
            error_message += "The chosen title does not exist."
        if not error_occured:
            if request.POST.get('is_superuser'):
                new_user = User.objects.create_superuser(username, email, password)
            else:
                new_user = User.objects.create_user(username, email, password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()
            person = Person(user=new_user, nickname=nickname, chosen_title=chosen_title, date_of_birth=date_of_birth, vat=vat, phone_number=phone_number, log_is_active=True, log_date_created=timezone.now(), log_date_last_update=timezone.now())
            person.save()
            titles = Title.objects.all().filter(unlock_conditions__exact="None")
            for title in titles:
                person.unlocked_titles.add(title)
            return HttpResponseRedirect(reverse('boardgamecafe:index'))
        return render(request, 'boardgamecafe/signup.html', {'error_message': error_message})
    return render(request, 'boardgamecafe/signup.html', {'error_message': "Error registering new user. Be sure that all fields are filled correctly."})





# SIGN IN, SIGN UP AND PERSONAL DATA SECTION
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('boardgamecafe:index'))
    if not request.method == 'POST':
        titles = Title.objects.all().filter(unlock_conditions__exact="None", log_is_active__exact=True)
        return render(request, 'boardgamecafe/signup.html', {'titles': titles})
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    nickname = request.POST.get('nickname')
    chosen_title_id = request.POST.get('chosen_title')
    date_of_birth = request.POST.get('date_of_birth')
    email = request.POST.get('email')
    vat = request.POST.get('vat')
    phone_number = request.POST.get('phone_number')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')
    if first_name and last_name and nickname and chosen_title_id and date_of_birth and email and vat and phone_number and username and password and password_confirm:
        error_message = "Error registering new user. "
        error_occured = False
        all_users = User.objects.all()
        for user in all_users:
            if user.username == username:
                if error_occured:
                    error_message += "<br>"
                error_occured = True
                error_message += "The username " + username + " already exists."
            if user.email == email:
                if error_occured:
                    error_message += "<br>"
                error_occured = True
                error_message += "The email " + email + " already exists."
        if password != password_confirm:
            if error_occured:
                error_message += "<br>"
            error_occured = True
            error_message += "The password does not match the confirmation password."
        try:
            chosen_title = Title.objects.get(pk=chosen_title_id)
        except Title.DoesNotExist:
            if error_occured:
                error_message += "<br>"
            error_occured = True
            error_message += "The chosen title does not exist."
        if not error_occured:
            if request.POST.get('is_superuser'):
                new_user = User.objects.create_superuser(username, email, password)
            else:
                new_user = User.objects.create_user(username, email, password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()
            person = Person(user=new_user, nickname=nickname, chosen_title=chosen_title, date_of_birth=date_of_birth, vat=vat, phone_number=phone_number, log_is_active=True, log_date_created=timezone.now(), log_date_last_update=timezone.now())
            person.save()
            titles = Title.objects.all().filter(unlock_conditions__exact="None")
            for title in titles:
                person.unlocked_titles.add(title)
            login(request, new_user)
            return HttpResponseRedirect(reverse('boardgamecafe:index'))
        return render(request, 'boardgamecafe/signup.html', {'error_message': error_message})
    return render(request, 'boardgamecafe/signup.html', {'error_message': "Error registering new user. Be sure that all fields are filled correctly."})

def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('boardgamecafe:index'))
    if not request.method == 'POST':
      return render(request, 'boardgamecafe/signin.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username and password:
      user = authenticate(username=username, password=password)
      if user is not None:
          login(request, user)
          return HttpResponseRedirect(reverse('boardgamecafe:index'))
    return render(request, 'boardgamecafe/signin.html', {'error_message': "Error signing in. The username and password don't match. Try again."})

@login_required
def signout(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect(reverse('boardgamecafe:index'))

@login_required
def personalarea(request):
    return render(request, 'boardgamecafe/personalarea.html')

@login_required
def userdetails(request):
    if not request.method == 'POST':
      selected_user_id = request.user.id
    else:
        selected_user_id = request.POST.get('selected_user_id')
    if selected_user_id:
        selected_user = get_object_or_404(User, pk=selected_user_id)
        if not request.user.is_superuser and selected_user != request.user:
            selected_user = request.user
        titles = selected_user.person.unlocked_titles.filter(log_is_active__exact=True)
        date_of_birth = selected_user.person.date_of_birth.strftime('%Y-%m-%d')
        return render(request, 'boardgamecafe/userdetails.html', {'user_to_view': selected_user, 'titles': titles, 'date_of_birth': date_of_birth,})
    user_id = request.POST.get('user_id')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    nickname = request.POST.get('nickname')
    chosen_title_id = request.POST.get('chosen_title')
    date_of_birth = request.POST.get('date_of_birth')
    email = request.POST.get('email')
    vat = request.POST.get('vat')
    phone_number = request.POST.get('phone_number')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')
    if user_id and first_name and last_name and nickname and chosen_title_id and date_of_birth and email and vat and phone_number and username:
        error_message = "Error editing user. "
        error_occured = False
        if not request.user.is_superuser and user_id != request.user.id:
            user_id = request.user.id
        user_to_edit = User.objects.get(pk=user_id)
        if not user_to_edit:
            error_message += "Showing your user details."
            titles = request.user.person.unlocked_titles.filter(log_is_active__exact=True)
            date_of_birth = request.user.person.date_of_birth.strftime('%Y-%m-%d')
            return render(request, 'boardgamecafe/userdetails.html',
                          {'error_message': error_message,
                           'user_to_view': request.user, 'titles': titles, 'date_of_birth': date_of_birth, })
        if user_to_edit.username != username or user_to_edit.email != email:
            all_users = User.objects.all()
            for user in all_users:
                if user_to_edit.username != username:
                    if user.username == username:
                        error_occured = True
                        error_message += "The username " + username + " already exists."
                if user_to_edit.email != email:
                    if user.email == email:
                        error_occured = True
                        error_message += "The email " + email + " already exists."
        if password and password_confirm:
            if password != password_confirm:
                error_occured = True
                error_message += "The password does not match the confirmation password."
        try:
            chosen_title = Title.objects.get(pk=chosen_title_id)
        except Title.DoesNotExist:
            error_occured = True
            error_message += "The chosen title does not exist."
        if not error_occured:
            user_to_edit.username = username
            user_to_edit.email = email
            if password and password_confirm:
                user_to_edit.set_password(password)
            user_to_edit.first_name = first_name
            user_to_edit.last_name = last_name
            user_to_edit.save()
            user_to_edit.person.nickname=nickname
            user_to_edit.person.chosen_title=chosen_title
            user_to_edit.person.date_of_birth=date_of_birth
            user_to_edit.person.vat=vat
            user_to_edit.person.phone_number=phone_number
            user_to_edit.person.log_date_last_update=timezone.now()
            user_to_edit.person.save()
            titles = user_to_edit.person.unlocked_titles.filter(log_is_active__exact=True)
            return render(request, 'boardgamecafe/userdetails.html',
                          {'user_to_view': user_to_edit, 'titles': titles, 'date_of_birth': date_of_birth, })
        titles = user_to_edit.person.unlocked_titles.filter(log_is_active__exact=True)
        date_of_birth = user_to_edit.person.date_of_birth.strftime('%Y-%m-%d')
        return render(request, 'boardgamecafe/userdetails.html', {'error_message': error_message, 'user_to_view': user_to_edit, 'titles': titles, 'date_of_birth': date_of_birth,})
    titles = request.user.person.unlocked_titles.filter(log_is_active__exact=True)
    date_of_birth = request.user.person.date_of_birth.strftime('%Y-%m-%d')
    return render(request, 'boardgamecafe/userdetails.html',
                  {'error_message': "Error editing user. Showing your user details.", 'user_to_view': request.user, 'titles': titles, 'date_of_birth': date_of_birth,})

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
