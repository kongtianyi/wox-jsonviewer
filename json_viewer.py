#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json
import webbrowser
import pyperclip
import re
import os
from typing import List
from enum import Enum
from LanguageBinding.wox import Wox, WoxAPI

RESULT_TEMPLATE = {
    'Title': '{}',
    'SubTitle': None,
    'IcoPath': 'ui/icon.png',
    "JsonRPCAction": {
        "method": "create_file_and_open",
        "parameters": ['{}'],
        "dontHideAfterAction": False
    }
}

PREDICT_TEMPLATE = {
    'Title': '{}',
    'SubTitle': None,
    'IcoPath': 'ui/icon.png',
    "JsonRPCAction": {
        "method": "change_query",
        "parameters": ['{}'],
        "dontHideAfterAction": True
    }
}

ERROR_TEMPLATE = {
    'Title': '{}',
    'SubTitle': None,
    'IcoPath': 'ui/icon.png',
}

PYTHON_JSON_TYPE_MAP = {
    "dict": "object",
    "list": "array",
    "tuple": "array",
    "set": "array",
    "str": "string",
    "unicode": "string",
    "int": "number",
    "float": "number",
    "bool": "bool",
    "NoneType": "null"
}


class QueryType(Enum):
    SIMPLE = 0
    SEARCH = 1


class Main(Wox):
    def query(self, key):
        result = []
        query_type, paths = self.parse_input(key)

        clipboard_text = str(pyperclip.paste())
        text = self.parse_text(clipboard_text.strip())

        json_dict = self.load_json(text)
        if json_dict is None:
            self.add_item(result, "can not read json from clipboard", template=ERROR_TEMPLATE)
            return result

        if query_type == QueryType.SIMPLE:
            self.add_item(result, text, text, subtitle="following rows are key-value pairs of clipboard object")

        for i in range(len(paths)):
            json_dict = self.load_json(text)
            for k in sorted(json_dict.keys()):
                v = json_dict[k]
                if i != len(paths) - 1:
                    # 中间的path都是整个的单词
                    if k.lower() == paths[i].lower():
                        text = v
                        break
                else:
                    # 最后一个path模糊搜索
                    if k.lower().find(paths[i].lower()) == -1:
                        continue
                    if k.lower() != paths[i].lower():
                        self.add_item(result,
                                      title=k + self.get_type_name(v) + ": " + self.generate_output(v),
                                      output=self.build_predict_output(k, paths),
                                      template=PREDICT_TEMPLATE,
                                      subtitle="press enter to fill in the search box")
                    else:
                        text = v
                        self.add_item(result,
                                      title=k + self.get_type_name(v) + ": " + self.generate_output(v),
                                      output=self.generate_output(v),
                                      template=RESULT_TEMPLATE,
                                      subtitle="press enter to show in web browser")

        if len(result) == 0:
            self.add_item(result, "path error", template=ERROR_TEMPLATE)

        return result

    def build_predict_output(self, k, paths):
        path = ">".join(paths[:-1])
        if path.strip() != "":
            path = path + ">"
        return "json " + path + k

    def add_item(self, result: List[dict], title, output=None, template=None, subtitle=None):
        if template is None:
            template = RESULT_TEMPLATE
        tmp_template = copy.deepcopy(template)
        tmp_template['Title'] = tmp_template['Title'].format(title)
        if subtitle is not None:
            tmp_template['SubTitle'] = tmp_template['SubTitle'] = subtitle
        if 'JsonRPCAction' in tmp_template.keys():
            tmp_template['JsonRPCAction']['parameters'][0] = str(output)
        result.append(tmp_template)

    def parse_input(self, key):
        if key.strip() == "":
            return QueryType.SIMPLE, [""]
        return QueryType.SEARCH, key.strip().split('>')

    def parse_text(self, text):
        text = text.replace("\r\n", "").replace("\n", "").replace("\t", "")
        if text.startswith('\"'):
            # like "{\"a\": 1}"
            return eval(text)
        elif text.startswith("{\\\""):
            # like {\"a\": 1}
            return eval("\"" + text + "\"")
        else:
            # like {"a": 1}
            return text

    def load_json(self, input):
        if type(input) == dict:
            return input
        try:
            json_obj = json.loads(input)
        except Exception:
            return None
        return json_obj

    def generate_output(self, param, intent=None):
        if self.check_if_escape_json_dict(param):
            param = self.load_json(param)
        if type(param) is not str:
            return json.dumps(param, ensure_ascii=False, indent=intent)
        return param

    def check_if_escape_json_dict(self, data):
        if type(data) is not str:
            return False
        if not data.startswith('{'):
            return False
        try:
            json.loads(data)
        except Exception:
            return False
        return True

    def get_web_handle(self, browser_name):
        try:
            wb = webbrowser.get(using=browser_name)
        except webbrowser.Error:
            return None
        return wb

    def create_file_and_open(self, data):
        file_name = "data.json"
        with open("./" + file_name, mode='w') as f:
            f.write(data)
        current_path = os.getcwd()
        wb = self.get_web_handle('google-chrome')
        if wb is None:
            wb = self.get_web_handle('chrome')
        if wb is None:
            wb = self.get_web_handle('windows-default')
        wb.open(current_path + "/" + file_name)  # clean
        self.change_query("")

    def change_query(self, text):
        WoxAPI.change_query(text)

    def hide_app(self):
        WoxAPI.hide_app()

    def get_type_name(self, item):
        type_str = str(type(item))
        pattern = re.compile("\'(.*?)\'")
        py_type_name = pattern.search(type_str).group()[1:-1]
        return '(' + PYTHON_JSON_TYPE_MAP.get(py_type_name, 'unknown') + ')'


if __name__ == '__main__':
    Main()
