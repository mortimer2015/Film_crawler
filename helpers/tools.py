# -*- coding: utf-8 -*-
# author: hunter
import os
from apps import settings


def spider_get_data_path(file_name='default', data_dir=settings.DATA_DIR):
    # this function should run in some file thant in "apps/spiders" dir.
    if not data_dir:
        data_dir = os.path.abspath(os.path.join(os.getcwd(), '../..'))
    file_path = os.path.join(data_dir, 'data', '{}.txt'.format(file_name))
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass
    return file_path
