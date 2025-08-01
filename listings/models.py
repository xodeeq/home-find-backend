from django.db import models


class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.IntegerField(help_text="Area in square feet")
    image = models.URLField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "properties"

    def __str__(self):
        return self.title