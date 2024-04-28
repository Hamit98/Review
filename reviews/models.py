from django.db import models
from django.contrib.auth.models import User

class Establishment(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True)
    average_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Rating(models.Model):
    rating_count = models.IntegerField()

    def __str__(self):
        return str(self.rating_count)

class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    review_text = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.establishment.name}"

