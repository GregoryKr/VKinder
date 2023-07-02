from vk_api.longpoll import Event, VkEventType

from src.db import session
from src.db.models import FoundUser, User
from src.services import api


AGE_RANGE = 5
SEARCH_FIELDS = (
    "age_from",
    "age_to",
    "sex",
    "city_id",
    "status",
    "hasphoto",
)


def ask_for_missing_fields(user: User) -> User:
    fields = ("home_town", "age")
    for field in fields:
        if getattr(user, field, None) is not None:
            continue
        api.send_message(user.vk_id, f"Напишите {field.replace('_', ' ').title()}")

        value = None
        for event in api.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                value = event.message or None
                break

        if value is not None and value.isdigit():
            value = int(value)

        setattr(user, field, value)
    user.save()
    return user


def save_home_town_id(user: User):
    home_town_id = api.get_city(user.home_town) if user.home_town else None
    user.home_town_id = home_town_id
    user.save()


def _search_command(user: User) -> FoundUser:
    found_user = api.search_users(
        age_from=user.age - AGE_RANGE,
        age_to=user.age + AGE_RANGE,
        # get opposite sex
        sex=(1 if user.sex == 2 else 2),
        city_id=user.home_town_id,
    )
    photos = api.get_photos(found_user["id"])
    photos.sort(
        key=lambda photo: photo["likes"]["count"] + photo["comments"]["count"],
        reverse=True,
    )
    photos = [f"photo{photo['owner_id']}_{photo['id']}" for photo in photos] or None
    if photos:
        photos = ",".join(photos)

    return FoundUser(
        vk_id=found_user["id"],
        photos=photos,
        first_name=found_user["first_name"],
        last_name=found_user["last_name"],
        user_id=user.id,
    ).save()


def search_command(event: Event) -> None:
    user: User = session.query(User).filter(User.vk_id == event.user_id).one()

    ask_for_missing_fields(user)
    if user.home_town_id is None:
        save_home_town_id(user)

    found_user = _search_command(user)
    api.send_message(
        event.user_id,
        (f"Встречайте {found_user.full_name}\n" f"https://vk.com/id{found_user.vk_id}"),
        attachment=found_user.photos,
    )
