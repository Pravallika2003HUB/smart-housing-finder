"""Create demo users, sample properties and sample reviews.

Usage:  python manage.py seed_data
"""
from django.core.management.base import BaseCommand

from accounts.models import User
from properties.models import Property
from reviews.models import Review

OWNER = {"email": "owner@demo.com", "full_name": "Suresh Kumar", "phone": "9000000002", "role": User.OWNER}
STUDENT = {"email": "student@demo.com", "full_name": "Ananya Rao", "phone": "9000000001", "role": User.STUDENT}
ADMIN = {"email": "admin@demo.com", "full_name": "Platform Admin", "phone": "9000000003", "role": User.ADMIN}
PASSWORD = "Shf#Housing2026x"

PROPERTIES = [
    dict(title="Comfort Stay PG", property_type="PG", location="Visakhapatnam",
         address="12-4-9 Beach Road, MVP Colony, Visakhapatnam 530017", monthly_rent=6500,
         security_deposit=10000, gender_preference="Any", food_available=True, wifi_available=True,
         parking_available=True, laundry_available=True, furnished=True, contact_number="+91 90000 11111",
         description="Well maintained PG close to Andhra University with home style meals.", is_verified=True),
    dict(title="Student Nest Hostel", property_type="Hostel", location="Hyderabad",
         address="Plot 44, Gachibowli, Hyderabad 500032", monthly_rent=8200, security_deposit=12000,
         gender_preference="Male", food_available=True, wifi_available=True, parking_available=False,
         laundry_available=True, furnished=True, contact_number="+91 90000 22222",
         description="Hostel for students near the IT corridor with study rooms and 24x7 security.", is_verified=True),
    dict(title="City View Rooms", property_type="Room", location="Bengaluru",
         address="5th Cross, Koramangala, Bengaluru 560034", monthly_rent=11500, security_deposit=20000,
         gender_preference="Any", food_available=False, wifi_available=True, parking_available=True,
         laundry_available=False, furnished=True, contact_number="+91 90000 33333",
         description="Private rooms with attached bathroom, walking distance to metro feeder bus.", is_verified=True),
    dict(title="Campus Stay PG", property_type="PG", location="Chennai",
         address="22 Velachery Main Road, Chennai 600042", monthly_rent=7400, security_deposit=9000,
         gender_preference="Female", food_available=True, wifi_available=True, parking_available=False,
         laundry_available=True, furnished=True, contact_number="+91 90000 44444",
         description="Ladies PG with warden, CCTV and vegetarian meals included in rent.", is_verified=True),
    dict(title="Budget Home for Students", property_type="Room", location="Vijayawada",
         address="Gunadala, Vijayawada 520004", monthly_rent=5200, security_deposit=6000,
         gender_preference="Any", food_available=False, wifi_available=True, parking_available=True,
         laundry_available=False, furnished=False, contact_number="+91 90000 55555",
         description="Affordable unfurnished rooms suitable for students on a tight budget.", is_verified=False),
        dict(
        title="Vizag Student PG",
        property_type="PG",
        location="Visakhapatnam",
        address="Dwaraka Nagar, Visakhapatnam 530016",
        monthly_rent=7000,
        security_deposit=10000,
        gender_preference="Any",
        food_available=True,
        wifi_available=True,
        parking_available=True,
        laundry_available=True,
        furnished=True,
        contact_number="9000010001",
        description="Comfortable PG accommodation for students and working professionals.",
        is_verified=True
    ),

    dict(
        title="MVP Girls PG",
        property_type="PG",
        location="Visakhapatnam",
        address="MVP Colony, Visakhapatnam 530017",
        monthly_rent=7500,
        security_deposit=10000,
        gender_preference="Female",
        food_available=True,
        wifi_available=True,
        parking_available=True,
        laundry_available=True,
        furnished=True,
        contact_number="9000010002",
        description="Safe and comfortable PG for female students and professionals.",
        is_verified=True
    ),

    dict(
        title="Madhurawada Student Hostel",
        property_type="Hostel",
        location="Visakhapatnam",
        address="Madhurawada, Visakhapatnam 530048",
        monthly_rent=6000,
        security_deposit=8000,
        gender_preference="Any",
        food_available=True,
        wifi_available=True,
        parking_available=True,
        laundry_available=True,
        furnished=True,
        contact_number="9000010003",
        description="Affordable hostel with essential facilities for students.",
        is_verified=True
    ),

    dict(
        title="Gajuwaka Comfort PG",
        property_type="PG",
        location="Visakhapatnam",
        address="Gajuwaka, Visakhapatnam 530026",
        monthly_rent=5500,
        security_deposit=8000,
        gender_preference="Male",
        food_available=True,
        wifi_available=True,
        parking_available=True,
        laundry_available=False,
        furnished=True,
        contact_number="9000010004",
        description="Affordable PG with food, WiFi and parking facilities.",
        is_verified=True
    ),

    dict(
        title="Rushikonda Beach Hostel",
        property_type="Hostel",
        location="Visakhapatnam",
        address="Rushikonda, Visakhapatnam 530045",
        monthly_rent=8000,
        security_deposit=12000,
        gender_preference="Any",
        food_available=True,
        wifi_available=True,
        parking_available=True,
        laundry_available=True,
        furnished=True,
        contact_number="9000010005",
        description="Modern hostel accommodation near Rushikonda.",
        is_verified=True
    ),

    dict(
        title="Siripuram Ladies PG",
        property_type="PG",
        location="Visakhapatnam",
        address="Siripuram, Visakhapatnam 530003",
        monthly_rent=8500,
        security_deposit=12000,
        gender_preference="Female",
        food_available=True,
        wifi_available=True,
        parking_available=True,
        laundry_available=True,
        furnished=True,
        contact_number="9000010006",
        description="Well-maintained PG for female students and professionals.",
        is_verified=True
    ),

    dict(
        title="Seethammadhara Boys PG",
        property_type="PG",
        location="Visakhapatnam",
        address="Seethammadhara, Visakhapatnam 530013",
        monthly_rent=6500,
        security_deposit=9000,
        gender_preference="Male",
        food_available=True,
        wifi_available=True,
        parking_available=True,
        laundry_available=True,
        furnished=True,
        contact_number="9000010007",
        description="Budget-friendly PG with food and WiFi facilities.",
        is_verified=True
    ),

    dict(
        title="Yendada Premium PG",
        property_type="PG",
        location="Visakhapatnam",
        address="Yendada, Visakhapatnam 530045",
        monthly_rent=9000,
        security_deposit=15000,
        gender_preference="Any",
        food_available=True,
        wifi_available=True,
        parking_available=True,
        laundry_available=True,
        furnished=True,
        contact_number="9000010008",
        description="Premium furnished PG suitable for students and professionals.",
        is_verified=True
    ),

    dict(
        title="MVP Student Hostel",
        property_type="Hostel",
        location="Visakhapatnam",
        address="MVP Colony, Visakhapatnam 530017",
        monthly_rent=6000,
        security_deposit=8000,
        gender_preference="Female",
        food_available=True,
        wifi_available=True,
        parking_available=False,
        laundry_available=True,
        furnished=True,
        contact_number="9000010009",
        description="Student-friendly hostel with food, WiFi and laundry.",
        is_verified=True
    ),

    dict(
        title="Dwaraka Nagar Premium Stay",
        property_type="PG",
        location="Visakhapatnam",
        address="Dwaraka Nagar, Visakhapatnam 530016",
        monthly_rent=9500,
        security_deposit=15000,
        gender_preference="Any",
        food_available=True,
        wifi_available=True,
        parking_available=True,
        laundry_available=True,
        furnished=True,
        contact_number="9000010010",
        description="Premium stay with furnished rooms and modern facilities.",
        is_verified=True
    ),
]

