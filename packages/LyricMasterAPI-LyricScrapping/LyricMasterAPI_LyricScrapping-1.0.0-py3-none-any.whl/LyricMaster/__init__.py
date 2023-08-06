# -*- coding: utf-8 -*-

"""
LyricMaster API
~~~~~~~~~~~~~~~

A basic API for LyricMaster API Discord Bot

:copyright: (c) 2020 LyricMaster
:license: MIT

"""

__title__ = 'LyricMasterAPI'
__author__ = 'proguy914629'
__license__ = 'MIT',
__copyright__ = 'Copyright 2020 LyricMaster'
__version__ = "1.0.0"

from .lyric import LyricMaster, LyricMasterException
from .error import (
    ScrappingError,
    #TranslateError,
    #CaptchaError,
    SongNameNotFound,
    LyricMasterException,
    SongError
)