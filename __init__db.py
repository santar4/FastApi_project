import asyncio

from app.models import User, Comment, Picture
from settings import engine, Base, async_session


async def create_bd():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data():
    async with async_session() as sess:
        try:
            user = User(
                username="john_doe",
                email="john.doe@example.com",
                password_hash="user1",
                bio_profile="A photographer and adventurer"
            )

            await sess.flush()


            picture = Picture(
                image=b'RIFF\xbc_\x00\x00WEBPVP8 \xb0_\x00\x00P\x14\x01\x9d\x01*h\x01\xcb\x00>1\x16\x88C"!!\x15If\xbc \x03\x04\xa0\x0b\xbb%U',  # Ваш файл у байтах
                name="Sunset",
                description="A beautiful sunset over the mountains",
                tag="nature",
                author=user
            )

            await sess.flush()


            comment = Comment(
                content="Amazing shot!",
                picture=picture,
                author=user
            )

            finalentry = (user, picture, comment)
            sess.add(finalentry)

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