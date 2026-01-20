# Generated manually - Add tasa_interes, cuota_mensual, monto_total fields

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='credito',
            name='tasa_interes',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('12.00'),
                help_text='Tasa de interés anual (%)',
                max_digits=5,
                validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]
            ),
        ),
        migrations.AddField(
            model_name='credito',
            name='cuota_mensual',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Cuota mensual calculada (calculada automáticamente)',
                max_digits=10,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='credito',
            name='monto_total',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Monto total a pagar (calculado automáticamente)',
                max_digits=10,
                null=True
            ),
        ),
    ]
