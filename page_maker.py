# coding: utf-8

from __future__ import absolute_import
import os

from lxml.html import tostring, fromstring
import macros


class Page(object):
    def __init__(self):
        self.html = """<html><head><title>Search Diff</title>

        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-11">
                    <table class="table table-bordered table-hover">
                        </table>
                </div>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>


</body></html>"""

    def add_sheet(self, s):
        outer_tree = fromstring(self.html)
        tag = outer_tree.find_class("table table-bordered table-hover")
        tag[0].extend([s.to_ele()])
        self.html = tostring(outer_tree)

    def get_html(self):
        return self.html

    def save_html(self):
        files = os.listdir(macros.html_path.get())
        max_id = 0
        file_id = 0
        for file in files:
            if file.startswith(macros.FILE_PREFIX):
                try:
                    file_id = int(file.split(macros.FILE_PREFIX)[-1].split(".html")[0])
                except:
                    pass
            if file_id > max_id:
                max_id = file_id
        file_name = macros.FILE_FORMAT.format(max_id + 1)
        file_path = os.path.join(macros.html_path.get(), file_name)
        with open(file_path, 'wb') as f:
            f.write(self.get_html())


class Sheet2Html(object):
    class Element(object):
        def __init__(self, val, style, row_span=1, col_span=1):
            self.val = val
            self.style = style
            if row_span == 0:
                row_span = 1
            if col_span == 0:
                col_span = 1
            self.row_span = row_span
            self.col_span = col_span
            if style is not None:
                self.style = {
                    'class': style
                }

    def __init__(self):
        self.sheet = [[(i, j) for j in range(256)] for i in range(256)]
        self.max_line = -1
        self.max_col = -1

    @staticmethod
    def _flatten(sheet):
        r = []
        for i in sheet:
            r.extend(i)
        return r

    def _get_target(self, start_pos, end_pos=None):
        if end_pos is None:
            end_pos = (start_pos[0] + 1, start_pos[1] + 1)
        else:
            end_pos = (end_pos[0] + 1, end_pos[1] + 1)
        self.max_line = max(self.max_line, end_pos[0] - 1)
        self.max_col = max(self.max_col, end_pos[1] - 1)

        line_slice = slice(start_pos[0], end_pos[0])
        col_slice = slice(start_pos[1], end_pos[1])
        target = self._flatten([_[col_slice] for _ in self.sheet[line_slice]])
        return target

    def write_one(self, val, start_pos, end_pos=None, style=None):
        target = self._get_target(start_pos, end_pos)
        for pos in target:
            self.sheet[pos[0]][pos[1]] = None
        for pos in target:
            self.sheet[pos[0]][pos[1]] = self.Element(val, style, target[-1][0] - target[0][0] + 1, target[-1][1] - target[0][1] + 1)
            break

    def write_list(self, list_val, start_pos, end_pos, style=None):
        target = self._get_target(start_pos, end_pos)
        for i, pos in enumerate(target):
            if style is not None:
                s = style[i]
            else:
                s = None
            self.sheet[pos[0]][pos[1]] = self.Element(list_val[i], s)

    @staticmethod
    def new_element(tag, val="", attribute=None, style=None):
        ele = fromstring("<{}>{}</{}>".format(tag, val, tag))
        if attribute is not None:
            for k, v in attribute.items():
                ele.set(k, v)
        if style is not None:
            for k, v in style.items():
                ele.set(k, v)
        return ele

    def to_ele(self):
        tbody = self.new_element("tbody")
        trs = []
        for i, line in enumerate(self.sheet):
            tr = self.new_element("tr")
            child = []
            for j, col in enumerate(line):
                if isinstance(col, self.Element):
                    th = self.new_element("th", col.val, dict(rowspan=str(col.row_span), colspan=str(col.col_span)), style=col.style)
                    child.append(th)
                    continue
                if col is not None and (isinstance(col, tuple) and col[0] <= self.max_line and col[1] <= self.max_col):
                    th = self.new_element("th")
                    child.append(th)
            if child:
                tr.extend(child)
                trs.append(tr)
        if trs:
            tbody.extend(trs)
        return tbody


if __name__ == '__main__':
    sheet = Sheet2Html()
    sheet.write_one("title", (0, 0), style='table-danger')
    sheet.write_one("nihao", (0, 1), (0, 2))
    sheet.write_one("wohao", (1, 0))
    sheet.write_one("wohao2", (1, 1))
    page = Page()
    page.add_sheet(sheet)
    print(page.get_html())
    print(page.save_html())
