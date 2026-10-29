# Guía para clonar y levantar el proyecto

## 1. Clonar el repositorio

Como no tengo la URL concreta de tu repositorio, utiliza:

```bash
git clone <URL_DEL_REPOSITORIO>
```

Por ejemplo:

```bash
git clone https://github.com/usuario/product-service.git
```

Entrar al proyecto:

```bash
cd product-service
```

## 2. Verificar Python

El proyecto puede ejecutarse con Python 3.12:

```bash
python --version
```

Resultado esperado:

```text
Python 3.12.x
```

## 3. Crear entorno virtual

En PowerShell:

```powershell
python -m venv .venv
```

Activarlo:

```powershell
.venv\Scripts\Activate.ps1
```

Deberías observar:

```text
(.venv) PS ...\product-service>
```

Salir del entorno virtual:

```
deactivate
```
## 4. Instalar dependencias

Si el proyecto contiene:

```text
requirements.txt
```

ejecuta:

```bash
pip install -r requirements.txt
```

Las dependencias principales son:

- FastAPI
- Uvicorn
- SQLAlchemy
- psycopg
- pydantic-settings
- python-dotenv

Si necesitas regenerar el archivo:

```bash
pip freeze > requirements.txt
```

## 5. Configurar variables de entorno

Crea:

```text
.env
```

Puedes utilizar:

```env
APP_NAME=product-service
APP_VERSION=1.0.0
API_V1_STR=/api/v1

ENABLE_SEED=true

DB_HOST=127.0.0.1
DB_PORT=5433
DB_NAME=product_db
DB_USER=product_user
DB_PASSWORD=Product_DB_2026.Change.This.Password
```

Si reutilizas PostgreSQL en el puerto estándar:

```env
DB_PORT=5432
```

## 6. Levantar PostgreSQL

Si tienes un `docker-compose.yml` propio del product-service:

```bash
docker compose up -d
```

Verifica:

```bash
docker compose ps
```

El estado debería indicar algo similar a:

```text
product-postgres    Up    healthy
```

### Si ya tienes PostgreSQL del User Service

Si el otro PostgreSQL utiliza:

```yaml
5432:5432
```

no levantes otro contenedor también con:

```yaml
5432:5432
```

porque obtendrás un error de puerto ocupado.

Para Product Service puedes utilizar:

```yaml
ports:
  - "5433:5432"
```

Entonces en `.env`:

```env
DB_PORT=5433
```

La lógica es:

```text
Windows             Docker
localhost:5433 ───► PostgreSQL:5432
```

## 7. Verificar la base de datos

Por ejemplo:

```bash
docker exec -it product-postgres psql -U product_user -d product_db
```

Dentro de PostgreSQL:

```sql
\dt
```

Una vez levantada la aplicación deberían aparecer:

```text
products
categories
product_categories
```

Salir:

```sql
\q
```

## 8. Levantar FastAPI

Con el entorno virtual activado:

```bash
uvicorn app.main:app --reload
```

Resultado esperado:

```text
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

## 9. Seed automático

Como tenemos:

```env
ENABLE_SEED=true
```

al iniciar el proyecto se ejecutará:

```text
init_db()
      │
      ▼
crear tablas
      │
      ▼
seed_database()
      │
      ├── categorías
      ├── productos
      └── producto-categoría
```

Por ejemplo:

```text
🌱 Iniciando siembra de Product Service

📂 Registrando categorías...
📦 Registrando productos...
🔗 Registrando relaciones producto-categoría...

✅ Siembra completada correctamente
```

El seed es idempotente, por lo que reiniciar la aplicación no debería duplicar los registros.

También se puede ejecutar manualmente:

```bash
python -m app.db.seed
```

## 10. Comprobar que funciona

Abre:

```text
http://127.0.0.1:8000/health
```

Respuesta:

```json
{
  "status": "ok",
  "service": "product-service"
}
```

Después:

```text
http://127.0.0.1:8000/docs
```

Swagger permitirá ejecutar directamente:

- Products
- Categories
- Product Categories

sin necesidad de Postman.

## 11. Secuencia recomendada después de clonar

En Windows/PowerShell, el proceso completo puede resumirse así:

```powershell
git clone <URL_DEL_REPOSITORIO>

cd product-service

python -m venv .venv

.venv\Scripts\Activate.ps1

pip install -r requirements.txt

docker compose up -d

uvicorn app.main:app --reload
```

Después accede a:

Swagger:

```text
http://127.0.0.1:8000/docs
```

Health:

```text
http://127.0.0.1:8000/health
```

Si `ENABLE_SEED=true`, no necesitas registrar manualmente datos iniciales: al levantar el servicio se crearán automáticamente categorías, productos y sus relaciones producto-categoría.