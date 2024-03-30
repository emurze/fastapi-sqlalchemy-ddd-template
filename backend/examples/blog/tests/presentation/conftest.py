from httpx import AsyncClient, Response


async def create_post(ac: AsyncClient, title: str, content: str) -> Response:
    return await ac.post("/posts/", json={"title": title, "content": content})
