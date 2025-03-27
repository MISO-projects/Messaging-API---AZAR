
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

##  Endpoints  

### 1. ➕ Agregar Email a Lista Negra  

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
