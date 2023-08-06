
import json
from pdcopyist.src.core.UIArgs import Content, AbcArgs
from typing import List

from werkzeug.datastructures import FileStorage
from pdcopyist.src.controllers.loaddata_model import UIJsonModel
import flask
from flask import request, Blueprint
import pandas as pd
from pdcopyist.src.core.Proxy import ProxyManager
from pdcopyist.src.controllers import common

app = Blueprint('loaddata', __name__)


@app.route('/ui_args', methods=['post'])
def get_ui_args():
    '''
    根据文件后缀名，返回界面所需内容
    '''
    file: FileStorage = flask.request.files.get('file')
    ext = flask.request.form['ext']

    model = UIJsonModel.get_model(file, ext)
    ret = model.to_args()
    ret = common.to_json(ret)

    return ret


@app.route('/file', methods=['post'])
def upload_file():
    file: FileStorage = flask.request.files.get('file')

    ext = flask.request.form['ext']
    filename = flask.request.form['file_name']
    args = json.loads(flask.request.form['args'])
    kwargs = {
        a['content']['var_name']: AbcArgs.extract_value(a)
        for a in args['contents']
        if a['content']['var_name'] is not None}

    model = UIJsonModel.get_model(file, ext)

    px = ProxyManager.get()
    px.init_all_proxy()
    px.import_module()

    model.handler(px.pd_read_proxy, file, ext, **kwargs)

    px.read_data()
    return common.df2json(px.get_df_data())

    # todo:根据不同情况做处理
    # px = ProxyManager.get()
    # px.read_data(file, filename, ext, args)
    # return common.df2json(px.get_df_data())
