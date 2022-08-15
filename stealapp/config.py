class BaseConfig:
    SECRET_KEY = '69ja$ap1'
    ADMIN_EMAIL = 'erubaihechukwu@gmail.com'
class TestConfig(BaseConfig):
    ADMIN_EMAIL = 'test@yahoo.com'
class LiveConfig(BaseConfig):
    ADMIN_EMAIL = 'live@yahoo.com'