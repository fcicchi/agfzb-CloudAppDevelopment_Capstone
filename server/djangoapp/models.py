from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=200)

    def __str__(self):
        return 'name= ' + self.name + ', desc= ' + self.desc

class CarModel(models.Model):
    
    TYPE_CHOICES = (
        ('SEDAN', "SEDAN"),
        ('SUV', "SUV"),
        ('WAGON', "WAGON"),
        ('OTHER', "OTHER"),
    )

    model_id = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length=10, choices=TYPE_CHOICES) 
    year = models.DateField()

    def __str__(self):
        return 'name=' + self.name

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    def __init__(self,dealership,name,purchase,review,purchase_date,car_make,car_model,car_year,sentiment):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Dealer name: " + self.name