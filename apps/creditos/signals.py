"""
Signals for Credito model.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import logging

from apps.creditos.models import Credito

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Credito)
def enviar_email_credito_creado(sender, instance, created, **kwargs):
    """
    Envía un email al cliente cuando se crea un crédito.
    """
    if created:
        try:
            cliente = instance.cliente
            banco = instance.banco
            
            subject = f'Confirmación de Crédito - {banco.nombre}'
            message = f"""
Hola {cliente.nombre_completo},

Su crédito ha sido registrado exitosamente.

Detalles del crédito:
- Tipo: {instance.get_tipo_credito_display()}
- Descripción: {instance.descripcion}
- Pago mínimo: ${instance.pago_minimo:,.2f}
- Pago máximo: ${instance.pago_maximo:,.2f}
- Plazo: {instance.plazo_meses} meses
- Banco: {banco.nombre}

Gracias por confiar en nosotros.

Saludos,
Equipo Tu Crédito
"""
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER or 'noreply@tucredito.com',
                [cliente.email],
                fail_silently=False,
            )
            
            logger.info(
                f"Email enviado al cliente {cliente.email} por crédito {instance.id}",
                extra={
                    'credito_id': instance.id,
                    'cliente_email': cliente.email,
                }
            )
        except Exception as e:
            logger.error(
                f"Error al enviar email para crédito {instance.id}: {str(e)}",
                extra={
                    'credito_id': instance.id,
                    'error': str(e),
                }
            )
