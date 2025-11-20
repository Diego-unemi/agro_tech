# Resumen de Implementación - Sistema AgroTech

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```
2. **Configurar variables de entorno (.env):**
```env
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_PHONE_NUMBER=+1234567890
REDIS_URL=redis://localhost:6379/0
```
##  Pasos Siguientes para ejecutar el Sistema

### 1. Crear migraciones de base de datos
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
### 2. Crear superusuario
```bash
python manage.py createsuperuser
```
### Modelos (6 nuevos modelos)
- ✅ CustomUser (extendido)
- ✅ Finca
- ✅ Zona
- ✅ Sensor
- ✅ UmbralAlerta
- ✅ Alerta


