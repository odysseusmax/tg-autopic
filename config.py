import os

class Config:
    USER_TOKEN = os.environ.get("USER_TOKEN", None)

    API_ID = int(os.environ.get("APP_ID"))

    API_HASH = os.environ.get("API_HASH", None)
    
    SAVE_TO_CHNL = int(os.environ.get("SAVE_TO_CHNL"))
