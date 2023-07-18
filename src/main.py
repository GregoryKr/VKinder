import sys

from handlers import event_handler
from services import api
from db.common import create_tables


def event_loop():
    for event in api.longpoll.listen():
        event_handler(event)

def vkinder():
    try:
        event_loop()
    except KeyboardInterrupt:
        exit()


COMMANDS = {
    "vkinder": vkinder,
    "create_db": create_tables
}

def main():
    args = sys.argv
    if len(args) == 2:
        command = args[-1]
    else:
        command = "vkinder"

    COMMANDS[command]()

if __name__ == "__main__":
    main()
