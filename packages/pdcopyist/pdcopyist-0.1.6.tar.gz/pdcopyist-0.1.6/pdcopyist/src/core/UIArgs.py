

from pdcopyist.src.helper.utils import CanJson
from pdcopyist.src.core import Proxy
from typing import Callable, Dict, Iterable
import sys


class Content(CanJson):
    def __init__(self, title: str, type: str, var_name: str, type_id: str, enable=True, source=None, defaultValue=None) -> None:
        self.title = title
        self.type = type
        self.type_id = type_id
        self.var_name = var_name
        self.enable = enable
        self.source = source
        self.defaultValue = defaultValue


class AbcArgs(object):
    """
    docstring
    """
    pass

    m_type_id = 0
    m_id_type_mapping = {}

    @staticmethod
    def setup_id(class_name: str):
        AbcArgs.m_type_id += 1
        id = str(AbcArgs.m_type_id)
        AbcArgs.m_id_type_mapping[id] = class_name
        return id

    @staticmethod
    def extract_value(content_dict: Dict):
        type_id = content_dict['content']['type_id']
        class_name = AbcArgs.m_id_type_mapping[type_id]
        ct = getattr(sys.modules[__name__], class_name)
        return ct.extract_value(content_dict['content'], content_dict['input'])

    def __init__(self, title, var_name=None, enable=True, default=None, required=True, to_content_overwrite: Callable = None) -> None:
        self.title = title
        self.default = default
        self.required = required
        self.var_name: str = var_name
        self.enable = enable
        self.to_content_overwrite = to_content_overwrite

    def set_var_name(self, var_name) -> 'AbcArgs':
        self.var_name = var_name
        return self

    def to_content(self) -> Content:
        raise NotImplementedError

    def to_rule(self):
        raise NotImplementedError


class ColumnSelect(AbcArgs):

    m_type_id = AbcArgs.setup_id('ColumnSelect')

    @staticmethod
    def extract_value(content_dict: Dict, input):
        """
        docstring
        """
        pass

    def __init__(self, title, var_name=None, enable=True, default=None, required=True, to_content_overwrite: Callable = None) -> None:
        super().__init__(title, var_name=var_name, enable=enable, default=default,
                         required=required, to_content_overwrite=to_content_overwrite)

    def to_content(self) -> Content:
        ct = Content(self.title, 'select', self.var_name, self.m_type_id, enable=self.enable,
                     source='data_columns', defaultValue=self.default)
        return ct

    def to_rule(self):
        return [{'required': self.required, 'message': '必需选择一列', 'trigger': 'change'}]


class Input(AbcArgs):

    m_type_id = AbcArgs.setup_id('Input')

    @staticmethod
    def extract_value(content_dict: Dict, input):
        return input

    def __init__(self, title, var_name=None, placeholder=None, enable=True, default=None, required=True, to_content_overwrite: Callable = None) -> None:
        super().__init__(title, var_name=var_name, enable=enable, default=default,
                         required=required, to_content_overwrite=to_content_overwrite)
        self.placeholder = placeholder

    def to_content(self) -> Content:
        if self.to_content_overwrite:
            return self.to_content_overwrite()

        ct = Content(self.title, 'input', self.var_name, self.m_type_id, enable=self.enable,
                     defaultValue=self.default)

        ct.placeholder = self.placeholder
        return ct

    def to_rule(self):
        return [{'required': self.required, 'message': '请输入内容', 'trigger': 'blur'}]


class Select(AbcArgs):

    m_type_id = AbcArgs.setup_id('Select')

    @staticmethod
    def extract_value(content_dict: Dict, input):
        source = content_dict['source']
        return source[input]['text']

    def __init__(self, title, source, var_name=None, default=None, required=True) -> None:
        super().__init__(title, var_name=var_name, default=default, required=required)

        if isinstance(source, Iterable):
            source = [{'value': i, 'text': str(v)}
                      for i, v in enumerate(source)]
        self.source = source

    def to_content(self) -> Content:
        if self.to_content_overwrite:
            return self.to_content_overwrite()

        ct = Content(self.title, 'select', self.var_name, self.m_type_id, enable=self.enable,
                     source=self.source, defaultValue=self.default)
        return ct

    def to_rule(self):
        return [{'required': self.required, 'message': '必需选择一项', 'trigger': 'change'}]


class ColumnWithTypeSelect(AbcArgs):

    m_type_id = AbcArgs.setup_id('ColumnWithTypeSelect')

    @staticmethod
    def extract_value(content_dict: Dict, input):
        pass

    def __init__(self, title, var_name=None, default=None, required=True) -> None:
        super().__init__(title, var_name=var_name, default=default, required=required)

    def get_value(self, index: int):
        df = Proxy.ProxyManager.get().get_last_df_cache()
        col = str(df.columns[index])
        return col

    def to_content(self) -> Content:
        df = Proxy.ProxyManager.get().get_last_df_cache()
        cols = [f'{name}({t})' for name, t in zip(df.columns, df.dtypes)]

        source = [{'value': i, 'text': str(v)}
                  for i, v in enumerate(cols)]

        ct = Content(self.title, 'select', self.var_name, self.m_type_id, enable=self.enable,
                     source=source, defaultValue=self.default)
        return ct

    def to_rule(self):
        return [{'required': self.required, 'message': '请输入内容', 'trigger': 'blur'}]


class Switch(AbcArgs):

    m_type_id = AbcArgs.setup_id('Switch')

    @staticmethod
    def extract_value(content_dict: Dict, input):
        return input

    def __init__(self, title, var_name=None, default=None, required=True) -> None:
        super().__init__(title, var_name=var_name, default=default, required=required)

    def to_content(self) -> Content:
        if self.to_content_overwrite:
            return self.to_content_overwrite()

        ct = Content(self.title, 'switch', self.var_name, self.m_type_id, enable=self.enable,
                     defaultValue=self.default)
        return ct

    def to_rule(self):
        return [{'required': self.required, 'message': '请选中一项', 'trigger': 'change'}]
