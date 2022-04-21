# project/server/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""

    WTF_CSRF_ENABLED = True
    REDIS_URL = "redis://redis:6379/0"
    QUEUES = ["default"]


class DevelopmentConfig(BaseConfig):
    """Development configuration."""




class ProductionConfig(BaseConfig):
    """Testing configuration."""

