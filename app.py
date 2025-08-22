#!/usr/bin/env python3
"""
AIFA Dashboard - Production Ready Version
Executive Dashboard for Felipe Ángeles International Airport
"""

import dash
from dash import Dash, html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import random

# Initialize Dash app
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True,
           meta_tags=[{'name': 'viewport',
                      'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

# Simulated data functions
def get_kpi_data():
    return {
        'participation_passengers': {'current': 12.8, 'change': 2.3, 'target': 15.0},
        'participation_operations': {'current': 9.7, 'change': 1.8, 'target': 12.0},
        'participation_cargo': {'current': 8.4, 'change': 3.1, 'target': 10.0},
        'growth_vs_market': {'current': 5.5, 'change': 0.8},
        'punctuality': {'current': 87.2, 'change': -1.3, 'target': 90.0},
        'route_utilization': {'current': 78.4, 'change': 2.1, 'target': 85.0}
    }

def get_historical_data():
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
              'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    passengers = [8.2, 8.6, 9.1, 9.5, 10.2, 10.8, 11.3, 11.7, 12.1, 12.4, 12.6, 12.8]
    operations = [6.8, 7.1, 7.5, 7.9, 8.3, 8.7, 9.0, 9.3, 9.5, 9.6, 9.7, 9.7]
    cargo = [5.1, 5.4, 5.8, 6.2, 6.7, 7.1, 7.5, 7.8, 8.0, 8.1, 8.2, 8.4]
    return {'months': months, 'passengers': passengers, 'operations': operations, 'cargo': cargo}

def get_route_data():
    return [
        {'city': 'Los Angeles, USA', 'passengers': 87000, 'load_factor': 85.7, 'frequency': 21},
        {'city': 'Houston, USA', 'passengers': 76000, 'load_factor': 81.3, 'frequency': 19},
        {'city': 'Miami, USA', 'passengers': 92000, 'load_factor': 87.4, 'frequency': 17},
        {'city': 'Guadalajara, México', 'passengers': 125000, 'load_factor': 82.3, 'frequency': 42},
        {'city': 'Monterrey, México', 'passengers': 98000, 'load_factor': 78.5, 'frequency': 35},
        {'city': 'Cancún, México', 'passengers': 156000, 'load_factor': 89.2, 'frequency': 28},
        {'city': 'Bogotá, Colombia', 'passengers': 45000, 'load_factor': 79.8, 'frequency': 14},
        {'city': 'Lima, Perú', 'passengers': 38000, 'load_factor': 82.1, 'frequency': 10}
    ]

def get_airport_comparison():
    return [
        {'name': 'AICM', 'passengers': 48.2, 'change': -2.1},
        {'name': 'AIFA', 'passengers': 12.8, 'change': 2.3},
        {'name': 'Guadalajara', 'passengers': 8.9, 'change': 0.8},
        {'name': 'Cancún', 'passengers': 15.4, 'change': 1.2},
        {'name': 'Monterrey', 'passengers': 7.2, 'change': -0.3},
        {'name': 'Tijuana', 'passengers': 4.9, 'change': 0.5},
        {'name': 'Otros', 'passengers': 2.6, 'change': -0.4}
    ]

def get_financial_data():
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    revenue = [150, 162, 175, 188, 195, 210, 225, 238, 245, 260, 275, 290]
    costs = [112, 118, 125, 135, 140, 150, 160, 170, 175, 185, 195, 205]
    return {'months': months, 'revenue': revenue, 'costs': costs}

def get_capacity_data():
    return {
        'checkin_area': {'current': 245, 'utilization': 98, 'standard': 250, 'unit': 'm²/millón pax'},
        'waiting_area': {'current': 890, 'utilization': 82, 'standard': 900, 'unit': 'm²/millón pax'},
        'security_area': {'current': 120, 'utilization': 76, 'standard': 140, 'unit': 'm²/millón pax'},
        'sterile_area': {'current': 450, 'utilization': 85, 'standard': 500, 'unit': 'm²/millón pax'},
        'baggage_system': {'current': 2400, 'utilization': 80, 'max_capacity': 3000, 'unit': 'bags/hr'}
    }

def get_capacity_zones():
    return [
        {'zone': 'Terminal A - Check-in', 'utilization': 85, 'capacity': 12000, 'current': 10200},
        {'zone': 'Terminal A - Seguridad', 'utilization': 76, 'capacity': 8000, 'current': 6080},
        {'zone': 'Terminal B - Check-in', 'utilization': 92, 'capacity': 10000, 'current': 9200},
        {'zone': 'Terminal B - Seguridad', 'utilization': 68, 'capacity': 6000, 'current': 4080},
        {'zone': 'Sala de Espera Dom.', 'utilization': 82, 'capacity': 15000, 'current': 12300},
        {'zone': 'Sala de Espera Int.', 'utilization': 74, 'capacity': 8000, 'current': 5920},
        {'zone': 'Puertas de Embarque', 'utilization': 78, 'capacity': 25000, 'current': 19500},
        {'zone': 'Recogida Equipajes', 'utilization': 83, 'capacity': 12000, 'current': 9960}
    ]

def get_security_data():
    """Datos completos de los 15 KPIs de seguridad operacional AIFA"""
    return {
        # KPIs principales (Top 5)
        'runway_incidents': {'rate': 0.12, 'target': '<0.15', 'unit': '/1000 ops', 'status': 'excellent', 'trend': -0.02},
        'fatal_accidents': {'rate': 0.00, 'target': '0.00', 'unit': '/1000 ops', 'status': 'excellent', 'trend': 0.00},
        'work_accidents': {'rate': 0.03, 'target': '<0.05', 'unit': '/1000 hrs', 'status': 'excellent', 'trend': -0.01},
        'runway_incursions': {'rate': 0.05, 'target': '<0.10', 'unit': '/1000 ops', 'status': 'excellent', 'trend': 0.01},
        'bird_strikes': {'rate': 0.85, 'target': '<1.20', 'unit': '/1000 ops', 'status': 'good', 'trend': 0.05},
        
        # Métricas operacionales (10 restantes)
        'security_staff': {'rate': 45, 'target': '>40', 'unit': '/millón pax', 'status': 'good', 'trend': 2.1},
        'incident_movements': {'rate': 0.08, 'target': '<0.12', 'unit': '/movimiento', 'status': 'excellent', 'trend': -0.02},
        'cameras_density': {'rate': 2.3, 'target': '>2.0', 'unit': '/hectárea', 'status': 'good', 'trend': 0.1},
        'wildlife_events': {'rate': 0.15, 'target': '<0.25', 'unit': '/operación', 'status': 'excellent', 'trend': -0.03},
        'lighting_functional': {'rate': 98.7, 'target': '>97.0', 'unit': '%', 'status': 'excellent', 'trend': 0.2},
        'lighting_incidents': {'rate': 0.02, 'target': '<0.05', 'unit': '/operación', 'status': 'excellent', 'trend': 0.01},
        'pothole_attended': {'rate': 95.2, 'target': '>90.0', 'unit': '%', 'status': 'excellent', 'trend': 1.8},
        'runway_maintenance': {'rate': 0.06, 'target': '<0.10', 'unit': '/operación', 'status': 'excellent', 'trend': -0.01},
        'fod_reports': {'rate': 0.08, 'target': '<0.15', 'unit': '/operación', 'status': 'excellent', 'trend': 0.02},
        'fod_damage': {'rate': 0.01, 'target': '<0.03', 'unit': '/operación', 'status': 'excellent', 'trend': 0.00}
    }

def get_quality_data():
    """Datos completos de los 11 KPIs oficiales de Calidad de Servicio AIFA"""
    return {
        # KPIs oficiales del documento AIFA (11 métricas mandatorias)
        'capacidad_diaria': {'value': 485, 'target': 450, 'unit': 'movimientos/día', 'status': 'excellent', 'trend': 12},
        'demoras_motivo': {'total': 47, 'climaticas': 18, 'tecnicas': 15, 'operacionales': 14, 'unit': 'demoras/día'},
        'demora_promedio': {'avg': 12.3, 'target': 15.0, 'unit': 'min/vuelo', 'status': 'excellent', 'trend': -1.2},
        'tiempo_seguridad': {'avg': 6.4, 'target': 8.0, 'unit': 'min', 'status': 'excellent', 'trend': -0.3},
        'disponibilidad_equipaje': {'availability': 98.5, 'target': 95.0, 'unit': '%', 'status': 'excellent', 'trend': 1.2},
        'tiempo_checkin_pico': {'avg': 3.2, 'target': 5.0, 'unit': 'min', 'status': 'excellent', 'trend': -0.1},
        'tiempo_equipaje_pico': {'avg': 8.1, 'target': 12.0, 'unit': 'min', 'status': 'excellent', 'trend': 0.4},
        'facilidad_ubicacion': {'score': 4.4, 'target': 4.0, 'unit': '/5', 'status': 'excellent', 'trend': 0.1},
        'precision_informacion': {'score': 4.6, 'target': 4.0, 'unit': '/5', 'status': 'excellent', 'trend': 0.2},
        'limpieza_banos': {'score': 4.5, 'target': 4.0, 'unit': '/5', 'status': 'excellent', 'trend': 0.2},
        'satisfaccion_general': {'score': 4.6, 'target': 4.0, 'unit': '/5', 'status': 'excellent', 'trend': 0.1},
        
        # NPS Score y breakdown
        'nps_score': {'score': 67, 'target': 50, 'unit': '/100', 'status': 'excellent', 'trend': 3},
        'nps_breakdown': {'promotores': 58, 'pasivos': 33, 'detractores': 9}
    }

def get_customer_journey_data():
    """Datos del Customer Journey con 6 touchpoints principales"""
    return {
        'llegada': {'score': 4.8, 'time': 2.1, 'target': 3.0, 'status': 'excellent', 'icon': 'mdi:car-arrow-right'},
        'checkin': {'score': 4.6, 'time': 3.2, 'target': 5.0, 'status': 'excellent', 'icon': 'mdi:airplane-check'},
        'seguridad': {'score': 4.4, 'time': 6.4, 'target': 8.0, 'status': 'good', 'icon': 'mdi:security'},
        'comercial': {'score': 4.2, 'time': 15.3, 'target': 'libre', 'status': 'good', 'icon': 'mdi:shopping'},
        'embarque': {'score': 4.7, 'time': 4.1, 'target': 5.0, 'status': 'excellent', 'icon': 'mdi:gate'},
        'equipaje': {'score': 4.1, 'time': 8.1, 'target': 12.0, 'status': 'warning', 'icon': 'mdi:baggage-claim'}
    }

def get_satisfaction_heatmap_data():
    """Datos para heatmap de satisfacción por áreas del aeropuerto"""
    return [
        ['Terminal', 'Check-in', 'Seguridad', 'Comercial'],
        [4.8, 4.6, 4.4, 4.2],
        [4.7, 4.5, 4.3, 4.1],
        [4.6, 4.4, 4.2, 4.0]
    ]

def get_productivity_data():
    """Datos completos de los 5 KPIs oficiales de Productividad AIFA"""
    return {
        # KPIs Principales - Executive Dashboard
        'movements_per_hour': {
            'current': 18.2,
            'benchmark': 16.0,
            'unit': 'mov/hr',
            'trend': 'up',
            'performance': 113.8,
            'change': 1.2
        },
        'turnaround_time': {
            'current': 35,
            'benchmark': 40,
            'unit': 'min',
            'trend': 'down',  # down is good for turnaround time
            'performance': 114.3,
            'change': -3
        },
        'gate_utilization': {
            'current': 78.4,
            'benchmark': 75.0,
            'unit': '%',
            'trend': 'up',
            'performance': 104.5,
            'change': 2.8
        },
        'staff_productivity': {
            'current': 1380,
            'benchmark': 1200,
            'unit': 'pax/emp',
            'trend': 'up',
            'performance': 115.0,
            'change': 85
        },
        'cost_per_wlu': {
            'current': 11.20,
            'benchmark': 12.50,
            'unit': 'USD',
            'trend': 'down',  # down is good for costs
            'performance': 110.4,
            'change': -0.95
        }
    }

def get_executive_metrics():
    """Métricas ejecutivas derivadas para dashboard de productividad"""
    return {
        'revenue_per_movement': 2450,
        'revenue_per_movement_change': '+3.2%',
        'asset_utilization': 84.5,
        'asset_utilization_change': '+2.1%',
        'labor_efficiency': 91.8,
        'labor_efficiency_change': '+1.8%',
        'process_optimization': 87.3,
        'process_optimization_change': '+4.2%'
    }

def get_benchmark_data():
    """Datos de benchmark internacional para comparación"""
    return {
        'aifa': [112.7, 114.0, 112.5, 104.9, 111.9, 108.5],
        'promedio_latam': [95, 92, 88, 90, 85, 87],
        'promedio_global': [100, 100, 100, 100, 100, 100],
        'top_performer': [125, 130, 120, 115, 125, 118],
        'categorias': ['Pax/Empleado', 'Ops/Empleado', 'Carga/Empleado', 'Ops/Puerta', 'Pax/Puerta', 'Eficiencia']
    }

# Metodología Data Functions
def get_dashboard_mapping():
    """Mapeo completo de KPIs y sistemas del dashboard AIFA"""
    return {
        'geografico': {
            'kpis': 8,
            'implementado': True,
            'sistemas': ['AODB', 'GIS', 'Radar'],
            'complejidad': 'Media',
            'descripcion': 'Análisis geográfico de rutas y conectividad internacional',
            'kpis_principales': ['Rutas Domésticas', 'Rutas Internacionales', 'Conectividad Hub', 'Cobertura Geográfica']
        },
        'financiero': {
            'kpis': 8, 
            'implementado': True,
            'sistemas': ['ERP', 'Contabilidad', 'CRM'],
            'complejidad': 'Baja',
            'descripcion': 'Indicadores financieros y rentabilidad operacional',
            'kpis_principales': ['Revenue per Pax', 'EBITDA', 'ROI', 'Cost per Operation']
        },
        'capacidad': {
            'kpis': 6,
            'implementado': True,
            'sistemas': ['AODB', 'BRS', 'FIDS'],
            'complejidad': 'Media',
            'descripcion': 'Utilización de capacidad de infraestructura aeroportuaria',
            'kpis_principales': ['Utilización Terminal', 'Throughput Pax', 'Capacity Load Factor']
        },
        'seguridad': {
            'kpis': 15,
            'implementado': True,
            'sistemas': ['SMS', 'AODB', 'Radar', 'CCTV'],
            'complejidad': 'Alta',
            'descripcion': 'Seguridad operacional y compliance OACI',
            'kpis_principales': ['Incidentes Runway', 'FOD Rate', 'Security Index', 'Safety Score']
        },
        'calidad': {
            'kpis': 11,
            'implementado': True, 
            'sistemas': ['IoT', 'CRM', 'Encuestas', 'Sensors'],
            'complejidad': 'Alta',
            'descripcion': 'Calidad de servicio y satisfacción del pasajero',
            'kpis_principales': ['NPS Score', 'Tiempo de Espera', 'Satisfacción General', 'Customer Journey']
        },
        'productividad': {
            'kpis': 5,
            'implementado': True,
            'sistemas': ['AODB', 'RH', 'ERP', 'WMS'],
            'complejidad': 'Media',
            'descripcion': 'Eficiencia operacional y productividad de recursos',
            'kpis_principales': ['Movimientos/Hora', 'Staff Productivity', 'Turnaround Time', 'Gate Utilization']
        }
    }

def get_technical_glossary():
    """Glosario técnico completo del sector aeroportuario"""
    return {
        'AODB': {
            'nombre': 'Airport Operational Database',
            'definicion': 'Sistema central que gestiona toda la información operacional del aeropuerto en tiempo real, incluyendo vuelos, recursos y coordinación entre sistemas.',
            'funciones': ['Seguimiento de vuelos en tiempo real', 'Gestión de recursos aeroportuarios', 'Integración con sistemas externos', 'Generación de reportes operacionales'],
            'criticidad': 'Alta - Sistema crítico del aeropuerto'
        },
        'SMS': {
            'nombre': 'Safety Management System', 
            'definicion': 'Sistema integral de gestión de seguridad operacional según estándares OACI Anexo 19, que permite identificar, evaluar y mitigar riesgos de seguridad.',
            'funciones': ['Reportes de incidentes y accidentes', 'Análisis de riesgos operacionales', 'Auditorías de seguridad', 'Gestión de indicadores de seguridad'],
            'criticidad': 'Crítica - Requerimiento regulatorio OACI'
        },
        'SCT_AFAC': {
            'nombre': 'Secretaría de Comunicaciones y Transportes / Agencia Federal de Aviación Civil',
            'definicion': 'Autoridades aeronáuticas mexicanas que regulan, certifican y supervisan todas las actividades de aviación civil en territorio nacional.',
            'funciones': ['Regulación aeronáutica nacional', 'Certificación de aeropuertos', 'Supervisión y auditorías', 'Emisión de licencias'],
            'criticidad': 'Crítica - Autoridad regulatoria nacional'
        },
        'OACI_ICAO': {
            'nombre': 'Organización de Aviación Civil Internacional / International Civil Aviation Organization',
            'definicion': 'Organismo especializado de la ONU que establece estándares y prácticas recomendadas internacionales para la aviación civil.',
            'funciones': ['Desarrollo de estándares globales', 'Prácticas recomendadas (SARPs)', 'Auditorías internacionales', 'Coordinación entre Estados'],
            'criticidad': 'Crítica - Estándares internacionales obligatorios'
        },
        'ERP': {
            'nombre': 'Enterprise Resource Planning',
            'definicion': 'Sistema integrado de gestión empresarial que unifica todos los procesos de negocio: finanzas, recursos humanos, operaciones y logística.',
            'funciones': ['Gestión financiera y contable', 'Administración de recursos humanos', 'Gestión de compras y logística', 'Reportes ejecutivos integrados'],
            'criticidad': 'Alta - Backbone administrativo'
        },
        'IoT': {
            'nombre': 'Internet of Things (Internet de las Cosas)',
            'definicion': 'Red interconectada de sensores, dispositivos y sistemas que recopilan y transmiten datos en tiempo real para monitoreo y control automatizado.',
            'funciones': ['Sensores de flujo de pasajeros', 'Monitoreo ambiental (temperatura, humedad)', 'Tracking de activos y equipos', 'Automatización de procesos'],
            'criticidad': 'Media - Optimización operacional'
        },
        'FOD': {
            'nombre': 'Foreign Object Debris/Damage',
            'definicion': 'Objetos extraños presentes en áreas operacionales (pistas, calles de rodaje) que representan riesgo de daño a aeronaves o equipos.',
            'funciones': ['Inspección sistemática de pistas', 'Reportes y clasificación de objetos', 'Protocolos de remoción', 'Prevención de incidentes'],
            'criticidad': 'Alta - Seguridad operacional crítica'
        },
        'NPS': {
            'nombre': 'Net Promoter Score',
            'definicion': 'Métrica de lealtad y satisfacción que mide la probabilidad de que un pasajero recomiende el aeropuerto, basada en escala 0-10.',
            'funciones': ['Encuestas de satisfacción a pasajeros', 'Análisis de tendencias de servicio', 'Benchmarking con otros aeropuertos', 'Identificación de áreas de mejora'],
            'criticidad': 'Media - Indicador de calidad de servicio'
        },
        'BRS': {
            'nombre': 'Baggage Reconciliation System',
            'definicion': 'Sistema de reconciliación y seguimiento de equipaje que garantiza que cada maleta esté asociada con un pasajero que efectivamente abordó.',
            'funciones': ['Tracking de equipaje end-to-end', 'Verificación de seguridad', 'Gestión de conexiones internacionales', 'Localización de equipaje extraviado'],
            'criticidad': 'Alta - Seguridad y satisfacción del pasajero'
        },
        'CRM': {
            'nombre': 'Customer Relationship Management',
            'definicion': 'Sistema de gestión de relaciones con pasajeros y clientes que centraliza interacciones, quejas, sugerencias y análisis de comportamiento.',
            'funciones': ['Gestión centralizada de quejas', 'Encuestas de satisfacción', 'Análisis de comportamiento del pasajero', 'Seguimiento de resoluciones'],
            'criticidad': 'Media - Experiencia del cliente'
        },
        'WLU': {
            'nombre': 'Work Load Unit',
            'definicion': 'Unidad de medida estándar de la industria aeroportuaria que equivale a 1 pasajero o 100 kg de carga, utilizada para cálculos de capacidad y productividad.',
            'funciones': ['Medición de carga de trabajo', 'Cálculos de capacidad', 'Benchmarking internacional', 'Planificación de recursos'],
            'criticidad': 'Media - Estándar de medición industria'
        },
        'FIDS': {
            'nombre': 'Flight Information Display System',
            'definicion': 'Sistema de pantallas de información de vuelos que muestra en tiempo real horarios, puertas, estados y actualizaciones para pasajeros.',
            'funciones': ['Información en tiempo real a pasajeros', 'Integración con AODB', 'Gestión de contenido dinámico', 'Multilenguaje y accesibilidad'],
            'criticidad': 'Alta - Información crítica para pasajeros'
        }
    }

def get_system_architecture():
    """Arquitectura de sistemas y flujo de datos"""
    return {
        'core_systems': {
            'AODB': {
                'descripcion': 'Sistema central de base de datos operacionales',
                'conexiones': ['SMS', 'FIDS', 'BRS', 'ERP'],
                'datos': ['Información de vuelos', 'Recursos aeroportuarios', 'Estadísticas operacionales'],
                'criticidad': 'Crítica'
            },
            'SMS': {
                'descripcion': 'Sistema de gestión de seguridad',
                'conexiones': ['AODB', 'Radar', 'CCTV'],
                'datos': ['Incidentes de seguridad', 'Análisis de riesgos', 'Reportes regulatorios'],
                'criticidad': 'Crítica'
            },
            'ERP': {
                'descripcion': 'Sistema de planificación de recursos empresariales',
                'conexiones': ['AODB', 'CRM', 'RH'],
                'datos': ['Información financiera', 'Recursos humanos', 'Gestión de activos'],
                'criticidad': 'Alta'
            }
        },
        'integration_apis': [
            {'nombre': 'AODB-API', 'protocolo': 'REST', 'formato': 'JSON', 'tiempo_real': True},
            {'nombre': 'SMS-API', 'protocolo': 'SOAP', 'formato': 'XML', 'tiempo_real': False},
            {'nombre': 'IoT-Gateway', 'protocolo': 'MQTT', 'formato': 'JSON', 'tiempo_real': True},
            {'nombre': 'ERP-Integration', 'protocolo': 'REST', 'formato': 'JSON', 'tiempo_real': False}
        ],
        'data_flow': {
            'tiempo_real': ['AODB', 'IoT', 'FIDS', 'Sensors'],
            'batch': ['ERP', 'CRM', 'Reportes', 'Analytics'],
            'frecuencia_actualizacion': {
                'AODB': '5 segundos',
                'IoT': '30 segundos', 
                'ERP': '1 hora',
                'CRM': '15 minutos'
            }
        }
    }

def get_kpi_formulas():
    """Fórmulas matemáticas exactas para cada KPI"""
    return {
        'seguridad': {
            'runway_incident_rate': {
                'formula': '(Número de Incidentes en Pista / Total de Movimientos) × 1000',
                'unidad': 'incidentes por 1000 operaciones',
                'fuente': 'SMS + AODB',
                'estandar_oaci': 'Anexo 19 - SMS',
                'meta_aifa': '< 0.15 por 1000 ops'
            },
            'fod_detection_rate': {
                'formula': '(FODs Detectados / Total de Inspecciones) × 100',
                'unidad': 'porcentaje',
                'fuente': 'Sistema de Inspección + Reportes Manuales',
                'estandar_oaci': 'Anexo 14 - Diseño de Aeródromos',
                'meta_aifa': '> 95% detección'
            }
        },
        'productividad': {
            'movements_per_hour': {
                'formula': 'Total de Movimientos de Aeronaves / Horas de Operación',
                'unidad': 'movimientos por hora',
                'fuente': 'AODB',
                'benchmark_internacional': '16-18 mov/hr aeropuertos similares',
                'meta_aifa': '> 16 movimientos/hora'
            },
            'staff_productivity': {
                'formula': 'Total de Pasajeros Atendidos / Número de Empleados FTE',
                'unidad': 'pasajeros por empleado',
                'fuente': 'AODB + Sistema RH',
                'benchmark_internacional': '1200-1500 pax/empleado',
                'meta_aifa': '> 1200 pax/empleado'
            }
        },
        'calidad': {
            'nps_score': {
                'formula': '% Promotores (9-10) - % Detractores (0-6)',
                'unidad': 'puntos NPS (-100 a +100)',
                'fuente': 'Sistema de Encuestas CRM',
                'benchmark_internacional': 'NPS > 30 considerado bueno',
                'meta_aifa': 'NPS > 40'
            },
            'average_waiting_time': {
                'formula': 'Σ(Tiempo de Espera por Pasajero) / Total de Pasajeros',
                'unidad': 'minutos',
                'fuente': 'Sensores IoT + Sistema de Colas',
                'estandar_servicio': '< 15 min en seguridad, < 5 min en migración',
                'meta_aifa': '< 10 min promedio general'
            }
        }
    }

def get_route_network_data():
    """Datos de la red de rutas AIFA con coordenadas geográficas"""
    aifa_lat, aifa_lon = 19.7373, -99.0068
    
    return {
        'hub': {'name': 'AIFA', 'lat': aifa_lat, 'lon': aifa_lon},
        'routes': [
            {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "pax": 87000, "type": "international", "flights": 21},
            {"name": "Houston", "lat": 29.7604, "lon": -95.3698, "pax": 76000, "type": "international", "flights": 19},
            {"name": "Miami", "lat": 25.7617, "lon": -80.1918, "pax": 92000, "type": "international", "flights": 17},
            {"name": "Guadalajara", "lat": 20.6597, "lon": -103.3496, "pax": 125000, "type": "domestic", "flights": 42},
            {"name": "Monterrey", "lat": 25.6866, "lon": -100.3161, "pax": 98000, "type": "domestic", "flights": 35},
            {"name": "Cancún", "lat": 21.1619, "lon": -86.8515, "pax": 156000, "type": "domestic", "flights": 28},
            {"name": "Madrid", "lat": 40.4168, "lon": -3.7038, "pax": 67000, "type": "international", "flights": 14},
            {"name": "Bogotá", "lat": 4.7110, "lon": -74.0721, "pax": 45000, "type": "international", "flights": 12}
        ]
    }

# KPI Card component
def create_kpi_card(title, value, change, icon, target=None, unit="", format_type="percent"):
    trend_color = '#00ff88' if change > 0 else '#ff4757'
    trend_arrow = '↗' if change > 0 else '↘'
    
    if format_type == "percent":
        value_display = f"{value}%"
        change_display = f"{change:+.1f}%"
    elif format_type == "decimal":
        value_display = f"{value:.2f}{unit}"
        change_display = f"{change:+.2f}"
    elif format_type == "integer":
        value_display = f"{value:,}{unit}"
        change_display = f"{change:+.0f}"
    else:
        value_display = f"{value}{unit}"
        change_display = f"{change:+.1f}"
    
    progress = (value / target * 100) if target else None
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Div([
                    DashIconify(icon=icon, width=30, height=30, style={'color': '#00d4ff'})
                ], className="kpi-icon"),
                html.Div([
                    html.H6(title, className="kpi-title"),
                    html.H3(value_display, className="kpi-value"),
                    html.Div([
                        html.Span(trend_arrow, style={'color': trend_color, 'fontSize': '16px'}),
                        html.Span(change_display, style={'color': trend_color, 'marginLeft': '5px'})
                    ], className="kpi-change"),
                    html.Small("vs mes anterior", className="kpi-period")
                ], className="kpi-content")
            ], className="kpi-header"),
            
            # Progress bar if target exists
            html.Div([
                dbc.Progress(
                    value=progress if progress else 0,
                    color="info" if progress and progress >= 90 else "warning" if progress and progress >= 70 else "danger",
                    style={'height': '4px', 'background': 'rgba(255,255,255,0.1)'}
                ) if target else None,
                html.Small(f"Meta: {target}{unit if format_type != 'percent' else '%'}" if target else "", className="kpi-target")
            ], className="kpi-progress") if target else None
        ])
    ], className="kpi-card")