REVIEWS = [
    ("Comfort Stay PG", 5, "Clean rooms and the food is genuinely good."),
    ("Student Nest Hostel", 4, "Great location, slightly noisy on weekends."),
    ("City View Rooms", 4, "Owner is responsive and repairs are quick."),
]


class Command(BaseCommand):
    help = "Seeds demo users, properties and reviews."

    def handle(self, *args, **options):
        users = {}
        for data in (OWNER, STUDENT, ADMIN):
            user, created = User.objects.get_or_create(
                email=data["email"], defaults={**data, "username": data["email"]}
            )
            if created:
                user.set_password(PASSWORD)
                if data["role"] == User.ADMIN:
                    user.is_staff = True
                    user.is_superuser = True
                user.save()
            users[data["role"]] = user

        owner = users[User.OWNER]
        for data in PROPERTIES:
            Property.objects.get_or_create(title=data["title"], defaults={**data, "owner": owner})

        student = users[User.STUDENT]
        for title, rating, comment in REVIEWS:
            prop = Property.objects.filter(title=title).first()
            if prop:
                Review.objects.get_or_create(
                    property=prop, user=student, defaults={"rating": rating, "comment": comment}
                )

        self.stdout.write(self.style.SUCCESS("Sample data created."))
        self.stdout.write(f"Demo logins (password: {PASSWORD}):")
        self.stdout.write("  student@demo.com / owner@demo.com / admin@demo.com")
