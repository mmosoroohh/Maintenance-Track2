import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configuration for Testing with seperate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://mmosoroohh:test123@localhost:5432/testmain'
    DEBUG = True

class StagingConfig(Config):
    """Configuratin for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configuration for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
