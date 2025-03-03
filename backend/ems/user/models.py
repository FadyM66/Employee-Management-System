from django.db import models
from django.db import IntegrityError


class User(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("employee", "Employee"),
    ]

    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")
    password = models.CharField(max_length=255, null=False)

    def save(self, *args, **kwargs):

        if self.role != "admin":
            # Use Django's apps.get_model to avoid circular imports
            from django.apps import apps

            Employee = apps.get_model("employee", "Employee")

            is_employed = Employee.objects.filter(email=self.email).first()
            if is_employed:
                super().save(*args, **kwargs)

            else:
                raise IntegrityError(
                    "Cannot create user account: No employee record found with this email."
                )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "User Account"
