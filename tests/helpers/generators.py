import uuid as uuid_pkg

from sqlalchemy.orm import Session

from src.app import models
from src.app.core.security import get_password_hash
from tests.conftest import fake


def create_user(db: Session, password: str = None) -> models.SampleUser:
    _user = models.SampleUser(
        name=fake.name(),
        username=fake.user_name(),
        email=fake.email(),
        hashed_password=get_password_hash(password or fake.password()),
    )

    db.add(_user)
    db.commit()
    db.refresh(_user)

    return _user