# Enhanced destination card for geographic tab
def create_enhanced_destination_card(route):
    """Crear tarjeta mejorada de destino con glassmorphism"""
    return html.Div([
        html.Div([
            html.Div([
                html.H6(route['city'], style={
                    'color': '#ffffff', 
                    'margin': '0 0 0.5rem 0', 
                    'fontWeight': '600',
                    'fontSize': '0.95rem'
                }),
                html.Div([
                    html.Span(f"{route['passengers']:,}", style={
                        'color': '#00d4ff', 
                        'fontWeight': '700',
                        'fontSize': '1.1rem'
                    }),
                    html.Span(" pax/año", style={
                        'color': '#8b92a9', 
                        'fontSize': '0.8rem',
                        'marginLeft': '4px'
                    })
                ], style={'marginBottom': '0.25rem'}),
            ], className="destination-info"),
            html.Div([
                html.Div(f"{route['load_factor']}%", style={
                    'color': '#f59e0b',
                    'fontWeight': '600',
                    'fontSize': '0.9rem'
                }),
                html.Div("Load Factor", style={
                    'color': '#8b92a9',
                    'fontSize': '0.7rem'
                })
            ], className="destination-metric")
        ], className="destination-row"),
        
        html.Div([
            DashIconify(icon="mdi:calendar", width=16, height=16, style={'marginRight': '6px', 'color': '#8b92a9'}),
            html.Span(f"{route['frequency']} vuelos/mes", style={
                'color': '#8b92a9',
                'fontSize': '0.75rem'
            }),
            html.Span(" | ", style={
                'color': '#8b92a9',
                'margin': '0 6px'
            }),
            DashIconify(icon="mdi:airplane", width=16, height=16, style={'marginRight': '4px', 'color': '#8b92a9'}),
            html.Span(f"{route['frequency']//4} vuelos/sem", style={
                'color': '#8b92a9',
                'fontSize': '0.75rem'
            })
        ], className="destination-details")
    ], className="enhanced-destination-card")

# Operations Center Components
def create_capacity_gauge(title, percentage, value, benchmark, icon, status):
    """Crear gauge visual para capacidad operativa"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                DashIconify(icon=icon, width=40, height=40, className="capacity-gauge-icon"),
                html.Div([
                    html.H2(percentage, className="gauge-percentage"),
                    html.P(title, className="gauge-title"),
                    html.Small(value, className="gauge-value"),
                    html.Small(benchmark, className="gauge-benchmark")
                ])
            ], className="gauge-content"),
            
            # Progress ring visual
            html.Div([
                dbc.Progress(
                    value=int(percentage.replace('%', '')),
                    color=status,
                    className="capacity-progress-ring",
                    style={"height": "8px"}
                )
            ], className="mt-2")
        ])
    ], className="capacity-gauge-card")

def create_status_row(zone, capacity, utilization, throughput, wait_time, status):
    """Crear fila para la tabla de estado operativo"""
    utilization_value = int(utilization.replace('%', ''))
    status_colors = {"optimal": "success", "warning": "warning", "critical": "danger"}
    
    return html.Tr([
        html.Td(zone, className="zone-name"),
        html.Td(capacity),
        html.Td([
            dbc.Progress(
                value=utilization_value,
                color=status_colors[status],
                className="mb-1",
                style={"height": "8px"}
            ),
            html.Small(utilization)
        ]),
        html.Td(throughput),
        html.Td(wait_time),
        html.Td([
            dbc.Badge(status.upper(), color=status_colors[status])
        ])
    ])

# Security Operations Components
def create_security_kpi_card(title, value, unit, target, status, icon):
    """Crear KPI card para seguridad operacional"""
    status_colors = {
        "excellent": "#00ff88",
        "good": "#00d4ff", 
        "warning": "#f59e0b",
        "critical": "#ff4757"
    }
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                DashIconify(icon=icon, width=48, height=48, className="security-kpi-icon"),
                html.Div([
                    html.H3(f"{value}", className="security-kpi-value"),
                    html.P(unit, className="security-kpi-unit"),
                    html.H6(title, className="security-kpi-title"),
                    html.Small(f"Meta: {target}", className="security-target")
                ])
            ], className="security-kpi-content"),
            
            # Status indicator
            html.Div([
                dbc.Badge(status.upper(), color=status, className="security-status-badge")
            ], className="mt-2")
        ])
    ], className="security-kpi-card")

def create_security_gauge(title, percentage, critical_threshold, icon):
    """Crear gauge circular para métricas de seguridad"""
    # Asegurar que percentage sea entero
    percentage_val = int(float(percentage)) if isinstance(percentage, (str, float)) else percentage
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                DashIconify(icon=icon, width=36, height=36, className="security-gauge-icon"),
                html.H4(f"{percentage_val}%", className="security-gauge-percentage"),
                html.P(title, className="security-gauge-title"),
                html.Small(f"Crítico: >{critical_threshold}%", className="security-gauge-threshold")
            ], className="text-center"),
            
            # Circular progress
            dbc.Progress(
                value=percentage_val,
                color="success" if percentage_val < critical_threshold else "warning" if percentage_val < 90 else "danger",
                className="security-circular-progress",
                style={"height": "8px"}
            )
        ])
    ], className="security-gauge-card")

def create_airport_map_svg():
    """Crear mapa SVG del aeropuerto AIFA con zonas de seguridad"""
    return html.Div([
        html.Div([
            # Representación visual del aeropuerto con CSS
            html.Div([
                html.Div("Terminal AIFA", className="airport-terminal"),
                html.Div("Pista 12L/30R", className="airport-runway runway-1"),
                html.Div("Pista 12R/30L", className="airport-runway runway-2"),
                html.Div("Torre Control", className="control-tower"),
                
                # Zonas de seguridad
                html.Div(className="security-zone zone-1"),
                html.Div(className="security-zone zone-2"),
                html.Div(className="security-zone zone-3"),
                html.Div(className="security-zone zone-4"),
                
                # Cámaras de seguridad
                html.Div(className="security-camera cam-1"),
                html.Div(className="security-camera cam-2"),
                html.Div(className="security-camera cam-3"),
                html.Div(className="security-camera cam-4"),
            ], className="airport-layout")
        ], className="airport-visual-container")
    ], className="map-container")

def get_security_chart_layout():
    """Layout estándar para gráficos de seguridad"""
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(10, 14, 39, 0.95)',
        'font': {'color': 'white', 'family': 'Inter', 'size': 12},
        'margin': {'l': 80, 'r': 40, 't': 40, 'b': 80},
        'xaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.15)', 'showgrid': True},
        'yaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.15)', 'showgrid': True},
        'legend': {'font': {'color': 'white'}, 'bgcolor': 'rgba(26, 31, 58, 0.9)'},
        'hovermode': 'x unified'
    }

# Customer Journey Experience Components
def create_journey_touchpoint_card(title, metric, unit, target, status, icon):
    """Crear card para cada punto del customer journey"""
    status_colors = {
        'excellent': '#00ff88',
        'good': '#f59e0b', 
        'warning': '#ff4757'
    }
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                DashIconify(icon=icon, width=36, height=36, style={'color': '#00d4ff', 'marginBottom': '0.75rem'}),
                html.H4(f"{metric}", style={'color': '#00d4ff', 'fontSize': '1.5rem', 'fontWeight': '700', 'margin': '0.5rem 0'}),
                html.P(unit, style={'color': '#ffffff', 'fontSize': '0.85rem', 'margin': '0.25rem 0'}),
                html.H6(title, style={'color': '#ffffff', 'fontSize': '0.95rem', 'fontWeight': '600', 'margin': '0.75rem 0 0.5rem 0'}),
                html.Small(f"Meta: {target}", style={'color': '#a0aec0', 'fontSize': '0.75rem', 'marginBottom': '0.75rem', 'display': 'block'}),
                dbc.Badge(status.upper(), style={
                    'backgroundColor': status_colors[status], 
                    'color': '#ffffff',
                    'fontSize': '0.7rem',
                    'fontWeight': '600',
                    'padding': '0.35rem 0.85rem',
                    'borderRadius': '8px',
                    'border': 'none',
                    'textShadow': '0 1px 2px rgba(0,0,0,0.3)',
                    'marginTop': '0.5rem'
                })
            ], style={'textAlign': 'center', 'padding': '1rem', 'minHeight': '180px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between'})
        ], style={'padding': '0.5rem'})
    ], className="journey-touchpoint-card", style={'height': '200px'})

def create_quality_kpi_card(title, value, unit, change, trend, icon):
    """KPI card con indicador de tendencia para calidad"""
    trend_icon = "mdi:trending-up" if trend == 'up' else "mdi:trending-down" if trend == 'down' else "mdi:trending-neutral"
    trend_color = "#00ff88" if trend == 'up' else "#ff4757" if trend == 'down' else "#f59e0b"
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                DashIconify(icon=icon, width=44, height=44, style={'color': '#00d4ff', 'marginBottom': '0.75rem'}),
                html.H3(f"{value}", style={'color': '#00d4ff', 'fontSize': '1.7rem', 'fontWeight': '700', 'margin': '0.5rem 0'}),
                html.P(unit, style={'color': '#ffffff', 'fontSize': '0.9rem', 'margin': '0.25rem 0'}),
                html.H6(title, style={'color': '#ffffff', 'fontSize': '1rem', 'fontWeight': '600', 'margin': '0.75rem 0 0.5rem 0'}),
                html.Div([
                    DashIconify(icon=trend_icon, width=18, height=18, style={'color': trend_color}),
                    html.Small(f"{change:+.1f}" if isinstance(change, (int, float)) else str(change), 
                              style={'color': trend_color, 'marginLeft': '6px', 'fontSize': '0.85rem', 'fontWeight': '600'})
                ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'gap': '0.25rem', 'marginTop': '0.5rem'})
            ], style={'textAlign': 'center', 'padding': '1rem', 'minHeight': '180px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between'})
        ], style={'padding': '0.5rem'})
    ], className="quality-kpi-card", style={'height': '200px'})

def create_nps_score_display(score, promoters, passives, detractors):
    """Display principal del NPS con breakdown"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.H2(f"{score}", style={
                    'fontSize': '2.2rem', 'fontWeight': '800', 'color': '#00d4ff', 
                    'margin': '0 0 0.5rem 0', 'textShadow': '0 0 20px rgba(0, 212, 255, 0.3)'
                }),
                html.P("NPS Score", style={'fontSize': '1rem', 'color': '#ffffff', 'marginBottom': '1rem'}),
                html.Div([
                    html.Div([
                        html.Span(f"{promoters}%", style={'fontSize': '1rem', 'fontWeight': '700', 'color': '#00ff88', 'display': 'block', 'marginBottom': '0.25rem'}),
                        html.P("Promotores", style={'fontSize': '0.75rem', 'color': '#ffffff', 'margin': '0'})
                    ], style={'textAlign': 'center', 'flex': '1'}),
                    html.Div([
                        html.Span(f"{passives}%", style={'fontSize': '1rem', 'fontWeight': '700', 'color': '#f59e0b', 'display': 'block', 'marginBottom': '0.25rem'}), 
                        html.P("Pasivos", style={'fontSize': '0.75rem', 'color': '#ffffff', 'margin': '0'})
                    ], style={'textAlign': 'center', 'flex': '1'}),
                    html.Div([
                        html.Span(f"{detractors}%", style={'fontSize': '1rem', 'fontWeight': '700', 'color': '#ff4757', 'display': 'block', 'marginBottom': '0.25rem'}),
                        html.P("Detractores", style={'fontSize': '0.75rem', 'color': '#ffffff', 'margin': '0'})
                    ], style={'textAlign': 'center', 'flex': '1'})
                ], style={'display': 'flex', 'justifyContent': 'space-around', 'gap': '0.5rem'})
            ], style={'textAlign': 'center', 'padding': '1rem', 'minHeight': '180px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between'})
        ], style={'padding': '0.5rem'})
    ], className="nps-score-card", style={'height': '200px'})

