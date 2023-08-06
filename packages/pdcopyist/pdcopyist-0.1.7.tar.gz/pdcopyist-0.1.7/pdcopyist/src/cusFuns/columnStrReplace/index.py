from pdcopyist.src.cusFuns.core.DecoratorFuns import dt_handle_func, dt_args, dt_source_code
from pdcopyist.src.core import UIArgs as ty
import pandas as pd


m_col_with_type_select = ty.ColumnWithTypeSelect('目标列：')


def generate_code(*args, **kwargs):
    col_name = f"'{m_col_with_type_select.get_value(kwargs['col_name'])}'"
    to_replace = kwargs['to_replace']
    value = kwargs['value']
    return f'''df[{col_name}] = df[{col_name}].str.replace('{to_replace}','{value}')'''


@dt_source_code(generate_code)
@dt_handle_func('列内容替换')
@dt_args(col_name=m_col_with_type_select,
         to_replace=ty.Input('查找内容：', placeholder='输入你需要查找的目标内容'),
         value=ty.Input('替换成：', placeholder='输入替换的内容'))
def str_replace(df: pd.DataFrame, col_name: str, to_replace, value):
    df[col_name] = df[col_name].str.replace(to_replace, value)
    return df
