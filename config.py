import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'es']
    VAPID_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQg6nDgKZZsxcdlIYM4
Ds3DWAY/U4Wp0y+aYmHlE17tF0qhRANCAAR9DC2EPalpn1o3byRMXieIlsxtDiim
41rscuCMDmEQCOpK8/mUbAvCpNb/7HgD6h7Y2dEA4JltR/4RJ1IcMkO1
-----END PRIVATE KEY-----"""
    VAPID_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEfQwthD2paZ9aN28kTF4niJbMbQ4o
puNa7HLgjA5hEAjqSvP5lGwLwqTW/+x4A+oe2NnRAOCZbUf+ESdSHDJDtQ==
-----END PUBLIC KEY-----"""
    VAPID_CLAIMS = {
        'sub': 'mailto:your-email@example.com'
    }