def create_satisfaction_stars(rating):
    """Crear display de estrellas para rating de satisfacción"""
    stars = []
    for i in range(5):
        if i < int(rating):
            stars.append(DashIconify(icon="mdi:star", width=24, height=24, style={'color': '#f59e0b'}))
        elif i < rating:
            stars.append(DashIconify(icon="mdi:star-half-full", width=24, height=24, style={'color': '#f59e0b'}))
        else:
            stars.append(DashIconify(icon="mdi:star-outline", width=24, height=24, style={'color': '#8b92a9'}))
    return html.Div(stars, className="satisfaction-stars")

def get_quality_chart_layout():
    """Layout base para gráficos de calidad de servicio"""
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(10, 14, 39, 0.95)',
        'font': {'color': 'white', 'family': 'Inter', 'size': 12},
        'margin': {'l': 80, 'r': 40, 't': 40, 'b': 80},
        'xaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.15)', 'showgrid': True},
        'yaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.15)', 'showgrid': True},
        'legend': {'font': {'color': 'white'}, 'bgcolor': 'rgba(26, 31, 58, 0.9)'},
        'hovermode': 'x unified'
    }

# Executive Dashboard Components for Productivity
def create_productivity_kpi_enhanced(title, current, benchmark, unit, trend, icon, performance):
    """KPI card ejecutiva con benchmark comparison"""
    trend_color = "#00ff88" if trend == 'up' else "#ff4757" if trend == 'down' else "#f59e0b"
    perf_color = "#00ff88" if performance >= 110 else "#f59e0b" if performance >= 100 else "#ff4757"
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                DashIconify(icon=icon, width=48, height=48, style={'color': '#00d4ff', 'marginBottom': '0.75rem'}),
                html.H3(f"{current:,}" if isinstance(current, int) else str(current), 
                       style={'color': '#00d4ff', 'fontSize': '1.8rem', 'fontWeight': '700', 'margin': '0.5rem 0'}),
                html.P(unit, style={'color': '#ffffff', 'fontSize': '0.9rem', 'margin': '0.25rem 0'}),
                html.H6(title, style={'color': '#ffffff', 'fontSize': '1rem', 'fontWeight': '600', 'margin': '0.75rem 0 0.5rem 0'}),
                
                # Benchmark comparison bar
                html.Div([
                    html.Small(f"Benchmark: {benchmark:,}", style={'color': '#a0aec0', 'fontSize': '0.75rem', 'display': 'block', 'marginBottom': '0.5rem'}),
                    dbc.Progress([
                        dbc.Progress(value=min(performance, 150), 
                                   color="success" if performance >= 110 else "warning" if performance >= 100 else "danger",
                                   bar=True, 
                                   style={'height': '6px'})
                    ], max=150, style={'height': '6px', 'backgroundColor': 'rgba(255,255,255,0.1)'}),
                    html.Div([
                        html.Span(f"{performance:.1f}%", style={'color': perf_color, 'fontWeight': '600', 'fontSize': '0.85rem'}),
                        html.Span(" vs benchmark", style={'color': '#a0aec0', 'fontSize': '0.75rem', 'marginLeft': '4px'})
                    ], style={'marginTop': '0.5rem'})
                ], style={'marginTop': '1rem'})
            ], style={'textAlign': 'center', 'padding': '1rem'})
        ], style={'padding': '0.5rem'})
    ], className="productivity-kpi-card", style={'height': '240px'})

def create_executive_metric(title, value, change, unit):
    """Métrica ejecutiva para summary section"""
    change_color = "#00ff88" if change.startswith('+') else "#ff4757" if change.startswith('-') else "#f59e0b"
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.H4(value, style={'color': '#00d4ff', 'fontSize': '1.4rem', 'fontWeight': '700', 'margin': '0'}),
                html.P(title, style={'color': '#ffffff', 'fontSize': '0.85rem', 'margin': '0.5rem 0 0.25rem 0'}),
                html.Div([
                    html.Span(change, style={'color': change_color, 'fontSize': '0.8rem', 'fontWeight': '600'}),
                    html.Span(f" {unit}", style={'color': '#a0aec0', 'fontSize': '0.75rem', 'marginLeft': '4px'})
                ])
            ], style={'textAlign': 'center'})
        ], style={'padding': '1rem'})
    ], className="executive-metric-card")

def calculate_productivity_index(kpis_dict):
    """Calcula índice consolidado de productividad"""
    performances = [kpi['performance'] for kpi in kpis_dict.values()]
    return sum(performances) / len(performances)

def get_productivity_chart_layout():
    """Layout estándar para gráficos ejecutivos de productividad"""
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(10, 14, 39, 0.95)',
        'font': {'color': 'white', 'family': 'Inter', 'size': 12},
        'margin': {'l': 80, 'r': 40, 't': 40, 'b': 80},
        'xaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.15)', 'showgrid': True},
        'yaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.15)', 'showgrid': True},
        'legend': {'font': {'color': 'white'}, 'bgcolor': 'rgba(26, 31, 58, 0.9)'},
        'hovermode': 'x unified'
    }

# Bloomberg Terminal Components
def create_trading_card(label, value, change, trend):
    """Crear trading card estilo Bloomberg"""
    return dbc.Card([
        dbc.CardBody([
            html.P(label, className="trading-label"),
            html.H2(value, className="trading-value"),
            html.Div([
                DashIconify(
                    icon="mdi:trending-up" if trend == "positive" else "mdi:trending-down", 
                    width=20, height=20, 
                    className="me-2"
                ),
                change
            ], className=f"trading-change {trend}")
        ])
    ], className="trading-card")

