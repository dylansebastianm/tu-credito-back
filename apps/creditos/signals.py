"""
Signals for Credito model.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import logging
import os
import sys

from apps.creditos.models import Credito

logger = logging.getLogger(__name__)


def is_loading_fixtures():
    """
    Detecta si estamos cargando fixtures o ejecutando seed_data.
    Esto evita que se envíen emails durante la carga masiva de datos.
    """
    # Verificar si hay una variable de entorno que deshabilite los emails
    if os.environ.get('DISABLE_EMAIL_SIGNALS', '').lower() in ('true', '1', 'yes'):
        return True
    
    # Verificar si estamos ejecutando loaddata o seed_data
    if 'loaddata' in sys.argv or 'seed_data' in sys.argv:
        return True
    
    # Verificar si estamos en un proceso de migración o build
    if 'migrate' in sys.argv or 'makemigrations' in sys.argv:
        return True
    
    return False


@receiver(post_save, sender=Credito)
def enviar_email_credito_creado(sender, instance, created, **kwargs):
    """
    Envía un email al cliente cuando se crea un crédito.
    Si falla el envío, solo se registra el error sin bloquear el proceso.
    NO envía emails durante la carga de fixtures o seed_data para evitar ralentizar el deploy.
    """
    if not created:
        return
    
    # Deshabilitar emails durante la carga de datos (fixtures, seed_data, etc.)
    if is_loading_fixtures():
        logger.debug(
            f"Email deshabilitado para crédito {instance.id} (carga de datos en curso)",
            extra={'credito_id': instance.id}
        )
        return
    
    # Verificar si el email está configurado antes de intentar enviar
    # Si es console backend o no hay credenciales SMTP, no intentar enviar
    email_backend = getattr(settings, 'EMAIL_BACKEND', '')
    email_host_user = getattr(settings, 'EMAIL_HOST_USER', '')
    
    if not email_backend or 'console' in email_backend or not email_host_user:
        # En desarrollo o si no hay backend/credenciales configurados, solo loguear
        logger.debug(
            f"Email no enviado para crédito {instance.id} (EMAIL_BACKEND: {email_backend}, EMAIL_HOST_USER: {'configurado' if email_host_user else 'no configurado'})",
            extra={'credito_id': instance.id}
        )
        return
        
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
                fail_silently=True,  # No fallar si no se puede enviar el email
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
