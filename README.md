
#  Blacklist API

##  Descripción General  
API REST que permite gestionar una lista negra global de emails. Proporciona funcionalidades para agregar emails a la lista negra y consultar si un email específico está en ella.

##  Características Principales  
- Autenticación mediante token estático  
- Almacenamiento en base de datos PostgreSQL  
- Registro automático de IP y timestamp  
- Respuestas en formato JSON  

##  Información General  
- **URL Base:** `http://localhost:8000`  
- **Autenticación:** Token estático  
- **Token:** `Bearer token123456`  
- **Formato:** JSON  

## Pruebas Unitarias 

Esta sección describe cómo ejecutar las pruebas unitarias.

### Requisitos

Para ejecutar las pruebas, necesitas instalar las dependencias de prueba:

```bash
pip install -r requirements-test.txt
```

### Ejecutar las pruebas

Para ejecutar todas las pruebas unitarias:

```bash
pytest
```

Para ejecutar las pruebas con cobertura:

```bash
pytest --cov=application
```

Para generar un reporte HTML de cobertura:

```bash
pytest --cov=application --cov-report=html
```

Esto generará un directorio `htmlcov` con el reporte de cobertura.

### Estructura de las pruebas

Las pruebas están organizadas en el directorio `tests/`:

- `test_blacklist.py`: Pruebas para los endpoints de la API de blacklist
- `conftest.py`: Configuración y fixtures para pytest

### Mocks

Las pruebas utilizan `unittest.mock` para simular la base de datos, lo que permite ejecutar las pruebas sin necesidad de una conexión a la base de datos real. 

##  Endpoints  

### 1. Agregar Email a Lista Negra  

**Endpoint:** `POST /blacklists`  
**Descripción:** Registra un email en la lista negra global junto con información adicional como el ID de la aplicación cliente y el motivo del bloqueo.

**Parámetros de Entrada:**  
- `email` (obligatorio): Email del cliente a bloquear  
- `app_uuid` (obligatorio): Identificador UUID de la aplicación cliente  
- `blocked_reason` (opcional): Motivo del bloqueo (máximo 255 caracteres)  

**Datos Capturados Automáticamente:**  
- IP de origen de la solicitud  
- Fecha y hora de la solicitud  

**Ejemplo de Solicitud:**  
```json
{
  "email": "ejemplo@dominio.com",
  "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "blocked_reason": "Comportamiento sospechoso"
}
```

**Respuestas:**  
- `201`: Email agregado exitosamente  
- `400`: Datos inválidos o faltantes  
- `401`: Token de autorización inválido  

### 2.  Verificar Email en Lista Negra  

**Endpoint:** `GET /blacklists/{email}`  
**Descripción:** Consulta si un email específico se encuentra registrado en la lista negra global.

**Parámetros de URL:**  
- `email`: Email a consultar  

**Ejemplo de Respuesta:**  
```json
{
  "is_blacklisted": true,
  "blocked_reason": "Comportamiento sospechoso"
}
```

**Respuestas:**  
- `200`: Consulta exitosa  
- `401`: Token de autorización inválido  

##  Seguridad  
- Todas las solicitudes requieren un token de autorización  
- El token debe enviarse en el header `Authorization`  
- Formato del token: `Bearer token123456`  

##  Consideraciones  
- La API registra automáticamente la IP de origen de cada solicitud  
- Se mantiene un registro de fecha y hora para cada entrada  
- Los UUIDs deben ser válidos y únicos  
- El motivo de bloqueo es opcional pero no puede exceder 255 caracteres  

## Pruebas de carga
Comando para ejecutar pruebas de carga con apache benchmarking

```sh
ab -n 5000 -c 1000 -t 10 -T 'application/json' -H "Authorization: Bearer token123456" -p blacklist_payload.json LB-blacklist-825409258.us-east-1.elb.amazonaws.com/blacklists
```