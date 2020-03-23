class Config:
    DEBUG = True
    SECRET_KEY= "secret_key"
    SQLALCHEMY_DATABASE_URI = r"sqlite:///foodapp/fooddelivery.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False