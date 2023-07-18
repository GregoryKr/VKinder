from vk_api.longpoll import Event

from db import session
from db.models import User
from services import api
from services.commands.search import search_command


def hello_command(event: Event):
    user: User = session.query(User).filter(User.vk_id == event.user_id).one()
    api.send_message(event.user_id, f"Hellloooo, {user.full_name}")


def bye_command(event: Event):
    user: User = session.query(User).filter(User.vk_id == event.user_id).one()
    api.send_message(event.user_id, f"Byee, {user.full_name}")


def unknown_command(event: Event):
    api.send_message(event.user_id, "Не известная команда")


COMMANDS = {
    "привет": hello_command,
    "пока": bye_command,
    "поиск": search_command,
}


__all__ = ["COMMANDS", "unknown_command"]
