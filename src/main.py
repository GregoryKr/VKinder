from src.handlers import event_handler
from src.services import api


def event_loop():
    for event in api.longpoll.listen():
        event_handler(event)


def main():
    try:
        event_loop()
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    main()
