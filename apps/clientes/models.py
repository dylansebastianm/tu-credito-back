"""
Cliente model for tu_credito project.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class TipoPersona(models.TextChoices):
    """Tipo de persona."""
    NATURAL = 'NATURAL', 'Natural'
    JURIDICO = 'JURIDICO', 'Jurídico'


class Cliente(models.Model):
    """
    Modelo para representar un cliente.
    """
    nombre_completo = models.CharField(
        max_length=200,
        help_text="Nombre completo del cliente"
    )
    fecha_nacimiento = models.DateField(
        help_text="Fecha de nacimiento del cliente"
    )
    edad = models.IntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(99)],
        help_text="Edad del cliente (calculada automáticamente, mínimo 18 años)"
    )
    nacionalidad = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nacionalidad del cliente"
    )
    direccion = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Dirección del cliente"
    )
    email = models.EmailField(
        unique=True,
        help_text="Correo electrónico del cliente"
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Teléfono del cliente"
    )
    tipo_persona = models.CharField(
        max_length=20,
        choices=TipoPersona.choices,
        default=TipoPersona.NATURAL,
        help_text="Tipo de persona"
    )
    banco = models.ForeignKey(
        'bancos.Banco',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clientes',
        help_text="Banco asociado al cliente"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre_completo']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['tipo_persona']),
        ]

    def __str__(self):
        return f"{self.nombre_completo} ({self.email})"

    def calculate_age(self):
        """
        Calcula la edad basándose en la fecha de nacimiento.
        """
        if self.fecha_nacimiento:
            today = timezone.now().date()
            return relativedelta(today, self.fecha_nacimiento).years
        return None

    def clean(self):
        """
        Validar datos del cliente.
        La edad se calcula automáticamente en save(), así que no la validamos aquí.
        """
        from django.core.exceptions import ValidationError
        
        # Validar rango de edad solo si está establecida y es diferente de la calculada
        # (esto puede pasar durante actualizaciones antes de que save() recalcule)
        if self.fecha_nacimiento:
            calculated_age = self.calculate_age()
            if calculated_age is not None:
                # Si la edad no coincide, no validar aquí porque save() la recalculará
                # Solo validar el rango de la edad calculada
                if calculated_age < 1 or calculated_age > 99:
                    raise ValidationError(
                        {
                            'fecha_nacimiento': f'La fecha de nacimiento resulta en una edad inválida ({calculated_age} años). La edad debe estar entre 1 y 99 años.'
                        }
                    )

    def save(self, *args, **kwargs):
        """
        Sobrescribir save para calcular edad automáticamente.
        """
        if self.fecha_nacimiento:
            self.edad = self.calculate_age()
        self.full_clean()
        super().save(*args, **kwargs)
