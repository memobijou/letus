# letus
1. Install docker
2. From root project run "docker-compose up -d"
3. Project runs on "127.0.0.1:8000"
#
Environment variables (only for production and staging):

Production:
DJANGO_SETTINGS_MODULE=letus.settings.production.settings

Staging:
DJANGO_SETTINGS_MODULE=letus.settings.staging.settings