def create_financial_kpi(title, value, change, icon):
    """Crear KPI financiero con icono"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                DashIconify(icon=icon, width=32, height=32, className="financial-icon"),
                html.Div([
                    html.H4(value, className="financial-kpi-value"),
                    html.P(title, className="financial-kpi-title"),
                    html.Small(change, className="financial-kpi-change")
                ])
            ], className="d-flex align-items-center")
        ])
    ], className="financial-kpi-card")

def create_financial_row(metric, current, target, variance, trend, industry, performance):
    """Crear fila para la matriz de rendimiento financiero"""
    trend_icon = "mdi:trending-up" if trend == "up" else "mdi:trending-down" if trend == "down" else "mdi:trending-neutral"
    trend_color = "text-success" if trend == "up" else "text-danger" if trend == "down" else "text-warning"
    
    return html.Tr([
        html.Td(metric, className="metric-name"),
        html.Td(current),
        html.Td(target),
        html.Td(variance, className="text-success" if "+" in variance else "text-danger"),
        html.Td([DashIconify(icon=trend_icon, width=16, height=16, className=trend_color)]),
        html.Td(industry),
        html.Td([
            dbc.Badge(
                "Excelente" if performance == "excellent" else "Bueno" if performance == "good" else "Advertencia",
                color="success" if performance == "excellent" else "info" if performance == "good" else "warning"
            )
        ])
    ])

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.Div([
                html.Img(
                    src="/assets/aifa-logo.jpg",
                    height="50px",
                    style={
                        'marginRight': '15px',
                        'backgroundColor': 'transparent',
                        'isolation': 'isolate'
                    },
                    className="header-logo"
                ),
                html.Div([
                    html.H1("Centro de Operaciones AIFA", className="header-title"),
                    html.P("Aeropuerto Internacional Felipe Ángeles", className="header-subtitle")
                ], className="header-text")
            ], className="header-content"),
            html.Div([
                html.Div([
                    html.Span("Última actualización: ", className="update-label"),
                    html.Span(id="live-update-time", className="update-time")
                ], className="update-info"),
                dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0)
            ], className="header-right")
        ], className="header-container")
    ], className="header"),
    
    # Navigation tabs
    dbc.Tabs([
        dbc.Tab(label="KPIs Estratégicos", tab_id="strategic", 
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Análisis Geográfico", tab_id="geographic",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Control 360°", tab_id="control-360",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Análisis Financiero", tab_id="financial",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Capacidad Operativa", tab_id="capacity",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Seguridad", tab_id="security",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Calidad de Servicio", tab_id="quality",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Productividad", tab_id="productivity",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'}),
        dbc.Tab(label="Metodología", tab_id="metodologia",
                label_style={'color': '#8b92a9'},
                active_label_style={'color': '#00d4ff', 'background': 'rgba(0, 212, 255, 0.1)'})
    ], id="tabs", active_tab="strategic", className="nav-tabs"),
    
    # Tab content
    html.Div(id="tab-content", className="content-area")
])

# Tab content callback
@callback(Output("tab-content", "children"),
          Input("tabs", "active_tab"))
def render_tab_content(active_tab):
    if active_tab == "strategic":
        return render_strategic_tab()
    elif active_tab == "geographic":
        return render_geographic_tab()
    elif active_tab == "control-360":
        return render_control_360_tab()
    elif active_tab == "financial":
        return render_financial_tab()
    elif active_tab == "capacity":
        return render_capacity_tab()
    elif active_tab == "security":
        return render_security_tab()
    elif active_tab == "quality":
        return render_quality_tab()
    elif active_tab == "productivity":
        return render_productivity_tab()
    elif active_tab == "metodologia":
        return render_metodologia_tab()
    else:
        return html.Div([
            html.H4(f"Módulo: {active_tab.replace('_', ' ').title()}", 
                   style={'color': '#8b92a9', 'textAlign': 'center', 'marginTop': '50px'}),
            html.P("En desarrollo - Framework implementado", 
                  style={'color': '#8b92a9', 'textAlign': 'center'})
        ])

def render_strategic_tab():
    kpi_data = get_kpi_data()
    
    return html.Div([
        # KPI Cards Row 1
        dbc.Row([
            dbc.Col([
                create_kpi_card(
                    "Participación Nacional Pasajeros",
                    kpi_data['participation_passengers']['current'],
                    kpi_data['participation_passengers']['change'],
                    "mdi:account-group",
                    kpi_data['participation_passengers']['target']
                )
            ], width=4),
            dbc.Col([
                create_kpi_card(
                    "Participación Nacional Operaciones",
                    kpi_data['participation_operations']['current'],
                    kpi_data['participation_operations']['change'],
                    "mdi:airplane-takeoff",
                    kpi_data['participation_operations']['target']
                )
            ], width=4),
            dbc.Col([
                create_kpi_card(
                    "Participación Nacional Carga",
                    kpi_data['participation_cargo']['current'],
                    kpi_data['participation_cargo']['change'],
                    "mdi:package-variant",
                    kpi_data['participation_cargo']['target']
                )
            ], width=4)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                create_kpi_card(
                    "Crecimiento vs Mercado",
                    kpi_data['growth_vs_market']['current'],
                    kpi_data['growth_vs_market']['change'],
                    "mdi:trending-up"
                )
            ], width=4),
            dbc.Col([
                create_kpi_card(
                    "Puntualidad de Vuelos",
                    kpi_data['punctuality']['current'],
                    kpi_data['punctuality']['change'],
                    "mdi:clock-check-outline",
                    kpi_data['punctuality']['target']
                )
            ], width=4),
            dbc.Col([
                create_kpi_card(
                    "Utilización de Rutas",
                    kpi_data['route_utilization']['current'],
                    kpi_data['route_utilization']['change'],
                    "mdi:map-marker-path",
                    kpi_data['route_utilization']['target']
                )
            ], width=4)
        ], className="mb-4"),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Evolución Participación de Mercado", className="chart-title"),
                        html.Small("Últimos 12 meses", className="chart-subtitle")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="participation-trend-chart")
                    ])
                ], className="chart-card")
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Progreso Meta Anual", className="chart-title"),
                        html.Small("Participación de pasajeros", className="chart-subtitle")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="progress-gauge")
                    ])
                ], className="chart-card")
            ], width=4)
        ], className="mb-4"),
        
        # Comparison Table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Comparativo Aeropuertos Mexicanos", className="chart-title"),
                        html.Small("Participación de mercado nacional", className="chart-subtitle")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="airport-comparison-chart")
                    ])
                ], className="chart-card")
            ], width=12)
        ])
    ])

def render_geographic_tab():
    route_data = get_route_data()
    
    return html.Div([
        html.H4("Análisis Geográfico", className="page-title"),
        html.P("Red de destinos, rutas estratégicas y análisis de mercado", className="page-subtitle"),
        
        # KPIs Geográficos - Grid 2x3 Balanceado y Responsive
        dbc.Row([
            dbc.Col([
                create_kpi_card("Destinos Activos", 28, 3, "mdi:map-marker-multiple", None, "", "integer")
            ], lg=4, md=6, sm=12),
            dbc.Col([
                create_kpi_card("Países Conectados", 8, 2, "mdi:earth", None, "", "integer")
            ], lg=4, md=6, sm=12),
            dbc.Col([
                create_kpi_card("Rutas Internacionales", 12, 4, "mdi:airplane", None, "", "integer")
            ], lg=4, md=6, sm=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                create_kpi_card("Rutas Domésticas", 16, 1, "mdi:home-map-marker", None, "", "integer")
            ], lg=4, md=6, sm=12),
            dbc.Col([
                create_kpi_card("Nuevas Rutas 2024", 7, 7, "mdi:plus-circle", None, "", "integer")
            ], lg=4, md=6, sm=12),
            dbc.Col([
                create_kpi_card("Factor Carga Promedio", 84.2, 2.1, "mdi:gauge", None, "%", "decimal")
            ], lg=4, md=6, sm=12)
        ], className="mb-4"),
        
        
        # Panel de Destinos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Principales Destinos", className="chart-title"),
                        html.Small("Red de rutas y conexiones AIFA", className="chart-subtitle")
                    ]),
                    dbc.CardBody([
                        html.Div([
                            create_enhanced_destination_card(route) for route in route_data
                        ])
                    ])
                ], className="chart-card")
            ], width=12)
        ], className="mb-4"),
        
        # Gráficas Simplificadas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Distribución por Región", className="chart-title"),
                        html.Small("Tráfico de pasajeros por zona geográfica", className="chart-subtitle")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="geographic-distribution-chart")
                    ])
                ], className="chart-card")
            ], width=12)
        ])
    ])

def render_control_360_tab():
    """Renderiza el tab del Control 360° con la demo 3D interactiva"""
    return html.Div([
        html.H4("Control 360° - Red Global de Rutas AIFA", className="page-title"),
        html.P("Sistema de Navegación Ejecutiva | Tecnología Aeroportuaria Premium", 
               className="page-subtitle"),
        
        # Container principal para la demo 3D
        html.Div([
            # Iframe que carga la demo 3D routes
            html.Iframe(
                src="/assets/demo_3d_routes.html",
                className="control-360-iframe"
            )
        ], className="control-360-container")
    ])

def render_financial_tab():
    """Renderiza el tab financiero con estilo Bloomberg Terminal profesional"""
    return html.Div([
        # Bloomberg Terminal Header
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H1("AIFA Terminal Financiero", className="terminal-title"),
                    html.P("Análisis Financiero en Tiempo Real • Métricas de Rendimiento", className="terminal-subtitle")
                ], className="bloomberg-header-content")
            ])
        ], className="bloomberg-header mb-4"),
        
        # Trading Cards - Métricas Principales
        dbc.Row([
            dbc.Col([
                create_trading_card("Ingresos", "$290M MXN", "+5.4% vs mes anterior", "positive")
            ], width=3),
            dbc.Col([
                create_trading_card("Margen EBITDA", "29.3%", "+1.8% vs mes anterior", "positive") 
            ], width=3),
            dbc.Col([
                create_trading_card("ROI Anual", "22.1%", "+3.2% vs año anterior", "positive")
            ], width=3),
            dbc.Col([
                create_trading_card("Flujo Operativo", "$127M MXN", "+8.1% vs plan", "positive")
            ], width=3)
        ], className="trading-grid mb-4"),
        
        # KPI Grid Financiero
        dbc.Row([
            dbc.Col([create_financial_kpi("Ingresos por Pasajero", "$148", "+$12 vs objetivo", "mdi:account-cash")], width=3),
            dbc.Col([create_financial_kpi("Ingresos Aeronáuticos", "$89", "+$8 vs anterior", "mdi:airplane")], width=3),
            dbc.Col([create_financial_kpi("Ingresos No-Aeronáuticos", "$59", "+$4 vs anterior", "mdi:store")], width=3),
            dbc.Col([create_financial_kpi("% No-Aeronáuticos", "39.9%", "+2.1% vs plan", "mdi:percent")], width=3)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([create_financial_kpi("Costo por Operación", "$2,847", "-$156 optimización", "mdi:calculator")], width=3),
            dbc.Col([create_financial_kpi("Costo por Pasajero", "$42", "-$3 eficiencia", "mdi:wallet")], width=3),
            dbc.Col([create_financial_kpi("Costos Personal", "34.2%", "-1.8% del revenue", "mdi:account-group")], width=3),
            dbc.Col([create_financial_kpi("Margen Operativo", "18.7%", "+2.4% vs objetivo", "mdi:chart-line")], width=3)
        ], className="mb-4"),
        
        # Charts Grid 2x2
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Análisis de Flujos de Ingresos", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="revenue-donut", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Estructura de Costos", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="cost-waterfall", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Rentabilidad vs Benchmarks", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="profitability-trends", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Análisis de Flujo de Efectivo", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="cashflow-analysis", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-4"),
        
        # Financial Performance Matrix
        dbc.Card([
            dbc.CardHeader([
                html.H5("Matriz de Rendimiento Financiero", className="chart-title")
            ]),
            dbc.CardBody([
                dbc.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("Métrica"),
                            html.Th("Actual"),
                            html.Th("Objetivo"),
                            html.Th("Variación"),
                            html.Th("Tendencia"),
                            html.Th("Promedio Industria"),
                            html.Th("Rendimiento")
                        ])
                    ]),
                    html.Tbody([
                        create_financial_row("Ingresos por Pasajero", "$148", "$145", "+$3", "up", "$142", "excellent"),
                        create_financial_row("Margen EBITDA", "29.3%", "25.0%", "+4.3%", "up", "22.0%", "excellent"),
                        create_financial_row("Costo por Operación", "$2,847", "$3,000", "-$153", "down", "$3,200", "excellent"),
                        create_financial_row("% Ingresos No-Aero", "39.9%", "40.0%", "-0.1%", "stable", "35.0%", "good"),
                        create_financial_row("Margen Operativo", "18.7%", "16.0%", "+2.7%", "up", "15.0%", "excellent"),
                        create_financial_row("% Costos Personal", "34.2%", "35.0%", "-0.8%", "down", "38.0%", "good")
                    ])
                ], striped=True, hover=True, className="financial-table")
            ])
        ], className="financial-table-container")
    ])

def render_capacity_tab():
    """Renderiza el tab de capacidad operativa como centro de control aeroportuario avanzado"""
    return html.Div([
        # Operations Control Header
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H1("Centro de Control de Capacidad Operativa", className="section-title"),
                    html.P("Monitoreo en Tiempo Real • Utilización de Recursos • Optimización de Flujos", 
                           className="section-subtitle"),
                    html.Div([
                        dbc.Badge("OPERACIONAL", color="success", className="me-2"),
                        dbc.Badge("SISTEMA ACTIVO", color="info", className="me-2"),
                        dbc.Badge("99.7% UPTIME", color="warning", className="me-2"),
                        dbc.Badge("0 ALERTAS CRÍTICAS", color="success")
                    ], className="status-badges")
                ])
            ])
        ], className="operations-header mb-4"),
        
        # Gauges Grid - Visual KPIs
        dbc.Row([
            dbc.Col([
                create_capacity_gauge("Check-in", "98%", "245 m²", "2.1 m²/M pax", "mdi:check-circle", "success")
            ], width=4),
            dbc.Col([
                create_capacity_gauge("Salas Espera", "82%", "890 m²", "7.2 m²/M pax", "mdi:seat", "info")
            ], width=4),
            dbc.Col([
                create_capacity_gauge("Seguridad", "76%", "120 m²", "1.0 m²/M pax", "mdi:shield-check", "warning")
            ], width=4)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                create_capacity_gauge("Área Estéril", "85%", "450 m²", "3.8 m²/M pax", "mdi:lock", "success")
            ], width=4),
            dbc.Col([
                create_capacity_gauge("Equipajes", "80%", "2,400 bags/hr", "3,000 máx", "mdi:bag-suitcase", "info")
            ], width=4),
            dbc.Col([
                create_capacity_gauge("Puertas", "75%", "18/24 activas", "24 disponibles", "mdi:airplane-takeoff", "info")
            ], width=4)
        ], className="mb-4"),
        
        # Visual Analytics Grid
        dbc.Row([
            dbc.Col([
                # Heatmap de densidad
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Mapa de Calor - Densidad por Hora", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="capacity-heatmap", style={"height": "350px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                # Utilization trends
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Tendencias de Utilización", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="utilization-trends", style={"height": "350px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                # Capacity vs Demand
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Capacidad vs Demanda", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="capacity-demand", style={"height": "350px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                # Real-time monitor gauge
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Monitor General en Tiempo Real", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="general-gauge", style={"height": "350px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-4"),
        
        # Live Operations Table
        dbc.Card([
            dbc.CardHeader([
                html.H5("Estado Operativo en Tiempo Real", className="chart-title"),
                html.Small("Actualización automática cada 30 segundos", className="text-muted")
            ]),
            dbc.CardBody([
                dbc.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("Zona/Sistema"),
                            html.Th("Capacidad"),
                            html.Th("Utilización"),
                            html.Th("Throughput"),
                            html.Th("Tiempo Espera"),
                            html.Th("Estado")
                        ])
                    ]),
                    html.Tbody([
                        create_status_row("Check-in Counters", "32/40", "98%", "180 pax/hr", "4.2 min", "optimal"),
                        create_status_row("Security Checkpoints", "8/10", "76%", "420 pax/hr", "8.1 min", "optimal"),
                        create_status_row("Immigration", "6/8", "68%", "380 pax/hr", "3.5 min", "optimal"),
                        create_status_row("Baggage Claim", "4/6", "85%", "2,400 bags/hr", "12.8 min", "warning"),
                        create_status_row("Gates", "18/24", "75%", "3,200 pax/hr", "N/A", "optimal"),
                        create_status_row("Parking", "2,847/3,500", "81%", "650 veh/hr", "N/A", "optimal")
                    ])
                ], striped=True, hover=True, className="operations-table")
            ])
        ], className="operations-table-container")
    ])

def render_security_tab():
    """Dashboard Bloomberg Terminal para Seguridad Operacional AIFA con 15 KPIs oficiales"""
    security_data = get_security_data()
    
    return html.Div([
        # Security Operations Header
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H1("Centro de Control de Seguridad Operacional", className="security-header-title"),
                    html.P("Monitoreo 15 KPIs Oficiales AIFA • Cumplimiento OACI • Gestión de Riesgos", 
                           className="security-header-subtitle"),
                    html.Div([
                        dbc.Badge("SMS ACTIVO", color="success", className="me-2"),
                        dbc.Badge("NIVEL SEGURIDAD A", color="info", className="me-2"), 
                        dbc.Badge("94.5/100 SCORE", color="warning", className="me-2"),
                        dbc.Badge("CUMPLIMIENTO OACI", color="success")
                    ], className="security-status-badges")
                ])
            ])
        ], className="security-operations-header mb-4"),
        
        # KPIs Principales (Top Row - 5 KPIs críticos)
        html.H5("KPIs Críticos de Seguridad", className="section-subtitle mb-3"),
        dbc.Row([
            dbc.Col([
                create_security_kpi_card(
                    "Incidentes en Pista",
                    security_data['runway_incidents']['rate'], 
                    security_data['runway_incidents']['unit'],
                    security_data['runway_incidents']['target'],
                    security_data['runway_incidents']['status'],
                    "mdi:runway"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Accidentes Mortales",
                    security_data['fatal_accidents']['rate'],
                    security_data['fatal_accidents']['unit'],
                    security_data['fatal_accidents']['target'],
                    security_data['fatal_accidents']['status'],
                    "mdi:alert-circle"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Accidentes Laborales",
                    security_data['work_accidents']['rate'],
                    security_data['work_accidents']['unit'],
                    security_data['work_accidents']['target'],
                    security_data['work_accidents']['status'],
                    "mdi:hard-hat"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Incursiones Pista",
                    security_data['runway_incursions']['rate'],
                    security_data['runway_incursions']['unit'],
                    security_data['runway_incursions']['target'],
                    security_data['runway_incursions']['status'],
                    "mdi:airplane-alert"
                )
            ], width=3, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Choques con Aves",
                    security_data['bird_strikes']['rate'],
                    security_data['bird_strikes']['unit'],
                    security_data['bird_strikes']['target'],
                    security_data['bird_strikes']['status'],
                    "mdi:bird"
                )
            ], width=3, className="mb-3")
        ]),
        
        # Centro de Control Visual
        html.H5("Centro de Control Visual", className="section-subtitle mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Mapa Aeroportuario AIFA", className="chart-title")
                    ]),
                    dbc.CardBody([
                        create_airport_map_svg()
                    ])
                ], className="chart-card")
            ], width=8),
            
            dbc.Col([
                # Panel de incidentes tiempo real
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Incidentes Tiempo Real", className="chart-title")
                    ]),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                DashIconify(icon="mdi:check-circle", width=24, height=24, style={"color": "#00ff88"}),
                                html.Span("Sin incidentes críticos", className="ms-2")
                            ], className="incident-row mb-2"),
                            html.Div([
                                DashIconify(icon="mdi:information", width=24, height=24, style={"color": "#00d4ff"}),
                                html.Span("FOD reportado Pista 12L", className="ms-2")
                            ], className="incident-row mb-2"),
                            html.Div([
                                DashIconify(icon="mdi:clock", width=24, height=24, style={"color": "#f59e0b"}),
                                html.Span("Inspección rutinaria 14:30", className="ms-2")
                            ], className="incident-row mb-2")
                        ])
                    ])
                ], className="chart-card"),
                
                # Estado sistemas críticos
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Sistemas Críticos", className="chart-title")
                    ]),
                    dbc.CardBody([
                        create_security_gauge("Iluminación", 99, 85, "mdi:lightbulb"),
                        create_security_gauge("Cámaras", 96, 80, "mdi:camera"),
                        create_security_gauge("Comunicaciones", 99, 90, "mdi:radio")
                    ])
                ], className="chart-card mt-3")
            ], width=4)
        ], className="mb-4"),
        
        # Dashboard Analítico (4 gráficos)
        html.H5("Análisis de Tendencias y Riesgos", className="section-subtitle mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Tendencias Mensuales", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="security-trends-chart", style={"height": "320px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Comparativo vs Estándares OACI", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="security-standards-chart", style={"height": "320px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Matriz de Riesgos por Zona", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="security-risk-matrix", style={"height": "320px"})
                    ])
                ], className="chart-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Distribución de Tipos de Incidentes", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="security-incidents-distribution", style={"height": "320px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-4"),
        
        # Métricas Operacionales (Grid de 10 KPIs restantes)
        html.H5("Métricas Operacionales Complementarias", className="section-subtitle mb-3"),
        dbc.Row([
            dbc.Col([
                create_security_kpi_card(
                    "Personal Seguridad",
                    security_data['security_staff']['rate'],
                    security_data['security_staff']['unit'],
                    security_data['security_staff']['target'],
                    security_data['security_staff']['status'],
                    "mdi:security"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Incidentes/Movimiento",
                    security_data['incident_movements']['rate'],
                    security_data['incident_movements']['unit'],
                    security_data['incident_movements']['target'],
                    security_data['incident_movements']['status'],
                    "mdi:airplane-settings"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Densidad Cámaras",
                    security_data['cameras_density']['rate'],
                    security_data['cameras_density']['unit'],
                    security_data['cameras_density']['target'],
                    security_data['cameras_density']['status'],
                    "mdi:camera-outline"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Eventos Fauna",
                    security_data['wildlife_events']['rate'],
                    security_data['wildlife_events']['unit'],
                    security_data['wildlife_events']['target'],
                    security_data['wildlife_events']['status'],
                    "mdi:paw"
                )
            ], width=3, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Luces Funcionales",
                    security_data['lighting_functional']['rate'],
                    security_data['lighting_functional']['unit'],
                    security_data['lighting_functional']['target'],
                    security_data['lighting_functional']['status'],
                    "mdi:lightbulb-on"
                )
            ], width=3, className="mb-3")
        ]),
        
        dbc.Row([
            dbc.Col([
                create_security_kpi_card(
                    "Incidentes Iluminación",
                    security_data['lighting_incidents']['rate'],
                    security_data['lighting_incidents']['unit'],
                    security_data['lighting_incidents']['target'],
                    security_data['lighting_incidents']['status'],
                    "mdi:lightbulb-alert"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Oquedades Atendidas",
                    security_data['pothole_attended']['rate'],
                    security_data['pothole_attended']['unit'],
                    security_data['pothole_attended']['target'],
                    security_data['pothole_attended']['status'],
                    "mdi:road-variant"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Mantenimiento Pistas",
                    security_data['runway_maintenance']['rate'],
                    security_data['runway_maintenance']['unit'],
                    security_data['runway_maintenance']['target'],
                    security_data['runway_maintenance']['status'],
                    "mdi:runway"
                )
            ], width=2, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Reportes FOD",
                    security_data['fod_reports']['rate'],
                    security_data['fod_reports']['unit'],
                    security_data['fod_reports']['target'],
                    security_data['fod_reports']['status'],
                    "mdi:alert-box"
                )
            ], width=3, className="mb-3"),
            dbc.Col([
                create_security_kpi_card(
                    "Daños FOD",
                    security_data['fod_damage']['rate'],
                    security_data['fod_damage']['unit'],
                    security_data['fod_damage']['target'],
                    security_data['fod_damage']['status'],
                    "mdi:airplane-alert"
                )
            ], width=3, className="mb-3")
        ])
    ])

def render_quality_tab():
    """Customer Journey Experience Dashboard con 11 KPIs oficiales AIFA"""
    quality_data = get_quality_data()
    journey_data = get_customer_journey_data()
    nps_breakdown = quality_data['nps_breakdown']
    
    return html.Div([
        # Customer Journey Experience Header
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H1("Customer Journey Experience AIFA", className="quality-header-title"),
                    html.P("Monitoreo 11 KPIs Oficiales • Experiencia del Pasajero • NPS 67/100", 
                           className="quality-header-subtitle"),
                    html.Div([
                        dbc.Badge("SATISFACCIÓN 4.6/5", color="success", className="me-2"),
                        dbc.Badge("NPS EXCELENTE", color="info", className="me-2"),
                        dbc.Badge("ESTÁNDARES OACI", color="warning", className="me-2"),
                        dbc.Badge("TIEMPO REAL", color="success")
                    ], className="quality-status-badges")
                ])
            ])
        ], className="quality-operations-header mb-4"),
        
        # Customer Journey Timeline (6 Touchpoints)
        html.H5("Customer Journey Timeline", className="section-subtitle mb-3"),
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        create_journey_touchpoint_card(
                            "Llegada/Acceso",
                            f"{journey_data['llegada']['score']}/5",
                            f"{journey_data['llegada']['time']} min",
                            f"<{journey_data['llegada']['target']} min",
                            journey_data['llegada']['status'],
                            journey_data['llegada']['icon']
                        )
                    ], width=2),
                    dbc.Col([
                        create_journey_touchpoint_card(
                            "Check-in",
                            f"{journey_data['checkin']['score']}/5",
                            f"{journey_data['checkin']['time']} min",
                            f"<{journey_data['checkin']['target']} min",
                            journey_data['checkin']['status'],
                            journey_data['checkin']['icon']
                        )
                    ], width=2),
                    dbc.Col([
                        create_journey_touchpoint_card(
                            "Control Seguridad",
                            f"{journey_data['seguridad']['score']}/5",
                            f"{journey_data['seguridad']['time']} min",
                            f"<{journey_data['seguridad']['target']} min",
                            journey_data['seguridad']['status'],
                            journey_data['seguridad']['icon']
                        )
                    ], width=2),
                    dbc.Col([
                        create_journey_touchpoint_card(
                            "Área Comercial",
                            f"{journey_data['comercial']['score']}/5",
                            f"{journey_data['comercial']['time']} min",
                            journey_data['comercial']['target'],
                            journey_data['comercial']['status'],
                            journey_data['comercial']['icon']
                        )
                    ], width=2),
                    dbc.Col([
                        create_journey_touchpoint_card(
                            "Embarque",
                            f"{journey_data['embarque']['score']}/5",
                            f"{journey_data['embarque']['time']} min",
                            f"<{journey_data['embarque']['target']} min",
                            journey_data['embarque']['status'],
                            journey_data['embarque']['icon']
                        )
                    ], width=2),
                    dbc.Col([
                        create_journey_touchpoint_card(
                            "Equipaje",
                            f"{journey_data['equipaje']['score']}/5",
                            f"{journey_data['equipaje']['time']} min",
                            f"<{journey_data['equipaje']['target']} min",
                            journey_data['equipaje']['status'],
                            journey_data['equipaje']['icon']
                        )
                    ], width=2)
                ])
            ])
        ], className="journey-timeline-container mb-4"),
        
        # KPIs Dashboard Principal (4 cards principales)
        html.H5("KPIs Dashboard Principal", className="section-subtitle mb-3"),
        dbc.Row([
            dbc.Col([
                create_nps_score_display(
                    quality_data['nps_score']['score'],
                    nps_breakdown['promotores'],
                    nps_breakdown['pasivos'],
                    nps_breakdown['detractores']
                )
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            DashIconify(icon="mdi:heart", width=44, height=44, style={'color': '#00d4ff', 'marginBottom': '0.75rem'}),
                            html.H3(f"{quality_data['satisfaccion_general']['score']}/5", style={'color': '#00d4ff', 'fontSize': '1.7rem', 'fontWeight': '700', 'margin': '0.5rem 0'}),
                            html.P("Satisfacción General", style={'color': '#ffffff', 'fontSize': '1rem', 'fontWeight': '600', 'margin': '0.75rem 0 0.5rem 0'}),
                            create_satisfaction_stars(quality_data['satisfaccion_general']['score']),
                            html.Small(f"Meta: >{quality_data['satisfaccion_general']['target']}/5", style={'color': '#a0aec0', 'fontSize': '0.8rem', 'marginTop': '0.5rem', 'display': 'block'})
                        ], style={'textAlign': 'center', 'padding': '1rem', 'minHeight': '180px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between'})
                    ], style={'padding': '0.5rem'})
                ], className="quality-kpi-card", style={'height': '200px'})
            ], width=3),
            dbc.Col([
                create_quality_kpi_card(
                    "Capacidad Diaria",
                    quality_data['capacidad_diaria']['value'],
                    quality_data['capacidad_diaria']['unit'],
                    quality_data['capacidad_diaria']['trend'],
                    'up',
                    "mdi:airplane-takeoff"
                )
            ], width=3),
            dbc.Col([
                create_quality_kpi_card(
                    "Demora Promedio",
                    quality_data['demora_promedio']['avg'],
                    quality_data['demora_promedio']['unit'],
                    quality_data['demora_promedio']['trend'],
                    'down',
                    "mdi:clock-outline"
                )
            ], width=3)
        ], className="mb-4"),
        
        # Analytics Avanzados (4 gráficos)
        html.H5("Analytics Avanzados", className="section-subtitle mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Heatmap Satisfacción por Áreas", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="quality-satisfaction-heatmap", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("NPS Breakdown", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="quality-nps-chart", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Tendencias Calidad (12 meses)", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="quality-trends-chart", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("Matriz Performance: Tiempo vs Satisfacción", className="chart-title")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="quality-performance-matrix", style={"height": "300px"})
                    ])
                ], className="chart-card")
            ], width=6)
        ], className="mb-4"),
        
        # Métricas Operacionales (Grid de 6 mini-cards)
        html.H5("Métricas Operacionales Oficiales", className="section-subtitle mb-3"),
        dbc.Row([
            dbc.Col([
                create_quality_kpi_card(
                    "Disponibilidad Equipaje",
                    f"{quality_data['disponibilidad_equipaje']['availability']}%",
                    "disponibilidad",
                    quality_data['disponibilidad_equipaje']['trend'],
                    'up',
                    "mdi:baggage-claim"
                )
            ], width=2),
            dbc.Col([
                create_quality_kpi_card(
                    "Precisión Información",
                    f"{quality_data['precision_informacion']['score']}/5",
                    "pantallas",
                    quality_data['precision_informacion']['trend'],
                    'up',
                    "mdi:information"
                )
            ], width=2),
            dbc.Col([
                create_quality_kpi_card(
                    "Facilidad Ubicación",
                    f"{quality_data['facilidad_ubicacion']['score']}/5",
                    "instalaciones",
                    quality_data['facilidad_ubicacion']['trend'],
                    'up',
                    "mdi:map-marker"
                )
            ], width=2),
            dbc.Col([
                create_quality_kpi_card(
                    "Limpieza Baños",
                    f"{quality_data['limpieza_banos']['score']}/5",
                    "encuesta",
                    quality_data['limpieza_banos']['trend'],
                    'up',
                    "mdi:toilet"
                )
            ], width=2),
            dbc.Col([
                create_quality_kpi_card(
                    "Check-in Hora Pico",
                    f"{quality_data['tiempo_checkin_pico']['avg']} min",
                    "tiempo espera",
                    quality_data['tiempo_checkin_pico']['trend'],
                    'down',
                    "mdi:airplane-check"
                )
            ], width=2),
            dbc.Col([
                create_quality_kpi_card(
                    "Equipaje Hora Pico",
                    f"{quality_data['tiempo_equipaje_pico']['avg']} min",
                    "tiempo espera",
                    quality_data['tiempo_equipaje_pico']['trend'],
                    'stable',
                    "mdi:clock-fast"
                )
            ], width=2)
        ])
    ])

def render_productivity_tab():
    """
    Render productivity operational tab with Executive Dashboard
    """
    productivity_data = get_productivity_data()
    executive_metrics = get_executive_metrics()
    
    # Calculate global efficiency index
    efficiency_index = calculate_productivity_index(productivity_data)
    
    return html.Div([
        # Executive Header
        html.Div([
            html.Div([
                DashIconify(icon="mdi:factory", width=32, height=32, style={'marginRight': '15px', 'color': '#00d4ff'}),
                html.Div([
                    html.H3("Executive Dashboard - Productividad Operacional", 
                           style={'margin': 0, 'fontWeight': '600', 'color': '#ffffff'}),
                    html.P("AIFA Operations Command Center", 
                          style={'margin': 0, 'fontSize': '14px', 'color': '#8b92a9'})
                ])
            ], style={'display': 'flex', 'alignItems': 'center'}),
            
            html.Div([
                html.Div([
                    html.P("ÍNDICE GLOBAL DE EFICIENCIA", 
                          style={'margin': 0, 'fontSize': '12px', 'color': '#8b92a9', 'letterSpacing': '1px'}),
                    html.H2(f"{efficiency_index}%", 
                           style={'margin': 0, 'color': '#00ff88' if efficiency_index >= 85 else '#ffa726', 'fontWeight': '700'})
                ], style={'textAlign': 'right'})
            ])
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'marginBottom': '30px',
            'padding': '20px',
            'background': 'rgba(255, 255, 255, 0.05)',
            'borderRadius': '12px',
            'backdropFilter': 'blur(10px)'
        }),
        
        # Main KPIs Grid - Official AIFA Productivity KPIs
        dbc.Row([
            dbc.Col([
                create_productivity_kpi_enhanced(
                    title="Movimientos por Hora",
                    current=productivity_data['movements_per_hour']['current'],
                    benchmark=productivity_data['movements_per_hour']['benchmark'],
                    unit="mov/hr",
                    trend=productivity_data['movements_per_hour']['trend'],
                    icon="mdi:airplane-clock",
                    performance=productivity_data['movements_per_hour']['performance']
                )
            ], width=12, md=6, lg=4, xl=2.4, style={'marginBottom': '20px'}),
            
            dbc.Col([
                create_productivity_kpi_enhanced(
                    title="Tiempo de Rotación",
                    current=productivity_data['turnaround_time']['current'],
                    benchmark=productivity_data['turnaround_time']['benchmark'],
                    unit="min",
                    trend=productivity_data['turnaround_time']['trend'],
                    icon="mdi:timer-outline",
                    performance=productivity_data['turnaround_time']['performance']
                )
            ], width=12, md=6, lg=4, xl=2.4, style={'marginBottom': '20px'}),
            
            dbc.Col([
                create_productivity_kpi_enhanced(
                    title="Utilización de Puertas",
                    current=productivity_data['gate_utilization']['current'],
                    benchmark=productivity_data['gate_utilization']['benchmark'],
                    unit="%",
                    trend=productivity_data['gate_utilization']['trend'],
                    icon="mdi:gate",
                    performance=productivity_data['gate_utilization']['performance']
                )
            ], width=12, md=6, lg=4, xl=2.4, style={'marginBottom': '20px'}),
            
            dbc.Col([
                create_productivity_kpi_enhanced(
                    title="Productividad Personal",
                    current=productivity_data['staff_productivity']['current'],
                    benchmark=productivity_data['staff_productivity']['benchmark'],
                    unit="pax/emp",
                    trend=productivity_data['staff_productivity']['trend'],
                    icon="mdi:account-group",
                    performance=productivity_data['staff_productivity']['performance']
                )
            ], width=12, md=6, lg=4, xl=2.4, style={'marginBottom': '20px'}),
            
            dbc.Col([
                create_productivity_kpi_enhanced(
                    title="Costo por UTC",
                    current=productivity_data['cost_per_wlu']['current'],
                    benchmark=productivity_data['cost_per_wlu']['benchmark'],
                    unit="USD",
                    trend=productivity_data['cost_per_wlu']['trend'],
                    icon="mdi:currency-usd",
                    performance=productivity_data['cost_per_wlu']['performance']
                )
            ], width=12, md=6, lg=4, xl=2.4, style={'marginBottom': '20px'})
        ], justify="center"),
        
        # Analytics Section
        html.Div([
            html.H5("Analytics Operacionales", 
                   style={'marginBottom': '20px', 'color': '#ffffff', 'fontWeight': '500'})
        ], style={'marginTop': '30px', 'marginBottom': '20px'}),
        
        # Charts Grid
        dbc.Row([
            # Efficiency Matrix
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Matriz de Eficiencia", 
                               style={'marginBottom': '15px', 'color': '#8b92a9'}),
                        dcc.Graph(
                            id='productivity-efficiency-matrix',
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="glass-card", style={'height': '400px'})
            ], width=12, lg=6, style={'marginBottom': '20px'}),
            
            # Benchmark Comparison Radar
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Comparación Benchmark Internacional", 
                               style={'marginBottom': '15px', 'color': '#8b92a9'}),
                        dcc.Graph(
                            id='productivity-benchmark-radar',
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="glass-card", style={'height': '400px'})
            ], width=12, lg=6, style={'marginBottom': '20px'}),
            
            # Productivity Trends
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Análisis de Tendencias de Productividad", 
                               style={'marginBottom': '15px', 'color': '#8b92a9'}),
                        dcc.Graph(
                            id='productivity-trends',
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="glass-card", style={'height': '400px'})
            ], width=12, lg=8, style={'marginBottom': '20px'}),
            
            # Resource Allocation
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Análisis ROI de Recursos", 
                               style={'marginBottom': '15px', 'color': '#8b92a9'}),
                        dcc.Graph(
                            id='productivity-roi-scatter',
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="glass-card", style={'height': '400px'})
            ], width=12, lg=4, style={'marginBottom': '20px'}),
            
            # Capacity Utilization Gauges
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Métricas de Utilización de Capacidad", 
                               style={'marginBottom': '15px', 'color': '#8b92a9'}),
                        dcc.Graph(
                            id='productivity-capacity-gauges',
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="glass-card", style={'height': '350px'})
            ], width=12, lg=6, style={'marginBottom': '20px'}),
            
            # Cost Breakdown Waterfall
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Desglose de Costos Operacionales", 
                               style={'marginBottom': '15px', 'color': '#8b92a9'}),
                        dcc.Graph(
                            id='productivity-cost-waterfall',
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="glass-card", style={'height': '350px'})
            ], width=12, lg=6, style={'marginBottom': '20px'})
        ]),
        
        # Executive Metrics Summary
        html.Div([
            html.H5("Resumen Ejecutivo de Métricas", 
                   style={'marginBottom': '20px', 'color': '#ffffff', 'fontWeight': '500'})
        ], style={'marginTop': '30px', 'marginBottom': '20px'}),
        
        dbc.Row([
            dbc.Col([
                create_executive_metric(
                    title="Ingresos por Movimiento",
                    value=f"${executive_metrics['revenue_per_movement']:,.0f}",
                    change=executive_metrics['revenue_per_movement_change'],
                    unit="USD"
                )
            ], width=6, md=3),
            
            dbc.Col([
                create_executive_metric(
                    title="Utilización de Activos",
                    value=f"{executive_metrics['asset_utilization']:.1f}%",
                    change=executive_metrics['asset_utilization_change'],
                    unit="percent"
                )
            ], width=6, md=3),
            
            dbc.Col([
                create_executive_metric(
                    title="Eficiencia Laboral",
                    value=f"{executive_metrics['labor_efficiency']:.1f}%",
                    change=executive_metrics['labor_efficiency_change'],
                    unit="percent"
                )
            ], width=6, md=3),
            
            dbc.Col([
                create_executive_metric(
                    title="Optimización de Procesos",
                    value=f"{executive_metrics['process_optimization']:.1f}%",
                    change=executive_metrics['process_optimization_change'],
                    unit="percent"
                )
            ], width=6, md=3)
        ])
    ], className="tab-content")

# Productivity Chart Functions
def create_efficiency_matrix():
    """Create efficiency matrix heatmap"""
    departments = ['Operaciones Terrestres', 'Seguridad', 'Servicio al Cliente', 'Mantenimiento', 'Carga', 'Migración']
    metrics = ['Productividad', 'Calidad', 'Control de Costos', 'Gestión del Tiempo']
    
    # Datos más realistas y consistentes
    values = np.array([
        [88, 85, 82, 90],  # Operaciones Terrestres
        [76, 92, 78, 85],  # Seguridad  
        [82, 88, 75, 80],  # Servicio al Cliente
        [91, 83, 85, 87],  # Mantenimiento
        [78, 80, 88, 82],  # Carga
        [74, 85, 72, 78]   # Migración
    ])
    
    fig = go.Figure(data=go.Heatmap(
        z=values,
        x=metrics,
        y=departments,
        colorscale='RdYlGn',
        showscale=True,
        text=[[f"{val:.0f}%" for val in row] for row in values],
        texttemplate="%{text}",
        textfont={"size": 11, "color": "white", "family": "Inter"},
        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.0f}%<extra></extra>',
        colorbar=dict(
            title="Eficiencia (%)",
            titlefont=dict(color='white', size=12),
            tickfont=dict(color='white', size=10)
        )
    ))
    
    fig.update_layout(
        title=dict(
            text="Eficiencia Operacional por Departamento",
            font=dict(color='white', size=14, family='Inter'),
            x=0.5
        ),
        xaxis=dict(
            title="Métricas",
            titlefont=dict(color='white', size=12),
            tickfont=dict(color='white', size=10)
        ),
        yaxis=dict(
            title="Departamentos", 
            titlefont=dict(color='white', size=12),
            tickfont=dict(color='white', size=10)
        ),
        font=dict(color='white', family='Inter'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=120, r=60, t=60, b=60)
    )
    
    return fig

def create_benchmark_radar():
    """Create international benchmark radar chart"""
    categories = ['Productividad Personal', 'Eficiencia de Costos', 'Tiempo de Rotación', 
                 'Utilización de Puertas', 'Satisfacción del Cliente']
    
    aifa_values = [92, 85, 94, 81, 88]
    benchmark_values = [85, 80, 88, 75, 82]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=aifa_values + [aifa_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='AIFA',
        line=dict(color='#00d4ff', width=3),
        fillcolor='rgba(0, 212, 255, 0.3)',
        marker=dict(size=8, color='#00d4ff')
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=benchmark_values + [benchmark_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Benchmark Internacional',
        line=dict(color='#ffa726', width=3),
        fillcolor='rgba(255, 167, 38, 0.2)',
        marker=dict(size=8, color='#ffa726')
    ))
    
    fig.update_layout(
        title=dict(
            text="Comparación con Benchmark Internacional",
            font=dict(color='white', size=14, family='Inter'),
            x=0.5
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color='white',
                tickfont=dict(size=10),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            angularaxis=dict(
                color='white',
                tickfont=dict(size=10, family='Inter')
            )
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='white', size=11, family='Inter'),
            x=0.85,
            y=0.95
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=60, r=60, t=60, b=60)
    )
    
    return fig

def create_productivity_trends():
    """Create productivity trends time series"""
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    movements_per_hour = [15.2, 15.8, 16.1, 15.9, 16.4, 16.8, 17.1, 17.3, 17.0, 17.5, 17.8, 18.2]
    staff_productivity = [1185, 1205, 1240, 1228, 1265, 1290, 1315, 1325, 1308, 1340, 1355, 1380]
    cost_per_wlu = [12.8, 12.5, 12.3, 12.4, 12.1, 11.9, 11.8, 11.6, 11.7, 11.5, 11.3, 11.2]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=movements_per_hour,
        mode='lines+markers',
        name='Movimientos/Hora',
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=8, color='#00d4ff'),
        hovertemplate='<b>Movimientos/Hora</b><br>%{x}: %{y:.1f}<extra></extra>',
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=[x/100 for x in staff_productivity],
        mode='lines+markers',
        name='Productividad Personal (x100)',
        line=dict(color='#00ff88', width=3),
        marker=dict(size=8, color='#00ff88'),
        hovertemplate='<b>Productividad Personal</b><br>%{x}: %{customdata}<extra></extra>',
        customdata=staff_productivity,
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=cost_per_wlu,
        mode='lines+markers',
        name='Costo por UTC',
        line=dict(color='#ffa726', width=3),
        marker=dict(size=8, color='#ffa726'),
        hovertemplate='<b>Costo por UTC</b><br>%{x}: $%{y:.2f}<extra></extra>',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title=dict(
            text="Tendencias de Productividad - 12 Meses",
            font=dict(color='white', size=14, family='Inter'),
            x=0.5
        ),
        xaxis=dict(
            title="Mes",
            titlefont=dict(color='white', size=12),
            tickfont=dict(color='white', size=10),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title="Índice de Productividad",
            titlefont=dict(color='white', size=12),
            tickfont=dict(color='white', size=10),
            side='left',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis2=dict(
            title="Costo por UTC (USD)",
            titlefont=dict(color='white', size=12),
            tickfont=dict(color='white', size=10),
            overlaying='y',
            side='right'
        ),
        legend=dict(
            font=dict(color='white', size=11, family='Inter'),
            x=0.02,
            y=0.98
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=60, r=60, t=60, b=60)
    )
    
    return fig

def create_roi_scatter():
    """Create resource ROI scatter plot"""
    departments = ['Ops. Terrestres', 'Seguridad', 'Servicio Cliente', 'Mantenimiento', 'Carga', 'Migración', 'TI', 'Admin']
    investment = [850, 420, 320, 1200, 380, 180, 520, 240]
    roi = [185, 142, 138, 168, 155, 134, 172, 125]
    
    fig = go.Figure(data=go.Scatter(
        x=investment,
        y=roi,
        mode='markers+text',
        text=departments,
        textposition='top center',
        marker=dict(
            size=20,
            color=roi,
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(
                title="ROI (%)",
                titlefont=dict(color='white', size=12),
                tickfont=dict(color='white', size=10)
            ),
            line=dict(width=2, color='white')
        ),
        textfont=dict(color='white', size=11, family='Inter'),
        hovertemplate='<b>%{text}</b><br>Inversión: $%{x}K USD<br>ROI: %{y}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="Inversión vs ROI por Departamento",
            font=dict(color='white', size=14, family='Inter'),
            x=0.5
        ),
        xaxis=dict(
            title="Inversión (K USD)",
            titlefont=dict(color='white', size=12),
            tickfont=dict(color='white', size=10),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title="ROI (%)",
            titlefont=dict(color='white', size=12),
            tickfont=dict(color='white', size=10),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=60, r=60, t=60, b=60)
    )
    
    return fig

def create_capacity_gauges():
    """Create capacity utilization gauge charts"""
    resources = ['Puertas', 'Check-in', 'Seguridad', 'Equipajes']
    utilizations = [78, 85, 72, 80]
    colors = ['#00d4ff', '#00ff88', '#ffa726', '#ff6b6b']
    
    fig = go.Figure()
    
    for i, (resource, util, color) in enumerate(zip(resources, utilizations, colors)):
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=util,
            domain={'row': i//2, 'column': i%2},
            title={
                'text': f"<b>{resource}</b>",
                'font': {'color': 'white', 'size': 14, 'family': 'Inter'}
            },
            gauge={
                'axis': {
                    'range': [None, 100],
                    'tickcolor': 'white',
                    'tickfont': {'size': 10, 'color': 'white'}
                },
                'bar': {'color': color, 'thickness': 0.8},
                'bgcolor': 'rgba(255,255,255,0.1)',
                'borderwidth': 2,
                'bordercolor': 'rgba(255,255,255,0.3)',
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(255, 71, 87, 0.2)'},
                    {'range': [50, 80], 'color': 'rgba(255, 167, 38, 0.2)'},
                    {'range': [80, 100], 'color': 'rgba(0, 255, 136, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': "#ff4757", 'width': 3},
                    'thickness': 0.75,
                    'value': 90
                }
            },
            number={
                'font': {'color': 'white', 'size': 18, 'family': 'Inter'},
                'suffix': '%'
            }
        ))
    
    fig.update_layout(
        title=dict(
            text="Utilización de Recursos Críticos",
            font=dict(color='white', size=14, family='Inter'),
            x=0.5,
            y=0.95
        ),
        grid={'rows': 2, 'columns': 2, 'pattern': "independent"},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_cost_waterfall():
    """Create operational cost breakdown waterfall chart"""
    categories = ['Personal', 'Infraestructura', 'Tecnología', 'Energía', 'Mantenimiento', 'Otros']
    values = [4500, 2800, 1200, 800, 1100, 600]
    
    fig = go.Figure(go.Waterfall(
        name="Desglose de Costos",
        orientation="v",
        measure=["relative"]*len(categories),
        x=categories,
        textposition="auto",
        text=[f"${v}K" for v in values],
        y=values,
        textfont=dict(color='white', size=12, family='Inter'),
        connector={"line": {"color": "rgba(255,255,255,0.3)", "width": 2}},
        increasing={"marker": {"color": "#00d4ff", "line": {"color": "white", "width": 2}}},
        decreasing={"marker": {"color": "#ff4757", "line": {"color": "white", "width": 2}}},
        totals={"marker": {"color": "#00ff88", "line": {"color": "white", "width": 2}}},
        hovertemplate='<b>%{x}</b><br>Costo: $%{y}K USD<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="Desglose de Costos Operacionales Mensuales",
            font=dict(color='white', size=14, family='Inter'),
            x=0.5
        ),
        xaxis=dict(
            titlefont=dict(color='white', size=12),
            tickfont=dict(color='white', size=10),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title="Costo (K USD)",
            titlefont=dict(color='white', size=12),
            tickfont=dict(color='white', size=10),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=60, r=20, t=60, b=60)
    )
    
    return fig

def render_metodologia_tab():
    """Render del tab de Metodología con sistema de autenticación"""
    
    # Modal de autenticación
    auth_modal = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle([
            DashIconify(icon="mdi:shield-check", width=24, height=24, style={'marginRight': '10px', 'color': '#00d4ff'}),
            "Acceso a Documentación Técnica"
        ])),
        dbc.ModalBody([
            html.Div([
                html.Div([
                    html.Div([
                        DashIconify(icon="mdi:security", width=48, height=48, style={'color': '#f59e0b', 'marginBottom': '10px'}),
                        html.H5("Área Restringida - Documentación Técnica AIFA", 
                               style={'color': '#ffffff', 'fontWeight': '700', 'marginBottom': '15px'}),
                        html.P("Esta sección contiene información confidencial clasificada. Solo personal autorizado.", 
                               style={'color': '#8b92a9', 'fontSize': '0.95rem', 'marginBottom': '20px'})
                    ], style={'textAlign': 'center', 'marginBottom': '25px'}),
                    
                    html.Div([
                        html.P("🔐 Credenciales válidas requeridas", 
                               style={'color': '#00d4ff', 'fontSize': '0.9rem', 'textAlign': 'center', 'marginBottom': '20px'})
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Usuario:", style={'color': '#ffffff', 'fontWeight': 'bold'}),
                        dbc.Input(
                            id="auth-username",
                            type="text",
                            placeholder="ej: director-aifa, metodologia-senior",
                            style={
                                'backgroundColor': 'rgba(26, 31, 58, 0.9)',
                                'border': '1px solid rgba(0, 212, 255, 0.3)',
                                'color': '#ffffff'
                            }
                        )
                    ], width=12)
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Contraseña:", style={'color': '#ffffff', 'fontWeight': 'bold'}),
                        dbc.Input(
                            id="auth-password",
                            type="password",
                            placeholder="Contraseña segura (8+ caracteres)",
                            style={
                                'backgroundColor': 'rgba(26, 31, 58, 0.9)',
                                'border': '1px solid rgba(0, 212, 255, 0.3)',
                                'color': '#ffffff'
                            }
                        )
                    ], width=12)
                ], className="mb-3"),
                html.Div(id="auth-message", style={'color': '#ff4757', 'marginTop': '10px'})
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id="auth-cancel", className="me-2", 
                      style={'backgroundColor': '#374151', 'border': 'none'}),
            dbc.Button("Ingresar", id="auth-submit", 
                      style={'backgroundColor': '#00d4ff', 'border': 'none'})
        ])
    ], id="auth-modal", size="md", is_open=False, backdrop="static")

    return html.Div([
        auth_modal,
        
        # Header de la sección
        html.Div([
            html.Div([
                DashIconify(icon="mdi:book-open-variant", width=32, height=32, 
                           style={'color': '#00d4ff', 'marginRight': '15px'}),
                html.H3("Metodología Técnica AIFA", 
                       style={'color': '#ffffff', 'margin': '0', 'fontWeight': '600'})
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            html.P("Documentación técnica, arquitectura de sistemas y metodologías operacionales", 
                   style={'color': '#8b92a9', 'margin': '0', 'fontSize': '1.1rem'})
        ], style={'marginBottom': '30px'}),
        
        # Botón de acceso principal
        html.Div([
            dbc.Button([
                DashIconify(icon="mdi:shield-lock", width=24, height=24, style={'marginRight': '10px'}),
                "Acceder a Documentación Técnica"
            ], id="open-auth-modal", size="lg", 
               style={
                   'backgroundColor': '#00d4ff', 
                   'border': 'none', 
                   'padding': '15px 30px',
                   'fontSize': '1.1rem',
                   'fontWeight': '600',
                   'boxShadow': '0 4px 15px rgba(0, 212, 255, 0.3)'
               })
        ], style={'textAlign': 'center', 'marginBottom': '40px'}),
        
        # Contenido protegido (inicialmente oculto)
        html.Div(id="protected-content", children=[], style={'display': 'none'}),
        
        # Preview público de metodología
        html.Div([
            html.H4("Vista Previa de Metodología", 
                   style={'color': '#ffffff', 'marginBottom': '20px', 'textAlign': 'center'}),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                DashIconify(icon="mdi:chart-line", width=40, height=40, 
                                           style={'color': '#00d4ff'}),
                                html.H5("Dashboard Overview", 
                                       style={'color': '#ffffff', 'marginTop': '15px'}),
                                html.P("Vista general de 53 KPIs distribuidos en 7 módulos operacionales", 
                                       style={'color': '#8b92a9', 'fontSize': '0.9rem'})
                            ], style={'textAlign': 'center'})
                        ])
                    ], className="chart-card", style={'height': '200px', 'display': 'flex', 'alignItems': 'center'})
                ], width=4),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                DashIconify(icon="mdi:sitemap", width=40, height=40, 
                                           style={'color': '#f59e0b'}),
                                html.H5("Arquitectura de Sistemas", 
                                       style={'color': '#ffffff', 'marginTop': '15px'}),
                                html.P("Diagramas de integración entre AODB, SMS, ERP y sistemas complementarios", 
                                       style={'color': '#8b92a9', 'fontSize': '0.9rem'})
                            ], style={'textAlign': 'center'})
                        ])
                    ], className="chart-card", style={'height': '200px', 'display': 'flex', 'alignItems': 'center'})
                ], width=4),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                DashIconify(icon="mdi:book-variant", width=40, height=40, 
                                           style={'color': '#8b5cf6'}),
                                html.H5("Glosario Técnico", 
                                       style={'color': '#ffffff', 'marginTop': '15px'}),
                                html.P("Definiciones completas de 12+ términos técnicos del sector aeroportuario", 
                                       style={'color': '#8b92a9', 'fontSize': '0.9rem'})
                            ], style={'textAlign': 'center'})
                        ])
                    ], className="chart-card", style={'height': '200px', 'display': 'flex', 'alignItems': 'center'})
                ], width=4)
            ])
        ])
    ])

def render_protected_methodology_content():
    """Contenido completo de metodología (después de autenticación)"""
    dashboard_mapping = get_dashboard_mapping()
    technical_glossary = get_technical_glossary()
    system_architecture = get_system_architecture()
    kpi_formulas = get_kpi_formulas()
    
    return html.Div([
        # 1. Dashboard Overview - Mapeo completo de KPIs
        html.Div([
            html.H4([
                DashIconify(icon="mdi:view-dashboard", width=28, height=28, 
                           style={'marginRight': '10px', 'color': '#00d4ff'}),
                "Dashboard Overview - Mapeo de KPIs"
            ], style={'color': '#ffffff', 'marginBottom': '20px'}),
            
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H6("Distribución de KPIs por Módulo", 
                               style={'color': '#ffffff', 'marginBottom': '15px'}),
                        dbc.Table([
                            html.Thead([
                                html.Tr([
                                    html.Th("Módulo", style={'color': '#00d4ff', 'borderColor': 'rgba(0, 212, 255, 0.3)'}),
                                    html.Th("KPIs", style={'color': '#00d4ff', 'borderColor': 'rgba(0, 212, 255, 0.3)'}),
                                    html.Th("Estado", style={'color': '#00d4ff', 'borderColor': 'rgba(0, 212, 255, 0.3)'}),
                                    html.Th("Sistemas", style={'color': '#00d4ff', 'borderColor': 'rgba(0, 212, 255, 0.3)'}),
                                    html.Th("Complejidad", style={'color': '#00d4ff', 'borderColor': 'rgba(0, 212, 255, 0.3)'})
                                ])
                            ]),
                            html.Tbody([
                                html.Tr([
                                    html.Td(modulo.title(), style={'color': '#ffffff', 'borderColor': 'rgba(255,255,255,0.1)'}),
                                    html.Td(str(data['kpis']), style={'color': '#ffffff', 'borderColor': 'rgba(255,255,255,0.1)'}),
                                    html.Td([
                                        dbc.Badge("✓ Implementado" if data['implementado'] else "Pendiente", 
                                                 color="success" if data['implementado'] else "warning",
                                                 className="me-1")
                                    ], style={'borderColor': 'rgba(255,255,255,0.1)'}),
                                    html.Td(", ".join(data['sistemas']), style={'color': '#8b92a9', 'fontSize': '0.9rem', 'borderColor': 'rgba(255,255,255,0.1)'}),
                                    html.Td([
                                        dbc.Badge(data['complejidad'], 
                                                 color="danger" if data['complejidad'] == "Alta" else 
                                                       "warning" if data['complejidad'] == "Media" else "info")
                                    ], style={'borderColor': 'rgba(255,255,255,0.1)'})
                                ]) for modulo, data in dashboard_mapping.items()
                            ])
                        ], bordered=True, hover=True, responsive=True, dark=True)
                    ])
                ])
            ], className="chart-card", style={'marginBottom': '30px'})
        ]),
        
        # 2. System Architecture
        html.Div([
            html.H4([
                DashIconify(icon="mdi:sitemap", width=28, height=28, 
                           style={'marginRight': '10px', 'color': '#f59e0b'}),
                "Arquitectura de Sistemas"
            ], style={'color': '#ffffff', 'marginBottom': '20px'}),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Sistemas Core", style={'color': '#ffffff', 'marginBottom': '15px'}),
                            html.Div([
                                html.Div([
                                    html.H6(sistema, style={'color': '#00d4ff', 'fontSize': '1rem'}),
                                    html.P(data['descripcion'], style={'color': '#ffffff', 'fontSize': '0.9rem', 'marginBottom': '5px'}),
                                    html.P(f"Criticidad: {data['criticidad']}", style={'color': '#f59e0b', 'fontSize': '0.8rem', 'marginBottom': '10px'}),
                                    html.P(f"Conexiones: {', '.join(data['conexiones'])}", style={'color': '#8b92a9', 'fontSize': '0.8rem'})
                                ], style={'marginBottom': '20px'}) for sistema, data in system_architecture['core_systems'].items()
                            ])
                        ])
                    ], className="chart-card")
                ], width=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("APIs de Integración", style={'color': '#ffffff', 'marginBottom': '15px'}),
                            html.Div([
                                html.Div([
                                    html.H6(api['nombre'], style={'color': '#00ff88', 'fontSize': '1rem'}),
                                    html.P(f"Protocolo: {api['protocolo']} | Formato: {api['formato']}", 
                                           style={'color': '#ffffff', 'fontSize': '0.9rem', 'marginBottom': '5px'}),
                                    html.P(f"Tiempo Real: {'Sí' if api['tiempo_real'] else 'No'}", 
                                           style={'color': '#f59e0b' if api['tiempo_real'] else '#8b92a9', 'fontSize': '0.8rem'})
                                ], style={'marginBottom': '15px'}) for api in system_architecture['integration_apis']
                            ])
                        ])
                    ], className="chart-card")
                ], width=6)
            ], style={'marginBottom': '30px'})
        ]),
        
        # 3. KPI Documentation
        html.Div([
            html.H4([
                DashIconify(icon="mdi:calculator", width=28, height=28, 
                           style={'marginRight': '10px', 'color': '#8b5cf6'}),
                "Documentación de KPIs"
            ], style={'color': '#ffffff', 'marginBottom': '20px'}),
            
            dbc.Accordion([
                dbc.AccordionItem([
                    html.Div([
                        html.H6("KPIs de Seguridad", style={'color': '#ffffff', 'marginBottom': '15px'}),
                        html.Div([
                            html.Div([
                                html.H6(kpi.replace('_', ' ').title(), style={'color': '#00d4ff'}),
                                html.P(f"Fórmula: {data['formula']}", style={'color': '#ffffff', 'fontFamily': 'monospace', 'backgroundColor': 'rgba(0,0,0,0.3)', 'padding': '8px', 'borderRadius': '4px'}),
                                html.P(f"Unidad: {data['unidad']}", style={'color': '#f59e0b'}),
                                html.P(f"Fuente: {data['fuente']}", style={'color': '#8b92a9'}),
                                html.P(f"Meta AIFA: {data['meta_aifa']}", style={'color': '#00ff88'})
                            ], style={'marginBottom': '20px'}) for kpi, data in kpi_formulas['seguridad'].items()
                        ])
                    ])
                ], title="Fórmulas de Seguridad"),
                
                dbc.AccordionItem([
                    html.Div([
                        html.H6("KPIs de Productividad", style={'color': '#ffffff', 'marginBottom': '15px'}),
                        html.Div([
                            html.Div([
                                html.H6(kpi.replace('_', ' ').title(), style={'color': '#00d4ff'}),
                                html.P(f"Fórmula: {data['formula']}", style={'color': '#ffffff', 'fontFamily': 'monospace', 'backgroundColor': 'rgba(0,0,0,0.3)', 'padding': '8px', 'borderRadius': '4px'}),
                                html.P(f"Unidad: {data['unidad']}", style={'color': '#f59e0b'}),
                                html.P(f"Fuente: {data['fuente']}", style={'color': '#8b92a9'}),
                                html.P(f"Meta AIFA: {data['meta_aifa']}", style={'color': '#00ff88'})
                            ], style={'marginBottom': '20px'}) for kpi, data in kpi_formulas['productividad'].items()
                        ])
                    ])
                ], title="Fórmulas de Productividad"),
                
                dbc.AccordionItem([
                    html.Div([
                        html.H6("KPIs de Calidad", style={'color': '#ffffff', 'marginBottom': '15px'}),
                        html.Div([
                            html.Div([
                                html.H6(kpi.replace('_', ' ').title(), style={'color': '#00d4ff'}),
                                html.P(f"Fórmula: {data['formula']}", style={'color': '#ffffff', 'fontFamily': 'monospace', 'backgroundColor': 'rgba(0,0,0,0.3)', 'padding': '8px', 'borderRadius': '4px'}),
                                html.P(f"Unidad: {data['unidad']}", style={'color': '#f59e0b'}),
                                html.P(f"Fuente: {data['fuente']}", style={'color': '#8b92a9'}),
                                html.P(f"Meta AIFA: {data['meta_aifa']}", style={'color': '#00ff88'})
                            ], style={'marginBottom': '20px'}) for kpi, data in kpi_formulas['calidad'].items()
                        ])
                    ])
                ], title="Fórmulas de Calidad")
            ], start_collapsed=True, style={'marginBottom': '30px'})
        ]),
        
        # 4. Technical Glossary
        html.Div([
            html.H4([
                DashIconify(icon="mdi:book-variant", width=28, height=28, 
                           style={'marginRight': '10px', 'color': '#00ff88'}),
                "Glosario Técnico"
            ], style={'color': '#ffffff', 'marginBottom': '20px'}),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.H5(f"{termino} ({data['nombre']})", style={'color': '#00d4ff', 'marginBottom': '10px'}),
                                html.P(data['definicion'], style={'color': '#ffffff', 'marginBottom': '15px'}),
                                html.H6("Funciones Principales:", style={'color': '#f59e0b', 'fontSize': '0.9rem', 'marginBottom': '8px'}),
                                html.Ul([
                                    html.Li(funcion, style={'color': '#8b92a9', 'fontSize': '0.8rem'}) 
                                    for funcion in data['funciones']
                                ], style={'marginBottom': '10px'}),
                                dbc.Badge(data['criticidad'], 
                                         color="danger" if "Crítica" in data['criticidad'] else 
                                               "warning" if "Alta" in data['criticidad'] else "info",
                                         style={'fontSize': '0.75rem'})
                            ])
                        ])
                    ], className="chart-card", style={'marginBottom': '20px'})
                ], width=6) for i, (termino, data) in enumerate(list(technical_glossary.items())[:8])
            ] + [
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.H5(f"{termino} ({data['nombre']})", style={'color': '#00d4ff', 'marginBottom': '10px'}),
                                html.P(data['definicion'], style={'color': '#ffffff', 'marginBottom': '15px'}),
                                html.H6("Funciones Principales:", style={'color': '#f59e0b', 'fontSize': '0.9rem', 'marginBottom': '8px'}),
                                html.Ul([
                                    html.Li(funcion, style={'color': '#8b92a9', 'fontSize': '0.8rem'}) 
                                    for funcion in data['funciones']
                                ], style={'marginBottom': '10px'}),
                                dbc.Badge(data['criticidad'], 
                                         color="danger" if "Crítica" in data['criticidad'] else 
                                               "warning" if "Alta" in data['criticidad'] else "info",
                                         style={'fontSize': '0.75rem'})
                            ])
                        ])
                    ], className="chart-card", style={'marginBottom': '20px'})
                ], width=6) for i, (termino, data) in enumerate(list(technical_glossary.items())[8:])
            ])
        ])
    ])

# Callbacks for charts
@callback(Output('participation-trend-chart', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_participation_trend(n):
    data = get_historical_data()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['months'],
        y=data['passengers'],
        mode='lines+markers',
        name='Pasajeros',
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=8, color='#00d4ff')
    ))
    
    fig.add_trace(go.Scatter(
        x=data['months'],
        y=data['operations'],
        mode='lines+markers',
        name='Operaciones',
        line=dict(color='#f59e0b', width=3),
        marker=dict(size=8, color='#f59e0b')
    ))
    
    fig.add_trace(go.Scatter(
        x=data['months'],
        y=data['cargo'],
        mode='lines+markers',
        name='Carga',
        line=dict(color='#00ff88', width=3),
        marker=dict(size=8, color='#00ff88')
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Mes'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Participación (%)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

@callback(Output('progress-gauge', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_progress_gauge(n):
    current = 12.8
    target = 15.0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Meta 15%", 'font': {'color': 'white'}},
        delta={'reference': target},
        gauge={
            'axis': {'range': [None, 20]},
            'bar': {'color': "#00d4ff"},
            'steps': [
                {'range': [0, 10], 'color': "rgba(255,71,87,0.3)"},
                {'range': [10, 15], 'color': "rgba(245,158,11,0.3)"},
                {'range': [15, 20], 'color': "rgba(0,255,136,0.3)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target
            }
        }
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

@callback(Output('airport-comparison-chart', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_airport_comparison(n):
    data = get_airport_comparison()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[x['name'] for x in data],
        y=[x['passengers'] for x in data],
        marker_color='#00d4ff',
        text=[f"{x['passengers']}%" for x in data],
        textposition='auto',
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Aeropuerto'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Participación (%)'),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

# Bloomberg Terminal Layout Helper
def get_bloomberg_layout():
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(10, 14, 39, 0.9)',
        'font': {'color': 'white', 'family': 'Inter'},
        'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40},
        'showlegend': True,
        'legend': {
            'font': {'color': 'white'},
            'bgcolor': 'rgba(26, 31, 58, 0.8)'
        },
        'xaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.1)'},
        'yaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.1)'}
    }

# Financial Charts Callbacks
@callback(Output('revenue-donut', 'figure'), Input('tabs', 'active_tab'))
def update_revenue_donut(active_tab):
    if active_tab != "financial":
        return {}
    
    return {
        'data': [go.Pie(
            labels=['Aeronáuticos', 'No-Aeronáuticos', 'Comerciales', 'Estacionamiento'],
            values=[178, 85, 19, 8],
            hole=0.6,
            marker_colors=['#00d4ff', '#00fff0', '#8b5cf6', '#ff6b35'],
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>$%{value}M MXN<br>%{percent}<extra></extra>'
        )],
        'layout': get_bloomberg_layout()
    }

@callback(Output('cost-waterfall', 'figure'), Input('tabs', 'active_tab'))
def update_cost_waterfall(active_tab):
    if active_tab != "financial":
        return {}
    
    return {
        'data': [go.Waterfall(
            name="Estructura de Costos",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Personal", "Mantenimiento", "Servicios", "Otros", "Total"],
            y=[78, 45, 32, 18, 173],
            text=['$78M', '$45M', '$32M', '$18M', '$173M'],
            textposition='outside',
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#ff4757"}},
            totals={"marker": {"color": "#00d4ff"}}
        )],
        'layout': get_bloomberg_layout()
    }

@callback(Output('profitability-trends', 'figure'), Input('tabs', 'active_tab'))
def update_profitability_trends(active_tab):
    if active_tab != "financial":
        return {}
    
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    return {
        'data': [
            go.Scatter(
                x=months,
                y=[15.2, 16.8, 17.5, 18.1, 18.7, 19.2, 18.9, 18.5, 19.1, 19.6, 19.8, 20.2],
                name='AIFA',
                mode='lines+markers',
                line=dict(color='#00d4ff', width=3),
                marker=dict(size=6, color='#00d4ff')
            ),
            go.Scatter(
                x=months,
                y=[14.5] * 12,
                name='Promedio Industria',
                mode='lines',
                line=dict(color='#ff6b35', width=2, dash='dash')
            ),
            go.Scatter(
                x=months,
                y=[16.0] * 12,
                name='Objetivo',
                mode='lines',
                line=dict(color='#00ff88', width=2, dash='dot')
            )
        ],
        'layout': get_bloomberg_layout()
    }

@callback(Output('cashflow-analysis', 'figure'), Input('tabs', 'active_tab'))
def update_cashflow_analysis(active_tab):
    if active_tab != "financial":
        return {}
    
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    return {
        'data': [
            go.Scatter(
                x=months,
                y=[85, 92, 98, 105, 112, 118, 125, 132, 127, 135, 142, 148],
                name='Flujo Operativo',
                mode='lines',
                fill='tonexty',
                line=dict(color='#00ff88'),
                fillcolor='rgba(0, 255, 136, 0.2)'
            ),
            go.Scatter(
                x=months,
                y=[78, 84, 89, 95, 101, 106, 112, 118, 115, 121, 127, 132],
                name='Flujo Libre',
                mode='lines',
                fill='tozeroy',
                line=dict(color='#00d4ff'),
                fillcolor='rgba(0, 212, 255, 0.2)'
            )
        ],
        'layout': get_bloomberg_layout()
    }

# Operations Center Layout Helper
def get_capacity_layout():
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(10, 14, 39, 0.9)',
        'font': {'color': 'white', 'family': 'Inter'},
        'margin': {'l': 60, 'r': 20, 't': 20, 'b': 60},
        'xaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.1)'},
        'yaxis': {'color': '#a0aec0', 'gridcolor': 'rgba(0, 212, 255, 0.1)'},
        'legend': {'font': {'color': 'white'}, 'bgcolor': 'rgba(26, 31, 58, 0.8)'}
    }

# Operations Center Charts Callbacks
@callback(Output('capacity-heatmap', 'figure'), Input('tabs', 'active_tab'))
def update_capacity_heatmap(active_tab):
    if active_tab != "capacity":
        return {}
    
    zones = ['Check-in', 'Seguridad', 'Inmigración', 'Espera', 'Gates', 'Equipajes']
    hours = ['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
    
    density_matrix = [
        [20, 45, 60, 75, 85, 90, 80, 65, 40],  # Check-in
        [15, 40, 55, 70, 80, 85, 75, 60, 35],  # Seguridad
        [10, 35, 50, 65, 75, 80, 70, 55, 30],  # Inmigración
        [25, 50, 65, 80, 90, 95, 85, 70, 45],  # Espera
        [30, 55, 70, 85, 95, 100, 90, 75, 50], # Gates
        [18, 42, 58, 72, 82, 88, 78, 62, 38]   # Equipajes
    ]
    
    return {
        'data': [go.Heatmap(
            z=density_matrix, x=hours, y=zones,
            colorscale=[
                [0, '#0a0e27'], [0.2, '#1a1f3a'], [0.4, '#00d4ff'],
                [0.6, '#ffb627'], [0.8, '#ff6b35'], [1, '#ff4757']
            ],
            hovertemplate='<b>%{y}</b><br>Hora: %{x}<br>Densidad: %{z}%<extra></extra>'
        )],
        'layout': get_capacity_layout()
    }

@callback(Output('utilization-trends', 'figure'), Input('tabs', 'active_tab'))
def update_utilization_trends(active_tab):
    if active_tab != "capacity":
        return {}
    
    hours = list(range(6, 23))
    
    return {
        'data': [
            go.Scatter(x=hours, y=[20, 35, 55, 70, 80, 85, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40],
                      name='Check-in', line=dict(color='#00ff88', width=3)),
            go.Scatter(x=hours, y=[15, 30, 50, 65, 75, 80, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35],
                      name='Seguridad', line=dict(color='#ffb627', width=3)),
            go.Scatter(x=hours, y=[25, 40, 60, 75, 85, 90, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45],
                      name='Gates', line=dict(color='#8b5cf6', width=3)),
            go.Scatter(x=hours, y=[18, 33, 48, 63, 73, 78, 83, 78, 73, 68, 63, 58, 53, 48, 43, 38, 33],
                      name='Equipajes', line=dict(color='#ff6b35', width=3))
        ],
        'layout': get_capacity_layout()
    }

@callback(Output('capacity-demand', 'figure'), Input('tabs', 'active_tab'))
def update_capacity_demand(active_tab):
    if active_tab != "capacity":
        return {}
    
    hours = list(range(6, 23))
    
    return {
        'data': [
            go.Scatter(
                x=hours,
                y=[100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                name='Capacidad Máxima',
                mode='lines',
                line=dict(color='#ff4757', width=2, dash='dash'),
                fill=None
            ),
            go.Scatter(
                x=hours,
                y=[20, 35, 55, 70, 80, 85, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40],
                name='Demanda Actual',
                mode='lines',
                line=dict(color='#00d4ff', width=3),
                fill='tonexty',
                fillcolor='rgba(0, 212, 255, 0.2)'
            )
        ],
        'layout': get_capacity_layout()
    }

@callback(Output('general-gauge', 'figure'), Input('tabs', 'active_tab'))
def update_general_gauge(active_tab):
    if active_tab != "capacity":
        return {}
    
    return {
        'data': [go.Indicator(
            mode="gauge+number+delta",
            value=78,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Utilización Terminal (%)"},
            delta={'reference': 75},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#00d4ff"},
                'steps': [
                    {'range': [0, 50], 'color': "rgba(0, 255, 136, 0.3)"},
                    {'range': [50, 80], 'color': "rgba(255, 182, 39, 0.3)"},
                    {'range': [80, 100], 'color': "rgba(255, 71, 87, 0.3)"}
                ],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 90}
            }
        )],
        'layout': get_capacity_layout()
    }

# Security Operations Charts Callbacks
@callback(Output('security-trends-chart', 'figure'), Input('tabs', 'active_tab'))
def update_security_trends(active_tab):
    if active_tab != "security":
        return {}
    
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    return {
        'data': [
            go.Scatter(x=months, y=[0.15, 0.12, 0.10, 0.08, 0.11, 0.09, 0.12, 0.10, 0.13, 0.11, 0.12, 0.12],
                      name='Incidentes Pista', line=dict(color='#ff4757', width=3),
                      hovertemplate='<b>Incidentes Pista</b><br>%{x}: %{y}/1000 ops<extra></extra>'),
            go.Scatter(x=months, y=[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                      name='Accidentes Mortales', line=dict(color='#00ff88', width=3),
                      hovertemplate='<b>Accidentes Mortales</b><br>%{x}: %{y}/1000 ops<extra></extra>'),
            go.Scatter(x=months, y=[0.90, 0.85, 0.88, 0.82, 0.87, 0.91, 0.86, 0.89, 0.85, 0.83, 0.85, 0.85],
                      name='Choques Aves', line=dict(color='#f59e0b', width=3),
                      hovertemplate='<b>Choques Aves</b><br>%{x}: %{y}/1000 ops<extra></extra>'),
            go.Scatter(x=months, y=[0.08, 0.06, 0.04, 0.03, 0.05, 0.04, 0.06, 0.05, 0.07, 0.05, 0.05, 0.05],
                      name='Incursiones Pista', line=dict(color='#00d4ff', width=3),
                      hovertemplate='<b>Incursiones Pista</b><br>%{x}: %{y}/1000 ops<extra></extra>')
        ],
        'layout': get_security_chart_layout()
    }

@callback(Output('security-standards-chart', 'figure'), Input('tabs', 'active_tab'))
def update_security_standards(active_tab):
    if active_tab != "security":
        return {}
    
    kpis = ['Incidentes\nPista', 'Accidentes\nMortales', 'Choques\nAves', 'Incursiones\nPista', 'Personal\nSeguridad']
    aifa_values = [0.12, 0.00, 0.85, 0.05, 45]
    oaci_standards = [0.15, 0.00, 1.20, 0.10, 40]
    
    return {
        'data': [
            go.Bar(x=kpis, y=aifa_values, name='AIFA Actual',
                   marker=dict(color='#00d4ff', opacity=0.8),
                   hovertemplate='<b>AIFA</b><br>%{x}: %{y}<extra></extra>'),
            go.Bar(x=kpis, y=oaci_standards, name='Estándar OACI',
                   marker=dict(color='#f59e0b', opacity=0.6),
                   hovertemplate='<b>OACI</b><br>%{x}: %{y}<extra></extra>')
        ],
        'layout': get_security_chart_layout()
    }

@callback(Output('security-risk-matrix', 'figure'), Input('tabs', 'active_tab'))
def update_security_risk_matrix(active_tab):
    if active_tab != "security":
        return {}
    
    zones = ['Terminal', 'Pista 12L', 'Pista 12R', 'Torre Control', 'Área Carga', 'Estacionamiento']
    risk_factors = ['FOD', 'Fauna', 'Clima', 'Humano', 'Equipo']
    
    risk_matrix = [
        [2, 1, 3, 2, 1, 2],  # FOD
        [1, 3, 3, 1, 2, 1],  # Fauna
        [2, 3, 3, 2, 2, 1],  # Clima
        [3, 2, 2, 2, 3, 2],  # Humano
        [2, 2, 2, 3, 2, 1]   # Equipo
    ]
    
    return {
        'data': [go.Heatmap(
            z=risk_matrix, x=zones, y=risk_factors,
            colorscale=[
                [0, '#00ff88'], [0.33, '#f59e0b'], [0.66, '#ff6b35'], [1, '#ff4757']
            ],
            hovertemplate='<b>%{y} - %{x}</b><br>Nivel Riesgo: %{z}<extra></extra>',
            showscale=True,
            colorbar=dict(
                title="Nivel Riesgo",
                titleside="right",
                tickmode="array",
                tickvals=[1, 2, 3],
                ticktext=["Bajo", "Medio", "Alto"],
                len=0.6
            )
        )],
        'layout': get_security_chart_layout()
    }

@callback(Output('security-incidents-distribution', 'figure'), Input('tabs', 'active_tab'))
def update_security_incidents_distribution(active_tab):
    if active_tab != "security":
        return {}
    
    incident_types = ['FOD', 'Fauna', 'Incursiones', 'Mantenimiento', 'Iluminación', 'Otros']
    values = [25, 20, 15, 18, 12, 10]
    colors = ['#ff4757', '#f59e0b', '#ff6b35', '#00d4ff', '#8b5cf6', '#00ff88']
    
    return {
        'data': [go.Pie(
            labels=incident_types,
            values=values,
            hole=0.4,
            marker=dict(colors=colors, line=dict(color='#0a0e27', width=2)),
            hovertemplate='<b>%{label}</b><br>Incidentes: %{value}<br>Porcentaje: %{percent}<extra></extra>',
            textinfo='label+percent',
            textposition='outside'
        )],
        'layout': {
            **get_security_chart_layout(),
            'showlegend': False,
            'margin': dict(l=20, r=20, t=20, b=20)
        }
    }

# Quality Service Callbacks - Customer Journey Analytics
@callback(Output('quality-satisfaction-heatmap', 'figure'), Input('tabs', 'active_tab'))
def update_quality_satisfaction_heatmap(active_tab):
    if active_tab != "quality":
        return {}
    
    areas = ['Terminal', 'Check-in', 'Seguridad', 'Comercial', 'Embarque', 'Equipaje']
    timeperiods = ['Hora Pico', 'Normal', 'Nocturno']
    
    # Matriz de satisfacción por área y período
    satisfaction_matrix = [
        [4.8, 4.6, 4.4, 4.2, 4.7, 4.1],  # Hora Pico
        [4.9, 4.8, 4.6, 4.5, 4.8, 4.3],  # Normal
        [4.7, 4.5, 4.3, 4.0, 4.6, 4.0]   # Nocturno
    ]
    
    return {
        'data': [go.Heatmap(
            z=satisfaction_matrix,
            x=areas,
            y=timeperiods,
            colorscale=[
                [0, '#ff4757'], [0.25, '#f59e0b'], [0.5, '#00d4ff'], [0.75, '#00ff88'], [1, '#00ff88']
            ],
            hovertemplate='<b>%{y} - %{x}</b><br>Satisfacción: %{z}/5<extra></extra>',
            showscale=True,
            colorbar=dict(
                title="Satisfacción",
                titleside="right",
                tickmode="array",
                tickvals=[3.5, 4.0, 4.5, 5.0],
                ticktext=["3.5", "4.0", "4.5", "5.0"],
                len=0.6
            )
        )],
        'layout': get_quality_chart_layout()
    }

@callback(Output('quality-nps-chart', 'figure'), Input('tabs', 'active_tab'))
def update_quality_nps_chart(active_tab):
    if active_tab != "quality":
        return {}
    
    labels = ['Promotores', 'Pasivos', 'Detractores']
    values = [58, 33, 9]
    colors = ['#00ff88', '#f59e0b', '#ff4757']
    
    return {
        'data': [go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker=dict(colors=colors, line=dict(color='#0a0e27', width=2)),
            hovertemplate='<b>%{label}</b><br>Porcentaje: %{value}%<br>NPS: %{percent}<extra></extra>',
            textinfo='label+percent',
            textposition='outside'
        )],
        'layout': {
            **get_quality_chart_layout(),
            'showlegend': False,
            'margin': dict(l=20, r=20, t=20, b=20),
            'annotations': [dict(text=f'NPS<br><b>67</b>', x=0.5, y=0.5, font_size=20, showarrow=False)]
        }
    }

@callback(Output('quality-trends-chart', 'figure'), Input('tabs', 'active_tab'))
def update_quality_trends_chart(active_tab):
    if active_tab != "quality":
        return {}
    
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    return {
        'data': [
            go.Scatter(x=months, y=[4.4, 4.5, 4.3, 4.6, 4.5, 4.7, 4.6, 4.8, 4.5, 4.6, 4.6, 4.6],
                      name='Satisfacción General', line=dict(color='#00ff88', width=3),
                      hovertemplate='<b>Satisfacción General</b><br>%{x}: %{y}/5<extra></extra>'),
            go.Scatter(x=months, y=[6.8, 6.5, 6.7, 6.4, 6.6, 6.2, 6.4, 6.1, 6.5, 6.3, 6.4, 6.4],
                      name='Tiempo Seguridad', line=dict(color='#f59e0b', width=3),
                      hovertemplate='<b>Tiempo Seguridad</b><br>%{x}: %{y} min<extra></extra>'),
            go.Scatter(x=months, y=[65, 62, 68, 64, 66, 69, 67, 70, 65, 67, 67, 67],
                      name='NPS Score', line=dict(color='#00d4ff', width=3),
                      hovertemplate='<b>NPS Score</b><br>%{x}: %{y}/100<extra></extra>'),
            go.Scatter(x=months, y=[3.4, 3.3, 3.5, 3.2, 3.4, 3.1, 3.2, 3.0, 3.3, 3.1, 3.2, 3.2],
                      name='Tiempo Check-in', line=dict(color='#8b5cf6', width=3),
                      hovertemplate='<b>Tiempo Check-in</b><br>%{x}: %{y} min<extra></extra>')
        ],
        'layout': get_quality_chart_layout()
    }

@callback(Output('quality-performance-matrix', 'figure'), Input('tabs', 'active_tab'))
def update_quality_performance_matrix(active_tab):
    if active_tab != "quality":
        return {}
    
    # Scatter plot: X=Tiempo de servicio, Y=Satisfacción, Tamaño=Volumen pasajeros
    areas = ['Terminal', 'Check-in', 'Seguridad', 'Comercial', 'Embarque', 'Equipaje']
    tiempo_servicio = [2.1, 3.2, 6.4, 15.3, 4.1, 8.1]
    satisfaccion = [4.8, 4.6, 4.4, 4.2, 4.7, 4.1]
    volumen_pax = [100, 85, 95, 60, 90, 80]  # Tamaño de burbuja
    
    return {
        'data': [go.Scatter(
            x=tiempo_servicio,
            y=satisfaccion,
            mode='markers+text',
            marker=dict(
                size=[v/2 for v in volumen_pax],
                color=['#00ff88', '#00d4ff', '#f59e0b', '#ff6b35', '#8b5cf6', '#ff4757'],
                opacity=0.7,
                line=dict(width=2, color='white')
            ),
            text=areas,
            textposition='middle center',
            hovertemplate='<b>%{text}</b><br>Tiempo: %{x} min<br>Satisfacción: %{y}/5<extra></extra>'
        )],
        'layout': {
            **get_quality_chart_layout(),
            'xaxis': {'title': 'Tiempo de Servicio (min)', 'color': '#a0aec0'},
            'yaxis': {'title': 'Satisfacción (1-5)', 'color': '#a0aec0', 'range': [3.8, 5.0]},
            'showlegend': False
        }
    }

# Removed unused callbacks for non-existent chart IDs

# Geographic Tab Callback - Simplified
@callback(Output('geographic-distribution-chart', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_geographic_distribution(n):
    route_data = get_route_data()
    
    # Agrupar por región
    regions = {'USA': 0, 'México': 0, 'LATAM': 0}
    for route in route_data:
        if 'USA' in route['city']:
            regions['USA'] += route['passengers']
        elif 'México' in route['city']:
            regions['México'] += route['passengers']
        else:
            regions['LATAM'] += route['passengers']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(regions.keys()),
        y=list(regions.values()),
        marker=dict(
            color=['#00d4ff', '#f59e0b', '#00ff88'],
        ),
        text=[f'{v:,}' for v in regions.values()],
        textposition='auto'
    ))
    
    fig.update_layout(
        xaxis=dict(title='Región', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Pasajeros Anuales', gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig

# Route Network Map Callbacks - Simplified version
@callback(
    Output('route-network-map', 'figure'),
    [Input('route-filter-all', 'n_clicks'),
     Input('route-filter-intl', 'n_clicks'),
     Input('route-filter-dom', 'n_clicks')]
)
def update_route_network(all_clicks, intl_clicks, dom_clicks):
    """Actualiza el mapa de rutas según el filtro seleccionado"""
    try:
        # Determinar filtro activo de manera simple
        ctx = dash.callback_context
        filter_type = 'all'  # Por defecto mostrar todas
        
        # Si hay context y fue triggereado, determinar qué botón
        if ctx.triggered and ctx.triggered[0]['prop_id'] != '.':
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'route-filter-intl':
                filter_type = 'international'
            elif button_id == 'route-filter-dom':
                filter_type = 'domestic'
        
        # Obtener datos
        data = get_route_network_data()
        hub = data['hub']
        routes = data['routes']
        
        # Aplicar filtro
        if filter_type == 'international':
            routes = [r for r in routes if r['type'] == 'international']
        elif filter_type == 'domestic':
            routes = [r for r in routes if r['type'] == 'domestic']
        
        # Crear figura
        fig = go.Figure()
        
        # 1. Hub AIFA - Marker central premium
        fig.add_trace(go.Scattergeo(
            lat=[hub['lat']],
            lon=[hub['lon']],
            text=['✈️ AIFA HUB'],
            mode='markers+text',
            marker=dict(
                size=45,
                color='#f59e0b',  # Color dorado para destacar
                line=dict(width=6, color='white'),
                symbol='star',
                opacity=1.0
            ),
            textposition='bottom center',
            textfont=dict(size=16, color='white', family='Inter'),
            name='AIFA Hub',
            hovertemplate='<b>🛬 AIFA - Hub Principal</b><br>📍 Felipe Ángeles International<br>🌐 Rutas Activas: ' + str(len(routes)) + '<br>📊 Estado: Operacional<extra></extra>'
        ))
        
        # 2. Líneas de rutas - Mejoradas para mayor visibilidad
        for route in routes:
            # Colores más contrastantes y visibles
            if route['type'] == 'international':
                line_color = '#00d4ff'  # Azul brillante para internacionales
                line_dash = 'solid'
            else:
                line_color = '#00ff88'  # Verde brillante para domésticas  
                line_dash = 'solid'
            
            # Grosor basado en volumen pero más grueso
            line_width = max(4, min(route['pax']/20000, 12))  # Entre 4 y 12px
            
            fig.add_trace(go.Scattergeo(
                lat=[hub['lat'], route['lat']],
                lon=[hub['lon'], route['lon']],
                mode='lines',
                line=dict(
                    width=line_width,
                    color=line_color,
                    opacity=1.0,  # Opacity completa para máxima visibilidad
                    dash=line_dash
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # 3. Markers de destinos - Rediseñados para mayor visibilidad
        for route in routes:
            # Tamaños más grandes y distintivos
            marker_size = max(18, min(route['pax']/8000, 35))  # Entre 18 y 35px
            
            # Colores más vibrantes y diferenciados
            if route['type'] == 'international':
                marker_color = '#ff6b35'  # Naranja vibrante para internacionales
                marker_symbol = 'square'
            else:
                marker_color = '#00ff88'  # Verde brillante para domésticas
                marker_symbol = 'circle'
            
            fig.add_trace(go.Scattergeo(
                lat=[route['lat']],
                lon=[route['lon']],
                text=[route['name']],
                mode='markers+text',
                marker=dict(
                    size=marker_size,
                    color=marker_color,
                    line=dict(width=4, color='white'),  # Border más grueso
                    symbol=marker_symbol,
                    opacity=1.0
                ),
                textposition='top center',
                textfont=dict(size=11, color='white', family='Inter'),
                showlegend=False,
                hovertemplate='<b>🎯 ' + route['name'] + '</b><br>' +
                             '👥 Pasajeros: ' + f"{route['pax']:,}" + '/año<br>' +
                             '✈️ Vuelos: ' + str(route['flights']) + '/mes<br>' +
                             '🌐 Tipo: ' + route['type'].title() + '<br>' +
                             '📈 Load Factor: Excelente<extra></extra>'
            ))
        
        # Layout del mapa - Optimizado para mejor contraste
        fig.update_layout(
            geo=dict(
                scope='world',
                projection_type='natural earth',
                showland=True,
                landcolor='rgba(15, 20, 35, 0.95)',  # Más oscuro para contraste
                showocean=True,
                oceancolor='rgba(5, 10, 25, 0.98)',  # Océano más profundo
                showcountries=True,
                countrycolor='rgba(0, 212, 255, 0.6)',  # Borders más visibles
                coastlinecolor='rgba(0, 212, 255, 0.7)',
                showlakes=False,  # Eliminar lagos para simplificar
                bgcolor='rgba(0,0,0,0)',
                showframe=False,
                center=dict(lat=25, lon=-95),
                projection_scale=1.1,  # Zoom ligeramente menor
                resolution=50  # Mejor resolución
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Inter'),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            height=500,
            title=dict(
                text="",
                x=0.5,
                font=dict(size=18, color='white')
            )
        )
        
        return fig
        
    except Exception as e:
        # En caso de error, devolver mapa básico
        print(f"Error en update_route_network: {str(e)}")
        
        # Mapa de respaldo básico
        fig = go.Figure()
        
        fig.add_trace(go.Scattergeo(
            lat=[19.7373],
            lon=[-99.0068],
            text=['AIFA'],
            mode='markers+text',
            marker=dict(size=30, color='#00d4ff'),
            textposition='bottom center'
        ))
        
        fig.update_layout(
            geo=dict(
                scope='world',
                projection_type='natural earth',
                showland=True,
                landcolor='rgba(26, 31, 58, 0.8)',
                showocean=True,
                oceancolor='rgba(10, 14, 39, 0.9)',
                center=dict(lat=25, lon=-95)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=0, r=0, t=0, b=0),
            height=500
        )
        
        return fig

@callback(
    [Output('route-filter-all', 'className'),
     Output('route-filter-intl', 'className'),
     Output('route-filter-dom', 'className')],
    [Input('route-filter-all', 'n_clicks'),
     Input('route-filter-intl', 'n_clicks'),
     Input('route-filter-dom', 'n_clicks')]
)
def update_filter_buttons(all_clicks, intl_clicks, dom_clicks):
    """Actualiza el estado activo de los botones de filtro"""
    try:
        ctx = dash.callback_context
        base_class = "filter-btn"
        active_class = "filter-btn active"
        
        # Por defecto, "Todas" está activo
        if not ctx.triggered or ctx.triggered[0]['prop_id'] == '.':
            return [active_class, base_class, base_class]
        
        # Determinar qué botón fue presionado
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'route-filter-all':
            return [active_class, base_class, base_class]
        elif button_id == 'route-filter-intl':
            return [base_class, active_class, base_class]
        elif button_id == 'route-filter-dom':
            return [base_class, base_class, active_class]
        else:
            return [active_class, base_class, base_class]
            
    except Exception as e:
        print(f"Error en update_filter_buttons: {str(e)}")
        # En caso de error, devolver estado por defecto
        return ["filter-btn active", "filter-btn", "filter-btn"]

# Productivity Chart Callbacks
@callback(Output('productivity-efficiency-matrix', 'figure'),
          [Input('tabs', 'active_tab')])
def update_efficiency_matrix(active_tab):
    if active_tab != "productivity":
        return {}
    return create_efficiency_matrix()

@callback(Output('productivity-benchmark-radar', 'figure'),
          [Input('tabs', 'active_tab')])
def update_benchmark_radar(active_tab):
    if active_tab != "productivity":
        return {}
    return create_benchmark_radar()

@callback(Output('productivity-trends', 'figure'),
          [Input('tabs', 'active_tab')])
def update_productivity_trends(active_tab):
    if active_tab != "productivity":
        return {}
    return create_productivity_trends()

@callback(Output('productivity-roi-scatter', 'figure'),
          [Input('tabs', 'active_tab')])
def update_roi_scatter(active_tab):
    if active_tab != "productivity":
        return {}
    return create_roi_scatter()

@callback(Output('productivity-capacity-gauges', 'figure'),
          [Input('tabs', 'active_tab')])
def update_capacity_gauges(active_tab):
    if active_tab != "productivity":
        return {}
    return create_capacity_gauges()

@callback(Output('productivity-cost-waterfall', 'figure'),
          [Input('tabs', 'active_tab')])
def update_cost_waterfall(active_tab):
    if active_tab != "productivity":
        return {}
    return create_cost_waterfall()

# Time update callback - Ciudad de México timezone
@callback(Output('live-update-time', 'children'),
          Input('interval-component', 'n_intervals'))
def update_time(n):
    # Timezone de Ciudad de México
    mexico_tz = pytz.timezone('America/Mexico_City')
    now = datetime.now(mexico_tz)
    return now.strftime("%d/%m/%Y %H:%M:%S CST")

# Authentication Callbacks for Metodología Tab
@callback(
    Output("auth-modal", "is_open"),
    [Input("open-auth-modal", "n_clicks"), 
     Input("auth-cancel", "n_clicks"),
     Input("auth-submit", "n_clicks")],
    [State("auth-modal", "is_open"),
     State("auth-username", "value"),
     State("auth-password", "value")]
)
def toggle_auth_modal(open_clicks, cancel_clicks, submit_clicks, is_open, username, password):
    """Control del modal de autenticación"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return False
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if button_id == "open-auth-modal":
        return True
    elif button_id == "auth-cancel":
        return False
    elif button_id == "auth-submit":
        # Aquí validaríamos las credenciales - por ahora aceptamos cualquier valor
        if username and password:
            return False  # Cerrar modal si hay credenciales
        else:
            return True   # Mantener abierto si faltan datos
    
    return is_open

