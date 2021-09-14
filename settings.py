from os import environ

SESSION_CONFIGS = [
    dict(
        name='Tratamiento_linea_base_contrato_informal',
        display_name="Normas Sociales - Linea Base Contrato Informal",
        num_demo_participants=3,
        app_sequence=['experimiento_1'],
        tipo="linea_base_contrato_informal"
    ),
    dict(
        name='Tratamiento_linea_base_contrato_formal',
        display_name="Normas Sociales - Linea Base Contrato Formal",
        num_demo_participants=3,
        app_sequence=['experimiento_1'],
        tipo="linea_base_contrato_formal"
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1, participation_fee=0.00, doc=""
)

ROOT_URLCONF = 'urls'

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ALLOWED_HOSTS = ['*']

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""
# don't share this with anybody.
SECRET_KEY = 'gu0-t&wo*2un8j93kesnb5!6t2=py8uap9d4qyl)y@u(mp-&w-'

INSTALLED_APPS = ['otree']
