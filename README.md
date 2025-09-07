# KSM
(NOTA: Aun en construccion)
Cascaron de APIS con CRUD de usuarios para partir de este codigo.

# Pasos para instalar el Sistema

# Instaladores
| Nombre                   | Instalador                                            |
|:-------------------------|:------------------------------------------------------| 
| `Compilador`             | Python3                                               |
| `IDE de programación`    | Visual Studio Code , Sublime Text , Atom , Vim , etc. |
| `FrameWorks`             |  [Django](https://www.djangoproject.com/ "Django") , [Django REST](https://www.django-rest-framework.org/ "Django REST")               |
| `Motor de base de datos` | MySQL , PostgreSQL , Sqlite3                          |

##### Paso 01: Erradicar Windows de tu vida.

Despues de haber cumplido con el paso 01, podemos pasar al paso 02.

##### Paso 02: Clonar el proyecto.

Linux:

```bash

git clone https://github.com/kayrosama/apibase.git
cd apibase
apt-get install -f -y python3-pip python3-venv
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

```

##### Paso 03: ...

En el archivo model debes encontrar estas variables y comentarlas.

```bash

users/models.py

    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username']

```

##### Paso 04: ...

Debe eliminar la base de datos creada [db.sqlite3], el archivo [users/migrations/00*.py] y posteriormente ejecutar la nueva migracion.

```bash

rm ./db.sqlite3
rm ./users/migrations/00*.py
python3 manage.py makemigrations
python3 manage.py migrate

```

##### Paso 05: ...

Mientras esta aun este desarrollando el proyecto se debe crear un super usuario con credenciales faciles de recordar.  Se muestra sugerencia para crear el super usuario de aplicacion.

```bash

python3 manage.py createsuperuser

username: admin
email: master@kmkz.io
password: adm123

```

##### Paso 06: ...

Antes de levantar el servicio y probar el super usuario creado, debe de descomentrar las variables que comento.

```bash

users/models.py

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

...

python3 manage.py runserver

http://127.0.0.1:8000/admin
email: master@kmkz.io
password: adm123

```

##### Paso 07: ...

------------

#  ありがとう

***KSM, 2024.***

