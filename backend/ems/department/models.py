from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

class Department(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(2)],
        help_text=("Department name (must be unique within company)"),
        verbose_name=("Department Name")
    )
    company = models.ForeignKey(
        'company.Company',
        related_name="departments",
        on_delete=models.CASCADE,
        verbose_name=("Company"),
        help_text=("Company for this department")
    )

    @property
    def number_of_employees(self):
        return self.employees.count()
    
    class Meta:
        unique_together = ('name', 'company')
        verbose_name = ("Department")

    def __str__(self):
        return f"{self.company.name} - {self.name}"

    def clean(self):
        from company.models import Company
        if self.pk and self.company_id != Company.objects.get(pk=self.company_id).pk:
            raise ValidationError("Cannot change company after creation")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)