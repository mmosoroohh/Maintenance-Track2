import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = "kasjdflkasldfkjal;dskjfla"
    DATABASE_NAME = "m_tracker"

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configuration for Testing with seperate test database."""
    TESTING = True
    DEBUG = True
    DATABASE_NAME = "m_tracker_test"

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
