# Prueba técnica Talento-B Carlos Morales

Este proyecto es una aplicación web desarrollada en **Django** para que los Auditores puedan registrar las validaciones de diseño y operatividad de los controles de riesgos en una organización. La aplicación utiliza una base de datos **PostgreSQL**.

## Características principales

- **Pantalla de Login:** Permite a los Auditores ingresar con su usuario, contraseña, seleccionar el ciclo (Semestre 1 o 2) y el año (desde 2022 hasta el año actual).
- **Pantalla Inicial del Auditor:** Muestra los controles asignados al auditor para el ciclo seleccionado, con información básica de cada control.
- **Pantalla de Diseño:** Permite registrar la validación del diseño de un control, incluyendo preguntas obligatorias y opcionales para determinar la calificación del diseño.
- **Pantalla de Encabezado:** Facilita el registro del inicio y finalización de la validación, así como el tiempo invertido. Los controles pueden marcarse como "Terminados" solo si la conclusión del diseño está definida.

## Tecnologías utilizadas

- **Backend:** Django (Python)
- **Base de datos:** PostgreSQL
- **Frontend:** HTML, TailwindCSS, JavaScript (en combinación con Django templates)

## Requisitos previos

Antes de instalar el proyecto, asegúrate de tener instalados:

- Python 3.8 o superior
- PostgreSQL
- Pip (gestor de paquetes de Python)
- Virtualenv (opcional, pero recomendado)

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto:

1: Clona el repositorio:

``` bash
  git clone https://github.com/KrlosPK/proyecto-auditoria.git
  cd proyecto-auditoria
```

2: Crea y activa un entorno virtual:

``` bash
  python -m venv virt
  .\virt\Scripts\activate # En MAC usa `.\virt\bin\activate`
```

3: Instala las dependencias:

``` bash
  pip install -r requirements.txt
```

4: Configura la base de datos PostgreSQL:

- Crea una base de datos en PostgreSQL para el proyecto.

- Crea un archivo ```.env``` en esta ruta: ```.\proyecto-auditoria\.env``` con las siguientes variables:

``` bash
SECRET_KEY="django-insecure-qjivck_8826q3)yp_-kar-ur)1v)+i1sv@9ut&-n7r856ocyus"
DB_NAME="<nombre_de_tu_base_de_datos>"
DB_USER="<usuario>", # Por lo general es `postgres`
DB_PASSWORD="<contraseña>"
DB_HOST="localhost"
DB_PORT="5432"
```

5: Realiza las migraciones:

``` bash
  python .\manage.py makemigrations
  python .\manage.py migrate
```

6: Crea un superusuario:

``` bash
  python .\manage.py createsuperuser
```

7: Inicia el servidor de desarrollo:

``` bash
  python .\manage.py runserver
```

8: [Accede a la aplicación en tu navegador dando click en este enlace](http://127.0.0.1:8000)