@callback(
    [Output("protected-content", "children"),
     Output("protected-content", "style"),
     Output("auth-message", "children")],
    [Input("auth-submit", "n_clicks")],
    [State("auth-username", "value"),
     State("auth-password", "value")]
)
def authenticate_and_show_content(submit_clicks, username, password):
    """Autenticación y mostrar contenido protegido"""
    if not submit_clicks:
        return [], {'display': 'none'}, ""
    
    # Sistema de autenticación robusto con credenciales seguras
    if username and password:
        # Credenciales autorizadas - Nivel Enterprise
        valid_credentials = {
            'director-aifa': 'AIFAExec2024!Tech',
            'gerente-ops': 'OpsSecure#2024',
            'metodologia-senior': 'TechDoc2024$AIFA',
            'ingeniero-sistemas': 'SysArch!2024#Safe',
            'analista-datos': 'DataAIFA2024@Secure',
            'consultor-externo': 'Consultant#AIFA24',
            'auditor-tecnico': 'Audit2024!Technical'
        }
        
        # Validación exacta de credenciales
        if username.lower() in valid_credentials and password == valid_credentials[username.lower()]:
            return render_protected_methodology_content(), {'display': 'block'}, ""
        else:
            return [], {'display': 'none'}, "⚠️ Acceso denegado. Credenciales inválidas o cuenta suspendida."
    else:
        return [], {'display': 'none'}, "🔐 Ingrese credenciales válidas para acceder a documentación técnica."

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)