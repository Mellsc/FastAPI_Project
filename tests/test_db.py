from dataclasses import asdict
from sqlalchemy import select
from fast_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model = User) as time:
        user =  User(
            username='alice', password='secret', email='teste@test'
        )
    
    session.add(user)
    session.commit()

    user = session.scalar(
        select(User).where(User.username == "alice", User.email == "teste@test",
                            User.password == "secret")
    )

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time, }

