"""
Banco model for tu_credito project.
"""
from django.db import models
from django.core.validators import MinLengthValidator


class TipoBanco(models.TextChoices):
    """Tipo de banco."""
    PRIVADO = 'PRIVADO', 'Privado'
    GOBIERNO = 'GOBIERNO', 'Gobierno'


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bancos'
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
