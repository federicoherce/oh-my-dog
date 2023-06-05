from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
#from perros.models import Perro



SOLO_CARACTERES = RegexValidator(r'^[a-zA-Z\sáÁéÉíÍóÓúÚ]+$', 'Este campo solo puede contener caracteres.')

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('activo', True)
        return self._create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, error_messages={
            'unique': 'Ya existe un usuario con este email'})
    nombre = models.CharField(max_length=30,validators=[SOLO_CARACTERES])
    apellido = models.CharField(max_length=30, validators=[SOLO_CARACTERES])
    dni = models.CharField(max_length=15, unique=True, error_messages= {
            'unique': 'Ya existe un usuario con este DNI'})
    telefono = models.CharField(max_length=15,validators = [
    RegexValidator(r'^[0-9+-]+$', 'El teléfono solo puede contener números y los caracteres "+" y "-".')])
    activo = models.BooleanField(default=False)
    usuario_nuevo = models.BooleanField(default=True)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def get_nombre(self):
        return self.nombre
    
    def get_activo(self):
        return self.activo
    
    def get_usuario_nuevo(self):
        return self.usuario_nuevo

        