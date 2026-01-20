"""
Credito model for tu_credito project.
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class TipoCredito(models.TextChoices):
    """Tipo de crédito."""
    AUTOMOTRIZ = 'AUTOMOTRIZ', 'Automotriz'
    HIPOTECARIO = 'HIPOTECARIO', 'Hipotecario'
    COMERCIAL = 'COMERCIAL', 'Comercial'


class Credito(models.Model):
    """
    Modelo para representar un crédito.
    """
    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.CASCADE,
        related_name='creditos',
        help_text="Cliente al que pertenece el crédito"
    )
    descripcion = models.CharField(
        max_length=500,
        help_text="Descripción del crédito"
    )
    pago_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Pago mínimo del crédito"
    )
    pago_maximo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Pago máximo del crédito"
    )
    plazo_meses = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Plazo del crédito en meses"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de registro del crédito"
    )
    banco = models.ForeignKey(
        'bancos.Banco',
        on_delete=models.CASCADE,
        related_name='creditos',
        help_text="Banco que otorga el crédito"
    )
    tipo_credito = models.CharField(
        max_length=20,
        choices=TipoCredito.choices,
        help_text="Tipo de crédito"
    )
    tasa_interes = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        default=Decimal('12.00'),
        help_text="Tasa de interés anual (%)"
    )
    cuota_mensual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Cuota mensual calculada (calculada automáticamente)"
    )
    monto_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Monto total a pagar (calculado automáticamente)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'creditos'
        verbose_name = 'Crédito'
        verbose_name_plural = 'Créditos'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['cliente']),
            models.Index(fields=['banco']),
            models.Index(fields=['fecha_registro']),
            models.Index(fields=['tipo_credito']),
        ]

    def __str__(self):
        return f"Crédito {self.tipo_credito} - {self.cliente.nombre_completo}"

    def calcular_cuota_mensual(self):
        """
        Calcula la cuota mensual usando la fórmula de amortización.
        Fórmula: P * (r * (1 + r)^n) / ((1 + r)^n - 1)
        donde P = monto (pago_maximo), r = tasa mensual, n = plazo en meses
        """
        from decimal import Decimal
        from math import pow
        
        if not self.pago_maximo or not self.plazo_meses or not self.tasa_interes:
            return None
        
        # Convertir a float para cálculos matemáticos
        monto = float(self.pago_maximo)
        tasa_anual = float(self.tasa_interes)
        plazo = self.plazo_meses
        
        # Tasa mensual
        tasa_mensual = (tasa_anual / 100) / 12
        
        if tasa_mensual == 0:
            # Si no hay interés, la cuota es simplemente el monto dividido por el plazo
            cuota = monto / plazo
        else:
            # Fórmula de amortización
            cuota = monto * (tasa_mensual * pow(1 + tasa_mensual, plazo)) / (pow(1 + tasa_mensual, plazo) - 1)
        
        return Decimal(str(round(cuota, 2)))
    
    def calcular_monto_total(self):
        """
        Calcula el monto total a pagar (cuota_mensual * plazo_meses).
        """
        if not self.cuota_mensual or not self.plazo_meses:
            return None
        
        return self.cuota_mensual * Decimal(str(self.plazo_meses))

    def clean(self):
        """
        Validar que pago_minimo <= pago_maximo.
        """
        from django.core.exceptions import ValidationError
        
        if self.pago_minimo and self.pago_maximo:
            if self.pago_minimo > self.pago_maximo:
                raise ValidationError(
                    {
                        'pago_maximo': 'El pago máximo debe ser mayor o igual al pago mínimo.'
                    }
                )

    def save(self, *args, **kwargs):
        """
        Sobrescribir save para calcular cuota_mensual y monto_total antes de guardar.
        """
        # Calcular cuota mensual y monto total antes de guardar
        self.cuota_mensual = self.calcular_cuota_mensual()
        if self.cuota_mensual:
            self.monto_total = self.calcular_monto_total()
        
        self.full_clean()
        super().save(*args, **kwargs)
