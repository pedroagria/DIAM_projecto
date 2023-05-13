from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
#from django.utils import timezone

# tenho pena de não ter nenhuma relação muitos para muitos (algo a pensar!)

class BoardGame(models.Model):
    name = models.CharField(max_length=50)
    release_year = models.IntegerField(validators=[MaxValueValidator(3000)])
    min_players = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    max_players = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    min_age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    min_playing_time = models.IntegerField(validators=[MinValueValidator(1)])
    avg_playing_time = models.IntegerField(validators=[MinValueValidator(1)])
    complexity = models.DecimalField(validators=[MinValueValidator(1), MaxValueValidator(5)], max_digits=3, decimal_places=2)
    number_of_copies = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    link = models.URLField() #default 200 character limit (can be changed)
    image = models.ImageField()  # para adicionar imagens. Talvez seja preciso a Pillow library. We'll see.
    log_is_active = models.BooleanField() # mudei o nome de isActive para isto
    log_date_created = models.DateTimeField() # adicionei para ficar com histórico de criação
    log_date_last_update = models.DateTimeField() # adicionei para se saber quando alguém mexeu

class Title(models.Model):
    designation = models.CharField(max_length=50, unique=True)
    unlock_conditions = models.TextField()
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Person(models.Model):
    # possivelmente associar users a isto e colocar algum tipo de pontos
    # name = models.CharField(max_length=100) #user já tem
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    unlocked_titles = models.ManyToManyField('Title', related_name='people')
    chosen_title = models.ForeignKey(Title, on_delete=models.RESTRICT)
    date_of_birth = models.DateField()
    # email = models.EmailField(unique=True)
    vat = models.CharField(max_length=15)
    phone_number_regex = RegexValidator(regex='^([0]{2}[1-9]{1,3})?([\+][0-9]{1,3})?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{3,6}$', message ="One of the accepted formats is +351919560372") # REVER
    phone_number = models.CharField(validators=[phone_number_regex], max_length=16) #blank=true se quisermos que o campo possa ficar vazio
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField() #alterei o signupdate para ficar como este
    log_date_last_update = models.DateTimeField()

class Comment(models.Model):
    boardgame = models.ForeignKey(BoardGame, on_delete=models.RESTRICT)
    person = models.ForeignKey(Person, on_delete=models.RESTRICT)
    text = models.TextField()
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Review(models.Model):
    boardgame = models.ForeignKey(BoardGame, on_delete=models.RESTRICT)
    person = models.ForeignKey(Person, on_delete=models.RESTRICT)
    rate = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(5)], max_digits=2, decimal_places=1)
    text = models.TextField() # TIRAR?
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Table(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(validators=[MinValueValidator(0)])
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Product(models.Model): # fez-me sentido mudar o titulo para produto invés de price e fazer a gestão pelo produto
    name = models.CharField(max_length=50)
    price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2) # dá 99999.99 euros, acho que mesmo na loucura é suficiente para o efeito
    stock_quantity = models.IntegerField()
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Calendar(models.Model):
    date = models.DateField()
    open_time = models.TimeField()
    close_time = models.TimeField() # mudei de end para close
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Booking(models.Model):
    person = models.ForeignKey(Person, on_delete=models.RESTRICT)
    boardgame = models.ForeignKey(BoardGame, on_delete=models.RESTRICT) # tenho ideia que tinhamos decidido que em cada reserva só se podia reservar um jogo de tabuleiro (mesmo que depois se usassem outros disponíveis)
    table = models.ForeignKey(Table, on_delete=models.RESTRICT)
    calendar = models.ForeignKey(Calendar, on_delete=models.RESTRICT)
    start_time = models.TimeField()
    end_time = models.TimeField()
    booking_price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)
    total_price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)
    value_paid = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2) # dá 99999.99 euros, acho que mesmo na loucura é suficiente para o efeito
    is_paid = models.BooleanField()
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()


class Order(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.IntegerField()
    total_price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2) # adicionei para guardar o preço no momento em que se faz a order (mesmo que o preço mude no segundo seguinte, está o preço total antigo)
    is_preorder = models.BooleanField()
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class BoardGameLove(models.Model):
    person = models.ForeignKey(Person, on_delete=models.RESTRICT)
    boardgame = models.ForeignKey(BoardGame, on_delete=models.RESTRICT)
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class CommentLove(models.Model):
    person = models.ForeignKey(Person, on_delete=models.RESTRICT)
    comment = models.ForeignKey(Comment, on_delete=models.RESTRICT)
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()
