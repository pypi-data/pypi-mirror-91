

import pandas as pd
from pdcopyist.src.core import Proxy
from typing import Callable, Iterable
from pdcopyist.src.cusFuns.core.UIModl import Content


class AbcArgs(object):
    """
    docstring
    """
    pass

    def __init__(self, title, default=None, required=True, to_content_overwrite: Callable = None) -> None:
        self.title = title
        self.default = default
        self.required = required
        self.var_name: str = None
        self.to_content_overwrite = to_content_overwrite

    def set_var_name(self, var_name) -> 'AbcArgs':
        self.var_name = var_name
        return self

    def to_content(self) -> Content:
        raise NotImplementedError

    def to_rule(self):
        raise NotImplementedError


class ColumnSelect(AbcArgs):

    def __init__(self, title, default=None, required=True) -> None:
        super().__init__(title, default=default, required=required)

    def to_content(self) -> Content:
        ct = Content(self.title, 'select', self.var_name,
                     source='data_columns', defaultValue=self.default)
        return ct

    def to_rule(self):
        return [{'required': self.required, 'message': '必需选择一列', 'trigger': 'change'}]


class Input(AbcArgs):

    def __init__(self, title, placeholder=None, default=None, required=True) -> None:
        super().__init__(title, default=default, required=required)
        self.placeholder = placeholder

    def to_content(self) -> Content:
        if self.to_content_overwrite:
            return self.to_content_overwrite()

        ct = Content(self.title, 'input', self.var_name,
                     defaultValue=self.default)
        return ct

    def to_rule(self):
        return [{'required': self.required, 'message': '请输入内容', 'trigger': 'blur'}]


class Select(AbcArgs):

    def __init__(self, title, source, default=None, required=True) -> None:
        super().__init__(title, default=default, required=required)

        if isinstance(source, Iterable):
            source = [{'value': i, 'text': str(v)}
                      for i, v in enumerate(source)]
        self.source = source

    def to_content(self) -> Content:
        if self.to_content_overwrite:
            return self.to_content_overwrite()

        ct = Content(self.title, 'select', self.var_name,
                     source=self.source, defaultValue=self.default)
        return ct

    def to_rule(self):
        return [{'required': self.required, 'message': '必需选择一项', 'trigger': 'change'}]


class ColumnWithTypeSelect(AbcArgs):

    def __init__(self, title, default=None, required=True) -> None:
        super().__init__(title, default=default, required=required)

    def get_value(self, index: int):
        df: pd.DataFrame = Proxy.ProxyManager.get().get_last_df_cache()
        col = str(df.columns[index])
        return col

    def to_content(self) -> Content:
        df: pd.DataFrame = Proxy.ProxyManager.get().get_last_df_cache()
        cols = [f'{name}({t})' for name, t in zip(df.columns, df.dtypes)]

        source = [{'value': i, 'text': str(v)}
                  for i, v in enumerate(cols)]

        ct = Content(self.title, 'select', self.var_name,
                     source=source, defaultValue=self.default)
        return ct

    def to_rule(self):
        return [{'required': self.required, 'message': '请输入内容', 'trigger': 'blur'}]


class Switch(AbcArgs):

    def __init__(self, title, default=None, required=True) -> None:
        super().__init__(title, default=default, required=required)

    def to_content(self) -> Content:
        if self.to_content_overwrite:
            return self.to_content_overwrite()

        ct = Content(self.title, 'switch', self.var_name,
                     defaultValue=self.default)
        return ct

    def to_rule(self):
        return [{'required': self.required, 'message': '请选中一项', 'trigger': 'change'}]
