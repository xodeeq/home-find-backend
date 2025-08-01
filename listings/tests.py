from django.test import TestCase
from .models import Property

class PropertyModelTest(TestCase):

    def setUp(self):
        Property.objects.create(
            title="Modern Downtown Loft",
            description="A beautiful loft in the heart of downtown.",
            price=2500,
            location="Downtown District",
            bedrooms=2,
            bathrooms=2,
            area=1200,
            image="photo-1460574283810-2aab119d8511"
        )

    def test_property_creation(self):
        property = Property.objects.get(title="Modern Downtown Loft")
        self.assertEqual(property.description, "A beautiful loft in the heart of downtown.")
        self.assertEqual(property.price, 2500)
        self.assertEqual(property.location, "Downtown District")
        self.assertEqual(property.bedrooms, 2)
        self.assertEqual(property.bathrooms, 2)
        self.assertEqual(property.area, 1200)
        self.assertEqual(property.image, "photo-1460574283810-2aab119d8511")

    def test_property_str(self):
        property = Property.objects.get(title="Modern Downtown Loft")
        self.assertEqual(str(property), "Modern Downtown Loft")