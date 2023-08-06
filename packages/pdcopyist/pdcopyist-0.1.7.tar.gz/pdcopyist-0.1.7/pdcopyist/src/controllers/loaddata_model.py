

from pdcopyist.src.core.MethodCall import ArgActor
from pdcopyist.src.core import Proxy
from werkzeug.datastructures import FileStorage
from pdcopyist.src.core import UIArgs
from pdcopyist.src.core.UIArgs import AbcArgs, Content
from pdcopyist.src.helper.utils import CanJson
from typing import List


class DataArgs(CanJson):

    def __init__(self, model_type) -> None:
        self.model_type = model_type.__name__
        self.contents: List[Content] = []

    def append_arg(self, args: AbcArgs):
        self.contents.append(args.to_content())


class UIJsonModel(object):

    @staticmethod
    def get_model(file: FileStorage, file_ext: str) -> 'UIJsonModel':
        if file_ext in ['xlsx', 'xls', 'xlsm']:
            return ExcelUIJsonModel(file, file_ext)

        if file_ext in ['csv']:
            return CsvUIJsonModel(file, file_ext)

        if file_ext in ['feather']:
            return FeatherUIJsonModel(file, file_ext)

        raise Exception('not support file')

    def __init__(self, file: FileStorage, file_ext: str) -> None:
        self.file = file
        self.file_ext = file_ext

    def handler(self, caller: Proxy.CallerProxy, file: FileStorage, file_ext: str, **kwargs):
        raise NotImplementedError

    def to_args(self) -> DataArgs:
        raise NotImplementedError


class ExcelUIJsonModel(UIJsonModel):

    s_engine_map = {
        'xls': 'xlrd',
        'xlsx': 'openpyxl',
        'xlsm': 'openpyxl'
    }

    def __init__(self, file, file_ext: str) -> None:
        super().__init__(file, file_ext)

    def _get_sheet_names(self, file):
        import pandas as pd
        xl = pd.ExcelFile(file)
        return xl.sheet_names

    def to_args(self) -> DataArgs:
        pass
        da = DataArgs(ExcelUIJsonModel)
        da.append_arg(UIArgs.Input(
            '文件名：', enable=False, default=self.file.filename))
        da.append_arg(UIArgs.Input('后缀：', enable=False, default=self.file_ext))
        da.append_arg(UIArgs.Select(
            '选择工作表：', self._get_sheet_names(self.file), var_name='sheet_name'))

        return da

    def handler(self, caller: Proxy.CallerProxy, file: FileStorage, file_ext: str, **kwargs):
        if file_ext in self.s_engine_map:
            kwargs['engine'] = self.s_engine_map[file_ext]

        with caller.with_cmd('加载数据') as cmd:
            cmd.create_statement('pd', 'df')
            getattr(caller, 'read_excel')(
                ArgActor(file, str(file.filename)), **kwargs)


class CsvUIJsonModel(UIJsonModel):

    def __init__(self, file, file_ext: str) -> None:
        super().__init__(file, file_ext)

    def to_args(self) -> DataArgs:
        pass
        da = DataArgs(CsvUIJsonModel)
        da.append_arg(UIArgs.Input(
            '文件名：', enable=False, default=str(self.file)))
        da.append_arg(UIArgs.Input('后缀：', enable=False, default=self.file_ext))
        da.append_arg(UIArgs.Select(
            '编码：', source=['utf8', 'gb2312'], var_name='encoding'))

        return da

    def handler(self, caller: Proxy.CallerProxy, file: FileStorage, file_ext: str, **kwargs):
        with caller.with_cmd('加载数据') as cmd:
            cmd.create_statement('pd', 'df')
            getattr(caller, 'read_csv')(
                ArgActor(file, str(file.filename)), **kwargs)


class FeatherUIJsonModel(UIJsonModel):

    def __init__(self, file, file_ext: str) -> None:
        super().__init__(file, file_ext)

    def to_args(self) -> DataArgs:
        pass
        da = DataArgs(FeatherUIJsonModel)
        da.append_arg(UIArgs.Input(
            '文件名：', enable=False, default=str(self.file)))
        da.append_arg(UIArgs.Input('后缀：', enable=False, default=self.file_ext))

        return da

    def handler(self, caller: Proxy.CallerProxy, file: FileStorage, file_ext: str, **kwargs):
        with caller.with_cmd('加载数据') as cmd:
            cmd.create_statement('pd', 'df')
            getattr(caller, 'read_feather')(
                ArgActor(file, str(file.filename)), **kwargs)
