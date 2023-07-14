import secrets

class Config(object):
    SECRET_KEY = secrets.token_bytes(32)

class MainConfig(Config):
    DB_PATH = "default"

# For unit and system tests
class TestingConfig(Config):
    DB_PATH = "test/test.db"