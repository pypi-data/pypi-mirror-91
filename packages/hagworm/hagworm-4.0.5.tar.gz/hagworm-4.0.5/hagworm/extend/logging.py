# -*- coding: utf-8 -*-

import logging

from datetime import timedelta

from hagworm.extend.base import Utils


class LogFileRotator:

    @classmethod
    def make(cls, _size=500, _time=r'00:00'):

        return cls(_size, _time).should_rotate

    def __init__(self, _size, _time):

        _size = _size * (1024 ** 2)
        _time = Utils.split_int(_time, r':')

        now_time = Utils.today()

        self._size_limit = _size
        self._time_limit = now_time.replace(hour=_time[0], minute=_time[1])

        if now_time >= self._time_limit:
            self._time_limit += timedelta(days=1)

    def should_rotate(self, message, file):

        file.seek(0, 2)

        if file.tell() + len(message) > self._size_limit:
            return True

        if message.record[r'time'].timestamp() > self._time_limit.timestamp():
            self._time_limit += timedelta(days=1)
            return True

        return False


DEFAULT_LOG_FILE_ROTATOR = LogFileRotator.make()


class LogInterceptor(logging.Handler):
    """日志拦截器
    """

    def emit(self, record):

        Utils.log.opt(
            depth=6,
            exception=record.exc_info
        ).log(
            record.levelname,
            record.getMessage()
        )


DEFAULT_LOG_INTERCEPTOR = LogInterceptor()


def init_logger(
        level, handler=None,
        file_path=None, file_rotation=DEFAULT_LOG_FILE_ROTATOR, file_retention=0xff,
        debug=False
):

    level = level.upper()

    if handler or file_path:

        Utils.log.remove()

        if handler:
            Utils.log.add(
                handler,
                level=level,
                enqueue=True,
                backtrace=debug,
            )

        if file_path:
            Utils.log.add(
                Utils.path.join(file_path, f'runtime_{{time}}_{Utils.getpid()}.log'),
                level=level,
                enqueue=True,
                backtrace=debug,
                rotation=file_rotation,
                retention=file_retention
            )

    else:

        Utils.log.level(level)

    logging.getLogger().addHandler(DEFAULT_LOG_INTERCEPTOR)
