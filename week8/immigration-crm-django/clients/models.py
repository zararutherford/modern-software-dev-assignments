from django.db import models
from django.core.validators import RegexValidator

class Client(models.Model):
    VISA_TYPE_CHOICES = [
        ('H1B', 'H-1B Work Visa'),
        ('L1', 'L-1 Intracompany Transfer'),
        ('O1', 'O-1 Extraordinary Ability'),
        ('EB1', 'EB-1 Employment Based First Preference'),
        ('EB2', 'EB-2 Employment Based Second Preference'),
        ('EB3', 'EB-3 Employment Based Third Preference'),
        ('F1', 'F-1 Student Visa'),
        ('GREEN_CARD', 'Green Card'),
        ('CITIZENSHIP', 'Citizenship'),
        ('ASYLUM', 'Asylum'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('INITIAL_CONSULTATION', 'Initial Consultation'),
        ('DOCUMENTS_GATHERING', 'Documents Gathering'),
        ('APPLICATION_PREP', 'Application Preparation'),
        ('FILED', 'Filed'),
        ('RFE', 'Request for Evidence'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied'),
        ('WITHDRAWN', 'Withdrawn'),
    ]

    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    # Immigration Details
    visa_type = models.CharField(max_length=20, choices=VISA_TYPE_CHOICES)
    current_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='INITIAL_CONSULTATION')
    country_of_origin = models.CharField(max_length=100)

    # Case Information
    case_number = models.CharField(max_length=50, unique=True)
    filing_date = models.DateField(null=True, blank=True)
    priority_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.case_number}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
