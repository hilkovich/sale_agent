from models.data import Data
import datetime


def save_input_data(tg_id, input_data: str, session):
    data_add = Data(
        user_id=tg_id,
        request_date=datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
        input_data=input_data,
        output_data=None,
    )
    session.add(data_add)
    session.commit()
    session.close()
    return data_add.id


def save_output_data(session, output_data, data_id, tg_id):
    data = session.query(Data).filter(Data.user_id == tg_id, Data.id == data_id).first()
    data.output_data = output_data
    session.commit()
    session.close()
