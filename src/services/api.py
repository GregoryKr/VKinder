from datetime import datetime

import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.utils import get_random_id

from src.db import session
from src.db.models import FoundUser
from src.settings import ACCESS_TOKEN, COMMUNITY_TOKEN

REQUIRED_FIELDS = (
    "city",
    "bdate",
    "sex",
    "home_town",
)


class VKinder:
    community = vk_api.VkApi(token=COMMUNITY_TOKEN)
    user = vk_api.VkApi(token=ACCESS_TOKEN)
    tools = vk_api.VkTools(ACCESS_TOKEN)
    longpoll = VkLongPoll(community)
    found_users = {"offset": 0, "count": 50, "users": []}

    def send_message(self, user_id: int, message: str, attachment: str | None = None):
        assert user_id is not None, ""
        self.community.method(
            "messages.send",
            {
                "user_id": user_id,
                "message": message,
                "attachment": attachment,
                "random_id": get_random_id(),
            },
        )

    def get_user(self, user_id: int) -> dict:
        data = self.user.method(
            "users.get", {"user_id": user_id, "fields": ",".join(REQUIRED_FIELDS)}
        )
        if not data:
            raise
        data = data[0]

        year = datetime.strptime(data["bdate"], "%d.%m.%Y").year
        age = datetime.now().year - year

        return dict(
            first_name=data["first_name"],
            last_name=data["last_name"],
            sex=data["sex"],
            home_town=data["home_town"],
            age=age,
        )

    def get_city(self, city_name: str) -> int | None:
        results = self.user.method(
            "database.getCities", {"country_id": 1, "need_all": 1, "q": city_name}
        )["items"]
        if not results:
            return None

        return results[0]["id"]

    def __get_new_found_user(self):
        user = self.found_users["users"].pop()
        if (
            session.query(FoundUser).filter(FoundUser.vk_id == user["id"]).first()
            is not None
        ):
            return self.__get_new_found_user()
        return user

    def search_users(
        self, status: int = 6, hasphoto: int = 0, is_closed: int = 0, **filters
    ) -> dict:
        if self.found_users["users"]:
            return self.found_users["users"].pop()
        self.found_users["offset"] += 1
        users = self.user.method(
            "users.search",
            dict(
                status=status,
                hasphoto=hasphoto,
                is_closed=is_closed,
                offset=self.found_users["offset"],
                count=self.found_users["count"],
                **filters
            ),
        )["items"]
        self.found_users["users"].extend(users)
        return self.__get_new_found_user()

    def get_photos(self, vk_id) -> list[dict]:
        response = self.user.method(
            "photos.get",
            {"user_id": vk_id, "album_id": "profile", "extended": 1, "count": 3},
        )
        return response["items"]
