from data_models.common_db import engine


def create_table(table_obj):

    try:
        table_obj.__table__.drop(bind=engine, checkfirst=True)
        table_obj.__table__.create(bind=engine)
        return {'status': 1, 'msg': ''}

    except Exception as e:
        return {'status': 0, 'msg': e}


def check_status(status):

    if status['status'] == 0:
        print(status['msg'])
        exit(1)
    else:
        pass
