from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class customer_manager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, id, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            id=id,
        )
        user.set_password(password)
        user.save(using=self._db)
        return email


# auth.user model will be override from setting --> see settings file to override
class Users(AbstractBaseUser):
    id = models.CharField(primary_key=True, editable=False, max_length=70)
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    image_url = models.CharField(max_length=60, default="profile.png")

    class Meta:
        db_table = "registered_user"

    # To login this field is required (email)
    USERNAME_FIELD = 'email'
    # this is required fields
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'id']
    objects = customer_manager()

    # This will return the email in template file
    def __str__(self):
        return self.email

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
