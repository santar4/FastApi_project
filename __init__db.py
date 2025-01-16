import asyncio

from app.models import User, Comment, Picture, Tag
from settings import engine, Base, async_session


async def create_bd():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data():
    async with async_session() as sess:
        try:
            user = User(username="john_doe", email="john@example.com", password_hash="hashed_password")
            user2 = User(username="jane_smith", email="jane@example.com", password_hash="hashed_password")

            tag1 = Tag(name="nature")
            tag2 = Tag(name="city")

            with open(r"C:\Go_iteens_Projects\FastApi_final_project\app\static\wallpaperflare.com_wallpaper.jpg",
                      "rb") as image_file:
                image_data = image_file.read()

            picture1 = Picture(
                name="Sunset in Nature",
                description="A beautiful sunset over a forest.",
                tag="nature",
                image=image_data,
                author=user
            )

            # Додавання тегів до картинок
            picture1.tags.append(tag1)

            # Створення коментарів
            comment1 = Comment(content="Amazing view!", author=user, picture=picture1)

            # Додавання до сесії
            sess.add(user)
            sess.add(user2)
            sess.add(picture1)

            sess.add(tag1)
            sess.add(tag2)
            sess.add(comment1)

            await sess.commit()

        except Exception as e:
            await sess.rollback()
            print(f"Помилка при додаванні даних: {e}")


async def main():
    await create_bd()
    print("database created")
    await insert_data()
    print("data added")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
