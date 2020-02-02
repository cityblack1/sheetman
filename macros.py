# coding: utf-8
import os


_HTML_PATH = os.path.join(os.path.dirname(__file__), 'htmls')

FILE_PREFIX = "_cityblack_"
FILE_FORMAT = FILE_PREFIX + "{}.html"

class HTMLPath(str):
    path = _HTML_PATH

    def set(self, path):
        self.path = path

    def get(self):
        return self.path

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path


html_path = HTMLPath()
