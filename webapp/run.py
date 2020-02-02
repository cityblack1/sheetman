# coding: utf-8

import os
import logging
import tornado.ioloop
import tornado.web
from tornado.log import enable_pretty_logging, LogFormatter
from macros import html_path

BASE_LOG_PATH = os.path.join(os.path.dirname(__file__), 'log')
ACCESS_LOG_PATH = os.path.join(BASE_LOG_PATH, 'tornado.access.log')
APP_LOG_PATH = os.path.join(BASE_LOG_PATH, 'tornado.application.log')
GEN_LOG_PATH = os.path.join(BASE_LOG_PATH, 'tornado.general.log')

_redis_cli = None


class _Config(object):
    use_local_file = True

    use_redis = False
    redis_url = None

    def use_redis_(self, url=None, **kwargs):
        if url is None:
            from redis import Redis
            _redis_cli = Redis()
        else:
            from redis import from_url
            _redis_cli = from_url(url, **kwargs)

    def use_local_filesystem_(self, path=None):
        if path is not None:
            html_path.set(path)


_config = _Config()


def use_local_filesystem(path=None):
    _config.use_local_filesystem_(path)


def use_redis(redis_url, **redis_config):
    _config.use_redis_(redis_url, **redis_config)


def _set_log():
    enable_pretty_logging()
    fmt = LogFormatter()
    for logger_name in ['tornado.access', 'tornado.application', 'tornado.general']:
        logger = logging.getLogger(logger_name)
        log_file_path = os.path.join(BASE_LOG_PATH, logger_name + '.log')
        log_handler = logging.FileHandler(log_file_path)
        log_handler.setFormatter(fmt)
        logger.addHandler(log_handler)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def _make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


def run():
    _set_log()
    app = _make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    run()
