import django_heroku
import dj_database_url

DATABASES['default'] = dj_database_url.config(conn_max_age=600,ssl_require=True)

django_heroku.settings(locals())
options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)