from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

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
    link = models.URLField()
    image = models.ImageField()
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Title(models.Model):
    designation = models.CharField(max_length=50, unique=True)
    unlock_conditions = models.TextField()
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    unlocked_titles = models.ManyToManyField('Title', related_name='people')
    chosen_title = models.ForeignKey(Title, on_delete=models.RESTRICT)
    date_of_birth = models.DateField()
    vat = models.CharField(max_length=15)
    phone_number_regex = RegexValidator(regex='^([0]{2}[1-9]{1,3})?([\+][0-9]{1,3})?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{3,6}$', message ="One of the accepted formats is +351919560372")
    phone_number = models.CharField(validators=[phone_number_regex], max_length=16)
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
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
    text = models.TextField()
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Table(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(validators=[MinValueValidator(0)])
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)
    stock_quantity = models.IntegerField()
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Calendar(models.Model):
    date = models.DateField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()

class Booking(models.Model):
    person = models.ForeignKey(Person, on_delete=models.RESTRICT)
    boardgame = models.ForeignKey(BoardGame, on_delete=models.RESTRICT)
    table = models.ForeignKey(Table, on_delete=models.RESTRICT)
    calendar = models.ForeignKey(Calendar, on_delete=models.RESTRICT)
    start_time = models.TimeField()
    end_time = models.TimeField()
    booking_price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)
    total_price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)
    value_paid = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)
    is_paid = models.BooleanField()
    log_is_active = models.BooleanField()
    log_date_created = models.DateTimeField()
    log_date_last_update = models.DateTimeField()


class Order(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.IntegerField()
    total_price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)
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
