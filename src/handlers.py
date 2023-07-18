from vk_api.longpoll import Event, VkEventType

from db import session
from db.models import User
from services import api
from services.commands import COMMANDS, unknown_command


def _save_new_user(user_id: int) -> User | None:
    data = api.get_user(user_id)
    if not data:
        return

    home_town = data.get("home_town")
    home_town_id = api.get_city(home_town) if home_town else None
    user = User(vk_id=user_id, home_town_id=home_town_id, **data).save()
    return user


def message_handler(event: Event) -> None:
    # not answering to not user
    if not event.user_id:
        return

    # save user if doesn't exists
    if session.query(User).filter(User.vk_id == event.user_id).first() is None:
        _save_new_user(event.user_id)

    COMMANDS.get(event.message.lower(), unknown_command)(event)


HANDLERS = {
    VkEventType.MESSAGE_NEW: message_handler,
}


def event_handler(event: Event) -> None:
    if event.to_me:
        HANDLERS.get(event.type, lambda _: None)(event)


__all__ = ["HANDLERS", "event_handler"]
