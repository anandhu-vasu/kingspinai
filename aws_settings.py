from pathlib import Path
import os
import subprocess
import ast


def get_environ_vars():
    completed_process = subprocess.run(
        ['/opt/elasticbeanstalk/bin/get-config', 'environment'],
        stdout=subprocess.PIPE,
        text=True,
        check=True
    )

    return ast.literal_eval(completed_process.stdout)

if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    env_vars = get_environ_vars()
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env_vars['RDS_DB_NAME'],
        'USER': env_vars['RDS_USERNAME'],
        'PASSWORD': env_vars['RDS_PASSWORD'],
        'HOST': env_vars['RDS_HOSTNAME'],
        'PORT': env_vars['RDS_PORT'],
    }
}
    
    
WEBHOOK_SITE ='https://kingspinai.eba-5ssf86gq.ap-south-1.elasticbeanstalk.com'
