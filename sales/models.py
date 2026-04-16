from django.db import models


class Sale(models.Model):
    date = models.DateField()
    product = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    total = models.FloatField()

    def __str__(self):
        return f"{self.product} - {self.total}"
