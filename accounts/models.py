from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from artist.models import Artist

# Create your models here.

class MyAccountManager(BaseUserManager):
    use_in_migrations:True

    def create_user(self,first_name,last_name,username,email,phone_number,password = None):
        if not email:
            raise ValueError('User must have a valid email address')
        
        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(email = self.normalize_email(email),
                username = username,
                first_name = first_name, 
                last_name = last_name,
                phone_number = phone_number)
        user.is_active = True
        user.set_password(password)
        user.save(using = self._db)
        return user
    

    def create_superuser(self,email,password,first_name,last_name,phone_number, username):
      user = self.create_user(
            email    = self.normalize_email(email),
            password = password,
            username= username,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            )
      
      user.is_admin = True
      user.is_active = True
      user.is_superuser = True
      user.is_staff = True
      user.save(using = self._db)
      return user


class Accounts(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=50,unique=True)
    phone_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username','first_name','last_name','phone_number']


    def __str__(self):
        return self.email
    
    def has_permission(self,permission,obj = None):
        return self.is_admin
    
    def has_module_permision(self,add_label):
        return True
    

class Address(models.Model):
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE,null=True)
    local_address = models.CharField(max_length=150)
    alt_ph_number = models.CharField(max_length=13)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)

