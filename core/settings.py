from pathlib import Path
import os
import dj_database_url # Importe no topo

# Carrega variáveis de ambiente de um arquivo .env (apenas para desenvolvimento local)
# Em produção (Railway), as variáveis são injetadas diretamente no ambiente.
# Para isso, instale: pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

APP_VERSION = '1.4.2'

# --- CONFIGURAÇÕES DE SEGURANÇA ---
# A SECRET_KEY é lida da variável de ambiente. NUNCA a deixe no código.
SECRET_KEY = os.environ.get('SECRET_KEY_DJANGO')

# O modo DEBUG é desativado por padrão em produção.
# Ele só será 'True' se a variável de ambiente DEBUG for explicitamente 'True'.
DEBUG = os.environ.get('DEBUG') == 'True'

# --- CONFIGURAÇÕES DE REDE (HOSTS) ---
# Configuração dinâmica de ALLOWED_HOSTS para Railway.
ALLOWED_HOSTS = ['www.bookowl.com.br', 'bookowl.com.br']
RAILWAY_APP_HOSTNAME = os.environ.get('RAILWAY_APP_HOSTNAME')
if RAILWAY_APP_HOSTNAME:
    # Adiciona o domínio do Railway quando a variável estiver disponível
    ALLOWED_HOSTS.append(RAILWAY_APP_HOSTNAME)

# Se estiver em desenvolvimento, permita o host local.
if DEBUG:
    ALLOWED_HOSTS.append('127.0.0.1')
    ALLOWED_HOSTS.append('localhost')

# Adiciona o domínio do Railway à lista de origens CSRF confiáveis.
CSRF_TRUSTED_ORIGINS = []
if RAILWAY_APP_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_APP_HOSTNAME}" )
    CSRF_TRUSTED_ORIGINS.append(f"https://www.bookowl.com.br" )

# Força o redirecionamento para HTTPS em produção.
# A variável IS_HEROKU é um nome comum que o Railway também pode usar.
# Ou podemos simplesmente checar se DEBUG é False.
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Adicione para servir estáticos em dev sem collectstatic
    'django.contrib.staticfiles',
    'widget_tweaks',

    # My apps
    'User.apps.UserConfig',
    'Home',
    'library',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- Adicione aqui
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.app_version_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_USER_MODEL = 'User.CustomUser'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = '/auth/login'


# --- BANCO DE DADOS ---
# Configuração unificada que funciona tanto localmente quanto em produção.
# O Railway provê a variável DATABASE_URL automaticamente.
# Para o Supabase, você pode construir essa URL ou usar a que eles fornecem.
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            ssl_require=True # Força SSL para bancos de dados remotos
        )
    }
else:
    # Fallback para um banco de dados local (SQLite) se DATABASE_URL não estiver definida.
    # Isso facilita o desenvolvimento local sem precisar de um banco de dados externo.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- ARQUIVOS ESTÁTICOS (CSS, JavaScript, Images) ---
# Configuração para WhiteNoise servir os arquivos estáticos em produção.
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Onde o `collectstatic` irá copiar os arquivos para produção.

STATICFILES_DIRS = [
    BASE_DIR / 'static', # Onde o Django procura seus arquivos estáticos durante o desenvolvimento.
]

# Adiciona o motor de armazenamento do WhiteNoise.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
