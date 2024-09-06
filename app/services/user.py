from models.user import User


def user_add(session, user_data):
    user = User(
        email=user_data.email,
        name=user_data.name,
        company_name=user_data.company_name,
        tg_id=user_data.tg_id,
    )
    session.add(user)
    session.commit()


def get_user_by_email(session, email):
    user = session.query(User).filter(User.email == email).first()
    if user:
        return user
    else:
        return None


def get_user_by_tg(session, tg_id):
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user:
        return user
    else:
        return None
