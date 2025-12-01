import os

class Config:
    SECRET_KEY = "your-super-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join("static", "uploads")
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "zip", "docx"}
    PER_PAGE = 6
