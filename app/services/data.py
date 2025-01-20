from models.data import Data, Action
import datetime
import json


def save_input_data(user_id, input_data: str, session):
    data_add = Data(
        user_id=user_id,
        request_date=datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
        input_data=input_data,
        output_data=None,
    )
    session.add(data_add)
    session.commit()
    data_id = data_add.id
    session.close()
    return data_id


def save_output_data(session, output_data, data_id, user_id):
    data = (
        session.query(Data).filter(Data.user_id == user_id, Data.id == data_id).first()
    )
    data.output_data = json.dumps(output_data)
    session.commit()
    session.close()


def save_user_action(session, action_type, user_id):
    curr_act = Action(
        user_id=user_id,
        action_date=datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
        action_type=action_type,
    )
    session.add(curr_act)
    session.commit()
    session.close()
