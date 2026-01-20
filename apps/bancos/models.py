"""
Banco model for tu_credito project.
"""
from decimal import Decimal
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, EmailValidator
from django.core.exceptions import ValidationError


class TipoBanco(models.TextChoices):
    """Tipo de banco."""
    PRIVADO = 'PRIVADO', 'Privado'
    GOBIERNO = 'GOBIERNO', 'Gobierno'


class EstadoBanco(models.TextChoices):
    """Estado del banco."""
    ACTIVO = 'activo', 'Activo'
    INACTIVO = 'inactivo', 'Inactivo'


class Banco(models.Model):
    """
    Modelo para representar un banco.
    """
    nombre = models.CharField(
        max_length=200,
        unique=True,
        validators=[MinLengthValidator(1)],
        help_text="Nombre del banco"
    )
    codigo = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(1)],
        help_text="Código único del banco",
        blank=True,
        null=True
    )
    tipo = models.CharField(
        max_length=20,
        choices=TipoBanco.choices,
        help_text="Tipo de banco"
    )
    direccion = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Dirección del banco"
    )
    email = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        validators=[EmailValidator()],
        help_text="Email de contacto del banco"
    )
    telefono = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Teléfono de contacto del banco"
    )
    sitio_web = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Sitio web del banco"
    )
    tasa_interes_min = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Tasa de interés mínima anual (%)"
    )
    tasa_interes_max = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Tasa de interés máxima anual (%)"
    )
    plazo_minimo = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Plazo mínimo en meses"
    )
    plazo_maximo = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Plazo máximo en meses"
    )
    monto_minimo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Monto mínimo de crédito (MXN)"
    )
    monto_maximo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Monto máximo de crédito (MXN)"
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoBanco.choices,
        default=EstadoBanco.ACTIVO,
        help_text="Estado del banco"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bancos'
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        ordering = ['nombre']

    def clean(self):
        """Validaciones a nivel de modelo."""
        super().clean()
        
        # Validar que tasa_interes_min <= tasa_interes_max
        if self.tasa_interes_min and self.tasa_interes_max:
            if self.tasa_interes_min > self.tasa_interes_max:
                raise ValidationError({
                    'tasa_interes_max': 'La tasa máxima debe ser mayor o igual a la tasa mínima.'
                })
        
        # Validar que plazo_minimo <= plazo_maximo
        if self.plazo_minimo and self.plazo_maximo:
            if self.plazo_minimo > self.plazo_maximo:
                raise ValidationError({
                    'plazo_maximo': 'El plazo máximo debe ser mayor o igual al plazo mínimo.'
                })
        
        # Validar que monto_minimo <= monto_maximo
        if self.monto_minimo and self.monto_maximo:
            if self.monto_minimo > self.monto_maximo:
                raise ValidationError({
                    'monto_maximo': 'El monto máximo debe ser mayor o igual al monto mínimo.'
                })

    def save(self, *args, **kwargs):
        """Sobrescribir save para ejecutar clean."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
