# 🚀 AIFA Dashboard Ejecutivo

Dashboard profesional de nivel Bloomberg para el Aeropuerto Internacional Felipe Ángeles (AIFA).

**🌐 Demo en vivo:** [https://aifa-dashboard.onrender.com](https://aifa-dashboard.onrender.com)

Construido con Dash + Plotly + CSS Glassmorphism para análisis ejecutivo en tiempo real.

## ✨ Características

- **Diseño Cyber-Executive**: Efectos glassmorphism con colores corporativos
- **7 Módulos Analíticos**: KPIs Estratégicos, Capacidad, Seguridad, Calidad, Productividad, Financiero, Geográfico
- **Gráficos Interactivos**: Plotly con mapas, gauges, tendencias y tablas comparativas
- **Datos en Tiempo Real**: Actualización automática cada 30 segundos
- **Responsive Design**: Optimizado para desktop y mobile
- **Deploy Ready**: Configurado para Render.com

## 🎨 Paleta de Colores

- **Cyan Primario**: `#00d4ff`
- **Dorado**: `#f59e0b` 
- **Azul Oscuro**: `#0a0e27`
- **Verde Éxito**: `#00ff88`
- **Rojo Error**: `#ff4757`

## 🚀 Instalación Local

```bash
# Clonar repositorio
git clone <repository-url>
cd aifa-dashboard

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

La aplicación estará disponible en `http://localhost:8050`

## 📊 Módulos del Dashboard

### 1. KPIs Estratégicos
- Participación nacional en pasajeros, operaciones y carga
- Crecimiento vs mercado
- Puntualidad de vuelos
- Utilización de rutas
- Gráficos de tendencia y progreso hacia metas

### 2. Análisis Geográfico
- Mapa mundial de rutas internacionales
- Penetración por estados de México
- Top destinos por volumen
- Factor de carga por ruta
- Análisis frecuencia vs pasajeros

### 3. Análisis Financiero
- Evolución de ingresos y costos
- Margen EBITDA
- Tendencias de rentabilidad

### 4. Otros Módulos
- Capacidad Operativa
- Seguridad 
- Calidad de Servicio
- Productividad

## 🌐 Deploy en Render.com

### Automático desde GitHub:

1. **Fork/Clone** este repositorio
2. **Conectar** a Render.com
3. **Crear Web Service** con configuración:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server`
   - **Python Version**: 3.11.5

### Manual:

```bash
# Crear archivo .env (opcional)
echo "PORT=8050" > .env

# Deploy
git add .
git commit -m "Deploy AIFA Dashboard"
git push origin main
```

## 📁 Estructura del Proyecto

```
aifa-dashboard/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias
├── Procfile              # Configuración Render/Heroku
├── runtime.txt           # Versión Python
├── assets/
│   └── style.css         # CSS profesional
├── src/
│   ├── data/
│   │   └── simulated_data.py    # Datos simulados
│   └── layouts/
│       ├── strategic.py         # KPIs estratégicos
│       ├── geographic.py        # Análisis geográfico
│       ├── financial.py         # Análisis financiero
│       ├── capacity.py          # Capacidad operativa
│       ├── security.py          # Seguridad
│       ├── quality.py           # Calidad
│       └── productivity.py      # Productividad
└── README.md
```

## 🛠️ Tecnologías

- **Frontend**: Dash 2.14.2, Plotly 5.18.0
- **Styling**: CSS3 con Glassmorphism, Bootstrap Components
- **Icons**: Dash Iconify (Material Design)
- **Data**: Pandas, NumPy (datos simulados)
- **Deploy**: Gunicorn, Render.com ready

## 📈 Datos Simulados

El dashboard incluye datos simulados realistas para demostración:

- **KPIs**: Participación de mercado, crecimiento, puntualidad
- **Rutas**: 8 destinos principales con métricas de tráfico
- **Financiero**: 12 meses de datos de ingresos/costos
- **Geográfico**: Penetración por estados mexicanos

## 🎯 Características Técnicas

- **Performance**: <3s tiempo de carga
- **Responsivo**: Breakpoints para mobile y desktop  
- **Accesibilidad**: Contraste WCAG, navegación por teclado
- **SEO**: Meta tags optimizados
- **PWA Ready**: Configuración para app móvil

## 📞 Soporte

Para dudas o mejoras, crear un issue en el repositorio.

---

**Desarrollado para el Aeropuerto Internacional Felipe Ángeles (AIFA)**  
*Dashboard Ejecutivo Profesional - Versión 1.0*