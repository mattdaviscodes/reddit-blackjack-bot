"""Configurations for Reddit bot."""

import os


class Config(object):
    """Base configuration."""
    USERNAME = 'blackjack_bot'
    PASSWORD = os.environ.get('PASSWORD')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    USER_AGENT = 'linux:blackjack_bot:v1.0 (by /u/Davism72)'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProdConfig(Config):
    """Production configuration."""
