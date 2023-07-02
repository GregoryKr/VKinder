from vk_api.longpoll import Event

from src.db import session
from src.db.models import User
from src.services import api
from src.services.commands import COMMANDS, unknown_command


def _save_new_user(user_id: int) -> User:
    data = api.get_user(user_id)
    home_town = data.get("home_town")
    home_town_id = api.get_city(home_town) if home_town else None
    user = User(vk_id=user_id, home_town_id=home_town_id, **data).save()
    return user


def message_handler(event: Event) -> None:
    # not answering to not user
    if not event.from_user:
        return

    # save user if doesn't exists
    if session.query(User).filter(User.vk_id == event.user_id).first() is None:
        _save_new_user(event.user_id)

    COMMANDS.get(event.message.lower(), unknown_command)(event)
