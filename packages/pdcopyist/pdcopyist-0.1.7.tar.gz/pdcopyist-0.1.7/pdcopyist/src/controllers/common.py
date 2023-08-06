import json
from pdcopyist.src.helper.utils import json_converter
from pdcopyist.src.dataModel.pandasCmd import PandasCmd
import flask
import pandas as pd


def to_json(obj):
    return flask.json.dumps(obj, default=json_converter)


def df2json(df: pd.DataFrame, head_tail_num=10):

    ret = None

    if len(df) > (head_tail_num * 2):
        ret = pd.concat([df.head(head_tail_num), df.tail(head_tail_num)])
    else:
        ret = df

    cmd = PandasCmd.from_df(df, ret)
    ret = flask.json.dumps(cmd, default=json_converter)
    return ret


def get_data_from_post():
    return json.loads(flask.request.get_data().decode())
