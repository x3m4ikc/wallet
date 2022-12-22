"""App`s Config for Settings.py"""
from django.apps import AppConfig


class TestsConfig(AppConfig):
    """Short name for app`s config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tests'
