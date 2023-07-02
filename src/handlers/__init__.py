from vk_api.longpoll import Event, VkEventType


from src.handlers.messages import message_handler


HANDLERS = {
    VkEventType.MESSAGE_NEW: message_handler,
}


def event_handler(event: Event) -> None:
    if event.to_me:
        HANDLERS.get(event.type, lambda _: None)(event)


__all__ = ["HANDLERS", "event_handler"]
