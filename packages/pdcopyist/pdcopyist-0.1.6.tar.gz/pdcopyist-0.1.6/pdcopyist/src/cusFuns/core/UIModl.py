

from pdcopyist.src.core.UIArgs import Content
from typing import Dict, List

from pdcopyist.src.helper.utils import CanJson


class FunModel(CanJson):

    def __init__(self, fun_name: str) -> None:
        self.uid: str = None
        self.function_name = fun_name
        self.contents: List[Content] = []
        self.rules = {}

    def add_content(self, content: Content):
        self.contents.append(content)


class InputRet(object):

    def __init__(self, var_name: str, input: object) -> None:
        self.var_name = var_name
        self.input = input


class CusFunInputRet(object):

    @staticmethod
    def from_dict(data: Dict) -> 'CusFunInputRet':
        pass
        ret = CusFunInputRet()
        ret.uid = data['uid']

        cts = [InputRet(c['content']['var_name'], c['input'])
               for c in data['contents']]

        ret.contents = cts
        return ret

    def __init__(self) -> None:
        self.contents: List[InputRet] = []
        self.uid: str = ''
