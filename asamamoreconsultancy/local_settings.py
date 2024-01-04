
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv
load_dotenv()
import dotenv


dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-k!8lp%oh6#2=2e4fp_p=r+9eu7)c8s0i+t%39-k&5sff0od$-@'

DEBUG = True



STATICFILES_DIRS = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')