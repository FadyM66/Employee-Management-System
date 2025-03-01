from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinLengthValidator, RegexValidator
from user.models import User

class Employee(models.Model):

    STATUS_CHOICES = [
        ('application_received', ('Application Received')),
        ('interview_scheduled', ('Interview Scheduled')),
        ('hired', ('Hired')),
        ('not_accepted', ('Not Accepted'))
    ]

    department = models.ForeignKey(
        'department.Department',
        related_name="employees",
        on_delete=models.CASCADE,
        verbose_name=("Department")
    )
    
    name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(2)],
        verbose_name=("Full Name")
    )
    
    email = models.EmailField(
        unique=True,
        verbose_name=("Email Address")
    )
    
    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^(?:\+20|0)1[0125]\d{8}$')],
        verbose_name=("Mobile Number")
    )
    
    address = models.TextField(
        null=True,
        verbose_name=("Full Address")
    )
    
    designation = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(2)],
        verbose_name=("Job Title")
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='application_received',
        verbose_name=("Employment Status")
    )
    
    hired_on = models.DateField(
        verbose_name=("Hire Date")
    )
    
    days_employed = models.PositiveIntegerField(
        editable=False,
        verbose_name=("Days Employed")
    )
    
    user = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=("User Account")
    )

    class Meta:
        verbose_name = ("Employee")

    def clean(self):
        if self.pk:
            original = Employee.objects.get(pk=self.pk)
            allowed_transitions = {
                'application_received': ['interview_scheduled', 'not_accepted'],
                'interview_scheduled': ['hired', 'not_accepted'],
                'hired': [],
                'not_accepted': []
            }
            
            if self.status not in allowed_transitions.get(original.status, []):
                raise ValidationError(
                    ("Invalid status transition from %(original)s to %(new)s"),
                    params={'original': original.status, 'new': self.status}
                )

        if self.status == 'hired' and not self.hired_on:
            self.hired_on = timezone.now().date()
            
        if self.status != 'hired':
            self.hired_on = None
            self.days_employed = None

        if self.hired_on:
            delta = timezone.now().date() - self.hired_on
            self.days_employed = delta.days

    def save(self, *args, **kwargs):
        self.full_clean()    

        if self.email and not self.user:
            try:
                matching_user = User.objects.get(email=self.email)
                self.user = matching_user
                
            except User.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    @property
    def company(self):
        return self.department.company

    def __str__(self):
        return f"{self.name} ({self.designation}) - {self.company.name}"
    