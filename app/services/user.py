from models.user import User
import datetime


def user_add(session, tg_id: int):
    user = User(
        tg_id=tg_id, created_on=datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    )
    session.add(user)
    session.commit()
    session.close()


def get_user_by_tg(session, tg_id: int):
    user = session.query(User).filter(User.tg_id == tg_id).first()
    session.close()
    if user:
        return user
    else:
        return None
