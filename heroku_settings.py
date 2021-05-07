import django_heroku

django_heroku.settings(locals())
options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)