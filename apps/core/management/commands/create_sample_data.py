"""
Comando para crear datos de prueba masivamente.
Uso: python manage.py create_sample_data [--count-bancos N] [--count-clientes N] [--count-creditos N] [--clear]
"""
from django.core.management.base import BaseCommand
from decimal import Decimal
from datetime import date, timedelta
import random

from apps.bancos.models import Banco, TipoBanco, EstadoBanco
from apps.clientes.models import Cliente, TipoPersona
from apps.creditos.models import Credito, TipoCredito


class Command(BaseCommand):
    help = 'Crea datos de prueba masivamente: bancos, clientes y créditos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count-bancos',
            type=int,
            default=12,
            help='Número de bancos a crear (default: 12)',
        )
        parser.add_argument(
            '--count-clientes',
            type=int,
            default=35,
            help='Número de clientes a crear (default: 35)',
        )
        parser.add_argument(
            '--count-creditos',
            type=int,
            default=60,
            help='Número de créditos a crear (default: 60)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Eliminar todos los datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        count_bancos = options['count_bancos']
        count_clientes = options['count_clientes']
        count_creditos = options['count_creditos']
        clear = options['clear']

        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Creando datos de prueba masivamente'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')

        # Limpiar datos existentes si se solicita
        if clear:
            self.stdout.write(self.style.WARNING('⚠ Eliminando datos existentes...'))
            Credito.objects.all().delete()
            Cliente.objects.all().delete()
            Banco.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Datos eliminados'))
            self.stdout.write('')

        # Crear bancos
        self.stdout.write(f'Creando {count_bancos} bancos...')
        bancos = []
        nombres_bancos = [
            "Banco Nacional", "Banco Popular", "Banco Central", "Banco del Sur",
            "Banco Industrial", "Banco Comercial", "Banco de Ahorro", "Banco Rural",
            "Banco Metropolitano", "Banco Regional", "Banco Internacional", "Banco Financiero",
            "Banco Atlántico", "Banco Pacífico", "Banco Continental", "Banco Unión"
        ]

        for i in range(count_bancos):
            nombre = nombres_bancos[i] if i < len(nombres_bancos) else f"Banco {i+1}"
            tipo = random.choice([TipoBanco.PRIVADO, TipoBanco.GOBIERNO])
            # 75% activos, 25% inactivos
            estado = random.choice([
                EstadoBanco.ACTIVO, EstadoBanco.ACTIVO, EstadoBanco.ACTIVO, EstadoBanco.INACTIVO
            ])

            banco = Banco.objects.create(
                nombre=nombre,
                codigo=f"BN{i+1:03d}",
                tipo=tipo,
                direccion=f"Calle {i+1}00, Ciudad",
                email=f"contacto@{nombre.lower().replace(' ', '')}.com",
                telefono=f"+52 55 {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
                sitio_web=f"https://www.{nombre.lower().replace(' ', '')}.com",
                tasa_interes_min=Decimal(f"{random.uniform(8.0, 12.0):.2f}"),
                tasa_interes_max=Decimal(f"{random.uniform(15.0, 25.0):.2f}"),
                plazo_minimo=random.randint(6, 12),
                plazo_maximo=random.randint(36, 60),
                monto_minimo=Decimal(f"{random.randint(10000, 50000)}"),
                monto_maximo=Decimal(f"{random.randint(500000, 2000000)}"),
                estado=estado,
            )
            bancos.append(banco)
            self.stdout.write(f'  ✓ {banco.nombre} ({banco.get_tipo_display()})')

        self.stdout.write('')

        # Crear clientes
        self.stdout.write(f'Creando {count_clientes} clientes...')
        clientes = []
        nombres = ["Juan", "María", "Carlos", "Ana", "Luis", "Laura", "Pedro", "Sofía", "Diego", "Carmen"]
        apellidos = [
            "Pérez", "García", "López", "Martínez", "González", "Rodríguez",
            "Fernández", "Sánchez", "Ramírez", "Torres"
        ]

        for i in range(count_clientes):
            nombre_completo = f"{random.choice(nombres)} {random.choice(apellidos)} {random.choice(apellidos)}"
            # Fecha de nacimiento entre 18 y 65 años
            fecha_nac = date.today() - timedelta(days=random.randint(18 * 365, 65 * 365))
            tipo_persona = random.choice([TipoPersona.NATURAL, TipoPersona.JURIDICO])
            # Asignar banco aleatorio (puede ser None)
            banco_asignado = random.choice(bancos + [None]) if bancos else None

            cliente = Cliente.objects.create(
                nombre_completo=nombre_completo,
                email=f"cliente{i+1}@example.com",
                tipo_persona=tipo_persona,
                fecha_nacimiento=fecha_nac,
                direccion=f"Av. Principal {random.randint(100, 999)}, Col. Centro",
                telefono=f"+52 55 {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
                nacionalidad=random.choice(["Mexicana", "Estadounidense", "Canadiense", "Española", None]),
                banco=banco_asignado,
            )
            clientes.append(cliente)
            self.stdout.write(f'  ✓ {cliente.nombre_completo}')

        self.stdout.write('')

        # Crear créditos
        self.stdout.write(f'Creando {count_creditos} créditos...')
        tipos_credito = [TipoCredito.AUTOMOTRIZ, TipoCredito.HIPOTECARIO, TipoCredito.COMERCIAL]
        descripciones = [
            "Crédito para compra de vehículo",
            "Crédito hipotecario para vivienda",
            "Crédito comercial para negocio",
            "Crédito personal",
            "Crédito para mejoras del hogar",
        ]

        for i in range(count_creditos):
            banco = random.choice(bancos)
            cliente = random.choice(clientes)
            tipo_credito = random.choice(tipos_credito)
            descripcion = random.choice(descripciones)

            # Monto del crédito dentro del rango del banco
            monto_base = float(banco.monto_minimo or 10000)
            monto_max = float(banco.monto_maximo or 500000)
            monto_credito = Decimal(f"{random.uniform(monto_base, monto_max):.2f}")

            # Plazo dentro del rango del banco
            plazo = random.randint(banco.plazo_minimo or 6, banco.plazo_maximo or 60)

            # Tasa dentro del rango del banco
            tasa = Decimal(f"{random.uniform(float(banco.tasa_interes_min or 8), float(banco.tasa_interes_max or 25)):.2f}")

            # Calcular cuota mensual aproximada (para establecer pago_minimo y pago_maximo)
            # Usamos una estimación simple: monto / plazo * factor de interés
            tasa_mensual = float(tasa) / 100 / 12
            cuota_estimada = float(monto_credito) * (tasa_mensual * (1 + tasa_mensual) ** plazo) / ((1 + tasa_mensual) ** plazo - 1) if tasa_mensual > 0 else float(monto_credito) / plazo
            
            # pago_minimo es 80-90% de la cuota estimada
            pago_minimo = Decimal(f"{cuota_estimada * random.uniform(0.80, 0.90):.2f}")
            # pago_maximo es 110-120% de la cuota estimada
            pago_maximo = Decimal(f"{cuota_estimada * random.uniform(1.10, 1.20):.2f}")

            fecha_inicio = date.today() - timedelta(days=random.randint(0, 365))

            credito = Credito.objects.create(
                cliente=cliente,
                banco=banco,
                descripcion=descripcion,
                tipo_credito=tipo_credito,
                monto=monto_credito,  # Monto total del crédito
                pago_minimo=pago_minimo,  # Cuota mínima mensual
                pago_maximo=pago_maximo,  # Cuota máxima mensual
                plazo_meses=plazo,
                tasa_interes=tasa,
                fecha_registro=fecha_inicio,
            )
            self.stdout.write(
                f'  ✓ Crédito #{credito.id} - {cliente.nombre_completo} - '
                f'Monto: ${monto_credito:,.2f} | Cuota: ${credito.cuota_mensual or 0:,.2f}/mes ({tipo_credito})'
            )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('✅ Datos creados exitosamente!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')
        self.stdout.write(f'   📊 Resumen:')
        self.stdout.write(f'   - {Banco.objects.count()} bancos')
        self.stdout.write(f'   - {Cliente.objects.count()} clientes')
        self.stdout.write(f'   - {Credito.objects.count()} créditos')
        self.stdout.write('')
        self.stdout.write('💡 Para exportar estos datos a fixtures:')
        self.stdout.write('   python manage.py export_data')
        self.stdout.write('')
