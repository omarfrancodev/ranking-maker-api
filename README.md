# Ranking Maker API

## Descripción

Esta API es parte de una aplicación web diseñada para gestionar y visualizar rankings de programas de televisión, anime, series y películas. Los usuarios pueden registrar shows, categorías, subcategorías, y ver rankings personalizados basados en las visualizaciones de cada persona.

## Características

- **Personas**: Registro de personas que pueden ver y rankear contenido.
- **Categorías y Subcategorías**: Organización de contenido en categorías (como TV Shows, Anime, Series, Películas) y subcategorías.
- **Contenido**: Gestión de shows con información básica.
- **Visualizaciones**: Registro de qué personas han visto qué shows y cuándo.
- **Rankings**: Asignación de rankings personalizados por persona y por subcategoría.

## Estructura del Proyecto

La API está organizada en múltiples aplicaciones de Django, cada una de las cuales maneja una parte específica del dominio:

- `people`: Gestión de las personas que interactúan con la aplicación.
- `categories`: Gestión de las categorías y subcategorías del contenido.
- `content`: Gestión de los shows de TV, anime, series y películas.
- `views`: Registro de las visualizaciones de los shows por parte de las personas.
- `rankings`: Gestión de los rankings personalizados por persona y subcategoría.

## Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/ranking-maker.git
   cd ranking-maker
   ```
2. **Crea y activa un entorno virtual:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno:**
Crea un archivo `.env` en el directorio raíz del proyecto y configura las siguientes variables:
   ```bash
    DEBUG=True
    SECRET_KEY=tu_secreto
    DATABASE_URL=postgres://usuario:password@localhost:5432/ranking_db
   ```

5. **Aplica las migraciones:**

   ```bash
   python manage.py migrate
   ```

6. **Crea un superusuario:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecuta el servidor de desarrollo:**

   ```bash
   python manage.py runserver
   ```

## Uso
La API ofrece endpoints para gestionar personas, categorías, subcategorías, contenido, visualizaciones y rankings. Algunos de los principales endpoints son:

- Personas:
  - GET `/api/people/`: Lista de personas.
  - POST `/api/people/`: Crear una nueva persona.

- Categorías:
  - GET /api/categories/: Lista de categorías.
  - POST /api/categories/: Crear una nueva categoría.

- Contenido:
  - GET /api/content/: Lista de contenido.
  - POST /api/content/: Crear un nuevo contenido.
  
- Visualizaciones:
  - POST /api/views/: Registrar que una persona ha visto un show.

- Rankings:
  - GET /api/rankings/: Obtener los rankings de una persona por categoría y subcategoría.
  - POST /api/rankings/: Crear un nuevo ranking.
