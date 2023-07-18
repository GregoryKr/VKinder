from datetime import datetime

import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.utils import get_random_id

from db import session
from db.models import FoundUser
from settings import ACCESS_TOKEN, COMMUNITY_TOKEN

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

    def get_user(self, user_id: int) -> dict | None:
        data = self.user.method(
            "users.get", {"user_id": user_id, "fields": ",".join(REQUIRED_FIELDS)}
        )
        if not data:
            return
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
        )
        if not results or "items" not in results:
            return

        return results["items"][0]["id"]

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
        response = self.user.method(
            "users.search",
            dict(
                status=status,
                hasphoto=hasphoto,
                is_closed=is_closed,
                offset=self.found_users["offset"],
                count=self.found_users["count"],
                **filters
            ),
        )

        try:
            users = response["items"]
        except (TypeError, KeyError):
            users = []

        self.found_users["users"].extend(users)
        return self.__get_new_found_user()

    def get_photos(self, vk_id) -> list[dict]:
        response = self.user.method(
            "photos.get",
            {"user_id": vk_id, "album_id": "profile", "extended": 1, "count": 3},
        )

        if not response or "items" not in response:
            return []
        return response["items"]
