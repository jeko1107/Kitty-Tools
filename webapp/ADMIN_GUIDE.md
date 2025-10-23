# Panel de Admin Mejorado - Guía de Uso

## 🎨 Interfaz Visual Mejorada

El panel de administración ahora tiene una interfaz completamente rediseñada con:

### ✨ Características Principales

1. **Dashboard Visual**: Estadísticas y métricas presentadas en tarjetas con colores
2. **Tabla Interactiva**: Historial de simulaciones con iconos y estados visuales
3. **Visualización Detallada**: Página dedicada para ver resultados de cada simulación
4. **Diseño Responsive**: Grid layout que se adapta a diferentes tamaños de pantalla
5. **Código de Colores**: Estados visuales claros (verde=éxito, rojo=error, amarillo=pendiente)

### 🚀 Cómo Usar

#### 1. Acceder al Panel
```
URL: http://localhost:5000/login
Usuario: admin
Contraseña: admin
```

#### 2. Ejecutar Simulaciones

En el panel principal (`/admin`), encontrarás el formulario de simulación:

**Simulación Flood (🌊 Kahoot Flood)**
```
Parámetros: n=50,minlat=50,maxlat=300
- n: número de bots a simular
- minlat: latencia mínima en milisegundos
- maxlat: latencia máxima en milisegundos

Ejemplo: n=100,minlat=25,maxlat=200
```

**Simulación Answers (📝 Answer Hack)**
```
Parámetros: n=50,q=10,acc=0.7
- n: número de bots
- q: número de preguntas
- acc: precisión/tasa de acierto (0.0 a 1.0)

Ejemplo: n=75,q=20,acc=0.85
```

**Simulación GUI (🖥️ Interfaz Gráfica)**
```
Parámetros: e=20
- e: número de eventos a simular

Ejemplo: e=50
```

#### 3. Ver Resultados

Después de ejecutar una simulación, serás redirigido automáticamente a la página de resultados donde verás:

**Para Flood:**
- Total de bots creados
- Número de errores
- Tiempo total de ejecución
- Tasa de éxito
- Tabla detallada de cada bot con delays y tiempos de respuesta

**Para Answers:**
- Total de bots y preguntas
- Precisión configurada
- Score promedio
- Tabla con rendimiento individual de cada bot
- Barras de progreso visuales

**Para GUI:**
- Total de eventos simulados
- Tiempo de ejecución
- Log detallado de eventos con timestamps

#### 4. Gestionar Simulaciones

En el historial puedes:
- 👁️ Ver resultados detallados (botón Ver)
- 💾 Descargar JSON con todos los datos (botón JSON)
- Filtrar por tipo y estado

### 🎯 Ejemplos de Uso

**Simular un ataque masivo de bots:**
```
Tipo: Flood
Parámetros: n=500,minlat=10,maxlat=100
```

**Probar precisión de bots en quiz:**
```
Tipo: Answers
Parámetros: n=100,q=25,acc=0.9
```

**Simular eventos de UI:**
```
Tipo: GUI
Parámetros: e=100
```

### 📊 Visualización de Datos

El panel muestra:
- **Métricas en tiempo real**: Números grandes y destacados
- **Gráficos de barras**: Para visualizar progreso y scores
- **Tablas ordenables**: Con todos los datos detallados
- **Códigos de color**: Verde (éxito), Rojo (error), Amarillo (advertencia)
- **Estados visuales**: Iconos ✓ y ✗ para estados de bots

### 🔧 Características Técnicas

- **Sin conexiones de red**: Todas las simulaciones son locales y seguras
- **Almacenamiento JSON**: Cada simulación se guarda en `webapp/jobs/`
- **Autenticación segura**: Login con CSRF protection
- **Responsive**: Funciona en desktop y móvil
- **Scrollable**: Tablas con scroll para grandes datasets

### 🎨 Personalización de Parámetros

Puedes ajustar los parámetros según tus necesidades:

**Simulación pequeña (prueba rápida):**
```
Flood: n=10,minlat=50,maxlat=150
Answers: n=20,q=5,acc=0.7
GUI: e=10
```

**Simulación mediana (testing):**
```
Flood: n=100,minlat=25,maxlat=200
Answers: n=75,q=15,acc=0.8
GUI: e=50
```

**Simulación grande (stress test):**
```
Flood: n=1000,minlat=10,maxlat=300
Answers: n=500,q=30,acc=0.9
GUI: e=200
```

### 📝 Notas Importantes

- Las simulaciones NO realizan conexiones de red reales
- Los datos son generados de forma aleatoria y determinística
- Todos los resultados se guardan localmente
- Puedes descargar cualquier resultado en formato JSON
- El panel está optimizado para mostrar grandes cantidades de datos

### 🔒 Seguridad

- Autenticación requerida para todas las operaciones
- CSRF protection en todos los formularios
- Contraseñas hasheadas con bcrypt
- Límite de intentos de login
- Sesiones seguras

---

**Servidor:** http://localhost:5000  
**Panel Admin:** http://localhost:5000/admin  
**Login:** http://localhost:5000/login  

**Credenciales por defecto:**  
Usuario: `admin`  
Contraseña: `admin`
