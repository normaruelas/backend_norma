PASOS RÁPIDOS

1) Crear y activar entorno virtual
------------------------------------------------
python -m venv venv
venv\Scripts\activate     (Windows)
# o en Linux/Mac: source venv/bin/activate

2) Instalar dependencias
------------------------------------------------
pip install -r requirements.txt

3) Migraciones, superusuario, ejecutar
------------------------------------------------
cd backend_norma/backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

4) (Opcional) Semilla de datos iniciales
------------------------------------------------
# En otra terminal, con el venv activo y dentro de backend_norma/backend:
python manage.py seed_menu

5) Panel y API
------------------------------------------------
Admin:        http://127.0.0.1:8000/admin/
Export JSON:  http://127.0.0.1:8000/api/menu_export/

6) Frontend
------------------------------------------------
En tu HTML, carga datos desde:
fetch('http://127.0.0.1:8000/api/menu_export/')
