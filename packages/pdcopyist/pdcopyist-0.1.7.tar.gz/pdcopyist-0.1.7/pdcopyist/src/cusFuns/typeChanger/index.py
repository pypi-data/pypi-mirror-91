from pdcopyist.src.cusFuns.core.DecoratorFuns import dt_handle_func, dt_args, dt_source_code
from pdcopyist.src.core import UIArgs as ty
import pandas as pd


m_types_select = ['str', 'int']
m_col_with_type_select = ty.ColumnWithTypeSelect('列：')


def generate_code(*args, **kwargs):
    col = f"'{m_col_with_type_select.get_value(kwargs['col'])}'"
    type_value = f"'{m_types_select[kwargs['type']]}'"
    return f'''df[{col}] = df[{col}].astype({type_value})'''


@dt_source_code(generate_code)
@dt_handle_func('列类型转换')
@dt_args(col=m_col_with_type_select, type=ty.Select('类型：', source=m_types_select))
def change_column_type(df: pd.DataFrame, col: str, type: str):
    df[col] = df[col].astype(type)
    return df
