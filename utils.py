from data_models.common_db import engine


def create_table(table_obj):

    try:
        table_obj.__table__.drop(bind=engine, checkfirst=True)
        table_obj.__table__.create(bind=engine)
        return

    except Exception as e:
        print(e)
        exit(-1)


