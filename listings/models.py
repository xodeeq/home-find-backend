from django.db import models


class Property(models.Model):
    APARTMENT = "Apartment"
    HOUSE = "House"
    CONDO = "Condo"
    STUDIO = "Studio"
    COMMERCIAL = "Commercial"

    PROPERTY_TYPES = {
        APARTMENT: APARTMENT,
        HOUSE: HOUSE,
        CONDO: CONDO,
        STUDIO: STUDIO,
        COMMERCIAL: COMMERCIAL,
    }

    NAIRA = "NGN"
    DOLLAR = "USD"
    EURO = "EUR"
    POUND = "GBP"

    CURRENCIES = {
        NAIRA: "₦",
        DOLLAR: "$",
        EURO: "€",
        POUND: "£",
    }

    ONE = "1"
    ONE_POINT_FIVE = "1.5"
    TWO = "2"
    TWO_POINT_FIVE = "2.5"
    THREE = "3"
    THREE_POINT_FIVE = "3.5"
    FOUR = "4"
    FOUR_PLUS = "4+"
    FIVE_PLUS = "5+"

    BEDROOMS = {
        STUDIO: STUDIO,
        ONE: ONE,
        TWO: TWO,
        THREE: THREE,
        FOUR: FOUR,
        FIVE_PLUS: FIVE_PLUS,
    }

    BATHROOMS = {
        ONE: ONE,
        ONE_POINT_FIVE: ONE_POINT_FIVE,
        TWO: TWO,
        TWO_POINT_FIVE: TWO_POINT_FIVE,
        THREE: THREE,
        THREE_POINT_FIVE: THREE_POINT_FIVE,
        FOUR_PLUS: FOUR_PLUS,
    }

    AMENITY_LABELS = {
        "swimming_pool": "Swimming Pool",
        "gym": "Gym",
        "parking": "Parking",
        "balcony": "Balcony",
        "garden": "Garden",
        "air_conditioning": "Air Conditioning",
        "heating": "Heating",
        "fireplace": "Fireplace",
        "walk_in_closet": "Walk-in Closet",
        "dishwasher": "Dishwasher",
        "washer_dryer": "Washer/Dryer",
        "elevator": "Elevator",
        "security_system": "Security System",
    }

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    bedrooms = models.CharField(choices=BEDROOMS)
    bathrooms = models.CharField(choices=BATHROOMS)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    area = models.IntegerField(help_text="Area in square feet", blank=True, null=True)
    image = models.URLField(max_length=200, blank=True)

    # Amenities
    swimming_pool = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    garden = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    heating = models.BooleanField(default=False)
    fireplace = models.BooleanField(default=False)
    walk_in_closet = models.BooleanField(default=False)
    dishwasher = models.BooleanField(default=False)
    washer_dryer = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    security_system = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = "properties"

    def __str__(self):
        return self.title
    
    @classmethod
    def get_reverse_amenity_labels(cls):
        return {v: k for k, v in cls.AMENITY_LABELS.items()}