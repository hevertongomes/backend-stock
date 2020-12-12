#!/bin/sh

echo "Running makemigrations..."
python manage.py makemigrations
echo "Running migrate..."
python manage.py migrate
echo "Running loaddata items_initial_data.json..."
python manage.py loaddata inventory/fixtures/items_initial_data.json
echo "Creating superuser..."
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('$SUPERUSER_NAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')"
