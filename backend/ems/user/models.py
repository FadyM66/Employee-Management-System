from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee')
    ]

    name = models.CharField(max_length=255, null=False)  
    email = models.EmailField(unique=True, null=False)    
    role = models.CharField(               
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='employee'
    )
    password = models.CharField(max_length=255, null=False) 

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "User Account"