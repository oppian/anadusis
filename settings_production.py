
DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'anadusis'              # Or path to database file if using sqlite3.
DATABASE_USER = 'anadusis'             # Not used with sqlite3.
DATABASE_PASSWORD = 'bewmen69'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

ADMINS = (
    ('Stephen Hartley', 'steve@oppian.com'),
    ('Matthew Jacobi', 'matt@oppian.com'),
    ('Lighthouse', 'ticket+oppian.37141-t3xa7ysc@lighthouseapp.com'),
)

# Default admin account and pass
# admin:dewnwerd7

MANAGERS = ADMINS
