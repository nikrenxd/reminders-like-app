import json, asyncio, sys, os
from sqlalchemy import insert

from src.database import Session

from src.users.auth import get_hashed_password
from src.users.models import User
from src.collections.models import Collection
from src.tasks.models import Task


def get_json_data(file_name: str) -> list[dict]:
    with open("data/" + file_name + ".json") as f:
        encoded_data = json.loads(f.read())
    return encoded_data


def get_users_with_hashed_password() -> list[dict[str, str]]:
    users = get_json_data("users")
    for user in users:
        user["password"] = get_hashed_password(user.get("password"))
    return users


class DbController:
    @staticmethod
    async def populate_db_with_users_and_tasks():
        # users = get_users_with_hashed_password()
        # collections = get_json_data("collections")
        tasks = get_json_data("tasks")

        async with Session() as session:
            # insert_users = insert(User).values(users)
            # insert_collections = insert(Collection).values(collections)
            insert_tasks = insert(Task).values(tasks)

            # await session.execute(insert_users)
            # await session.execute(insert_collections)
            await session.execute(insert_tasks)
            await session.commit()


async def main():
    sys_argv = sys.argv

    if len(sys_argv) < 2:
        raise Exception("Need provide more args")

    if sys_argv[1] == "populate":
        await DbController().populate_db_with_users_and_tasks()


if __name__ == "__main__":
    asyncio.run(main())
