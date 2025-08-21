import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_kpi_data():
    """Generate simulated KPI data for AIFA"""
    return {
        'participation_passengers': {
            'current': 12.8,
            'change': 2.3,
            'trend': 'up',
            'target': 15.0
        },
        'participation_operations': {
            'current': 9.7,
            'change': 1.8,
            'trend': 'up',
            'target': 12.0
        },
        'participation_cargo': {
            'current': 8.4,
            'change': 3.1,
            'trend': 'up',
            'target': 10.0
        },
        'growth_vs_market': {
            'current': 5.5,
            'change': 0.8,
            'trend': 'up'
        },
        'punctuality': {
            'current': 87.2,
            'change': -1.3,
            'trend': 'down',
            'target': 90.0
        },
        'route_utilization': {
            'current': 78.4,
            'change': 2.1,
            'trend': 'up',
            'target': 85.0
        }
    }

def generate_historical_data():
    """Generate historical trend data"""
    dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
    
    # Market participation trend
    base_participation = 8.0
    participation_data = []
    
    for i in range(12):
        value = base_participation + (i * 0.4) + np.random.normal(0, 0.3)
        participation_data.append({
            'date': dates[i],
            'passengers': max(0, value + np.random.normal(0, 0.2)),
            'operations': max(0, value - 1.5 + np.random.normal(0, 0.15)),
            'cargo': max(0, value - 2.0 + np.random.normal(0, 0.25))
        })
    
    return pd.DataFrame(participation_data)

def generate_airport_comparison():
    """Generate comparison data with other Mexican airports"""
    airports = [
        {'name': 'AICM', 'passengers': 48.2, 'operations': 41.3, 'change': -2.1},
        {'name': 'AIFA', 'passengers': 12.8, 'operations': 9.7, 'change': 2.3},
        {'name': 'Guadalajara', 'passengers': 8.9, 'operations': 10.2, 'change': 0.8},
        {'name': 'Cancún', 'passengers': 15.4, 'operations': 12.8, 'change': 1.2},
        {'name': 'Monterrey', 'passengers': 7.2, 'operations': 8.1, 'change': -0.3},
        {'name': 'Tijuana', 'passengers': 4.9, 'operations': 6.3, 'change': 0.5},
        {'name': 'Otros', 'passengers': 2.6, 'operations': 11.6, 'change': -0.4}
    ]
    return pd.DataFrame(airports)

def generate_route_data():
    """Generate route network data"""
    routes = [
        {'city': 'Guadalajara', 'country': 'México', 'lat': 20.5218, 'lon': -103.3111, 
         'passengers': 125000, 'frequency': 42, 'load_factor': 82.3},
        {'city': 'Monterrey', 'country': 'México', 'lat': 25.7785, 'lon': -100.1069,
         'passengers': 98000, 'frequency': 35, 'load_factor': 78.5},
        {'city': 'Cancún', 'country': 'México', 'lat': 21.0368, 'lon': -86.8770,
         'passengers': 156000, 'frequency': 28, 'load_factor': 89.2},
        {'city': 'Los Angeles', 'country': 'USA', 'lat': 34.0522, 'lon': -118.2437,
         'passengers': 87000, 'frequency': 21, 'load_factor': 85.7},
        {'city': 'Houston', 'country': 'USA', 'lat': 29.9844, 'lon': -95.3414,
         'passengers': 76000, 'frequency': 19, 'load_factor': 81.3},
        {'city': 'Miami', 'country': 'USA', 'lat': 25.7617, 'lon': -80.1918,
         'passengers': 92000, 'frequency': 17, 'load_factor': 87.4},
        {'city': 'Bogotá', 'country': 'Colombia', 'lat': 4.7110, 'lon': -74.0721,
         'passengers': 45000, 'frequency': 14, 'load_factor': 79.8},
        {'city': 'Lima', 'country': 'Perú', 'lat': -12.0464, 'lon': -77.0428,
         'passengers': 38000, 'frequency': 10, 'load_factor': 82.1}
    ]
    
    # Add AIFA location
    for route in routes:
        route['origin_lat'] = 19.7369
        route['origin_lon'] = -99.0256
    
    return pd.DataFrame(routes)

def generate_state_penetration():
    """Generate state penetration data for Mexico"""
    states = {
        'Ciudad de México': 45.2,
        'Estado de México': 38.7,
        'Jalisco': 12.3,
        'Nuevo León': 8.9,
        'Puebla': 7.2,
        'Querétaro': 6.8,
        'Guanajuato': 5.9,
        'Veracruz': 4.2,
        'Hidalgo': 15.3,
        'Michoacán': 3.8,
        'Chihuahua': 2.1,
        'Coahuila': 1.9,
        'San Luis Potosí': 3.4,
        'Aguascalientes': 2.8,
        'Morelos': 4.5,
        'Tlaxcala': 8.9
    }
    
    data = []
    for state, penetration in states.items():
        data.append({
            'state': state,
            'penetration': penetration,
            'passengers': int(penetration * 25000 + np.random.randint(-5000, 5000))
        })
    
    return pd.DataFrame(data)

def generate_financial_data():
    """Generate financial performance data"""
    months = pd.date_range(end=datetime.now(), periods=12, freq='M')
    
    financial_data = []
    base_revenue = 150  # Million MXN
    
    for i, month in enumerate(months):
        revenue = base_revenue + (i * 8) + np.random.normal(0, 10)
        costs = revenue * 0.75 + np.random.normal(0, 5)
        
        financial_data.append({
            'month': month,
            'revenue': revenue,
            'costs': costs,
            'ebitda': revenue - costs,
            'margin': ((revenue - costs) / revenue) * 100
        })
    
    return pd.DataFrame(financial_data)

def generate_operational_metrics():
    """Generate operational performance metrics"""
    return {
        'daily_operations': 287,
        'on_time_departure': 87.2,
        'gate_utilization': 82.4,
        'turnaround_time': 38.5,  # minutes
        'passenger_flow': 42500,  # daily
        'cargo_volume': 1250,  # tons daily
        'aircraft_movements': {
            'domestic': 198,
            'international': 89
        }
    }