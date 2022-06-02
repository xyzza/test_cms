import pytest


async def test_get_single(not_authorized_client, article):
    response = await not_authorized_client.get(f"/v1/articles/{article['id']}")
    assert response.status_code == 200
    resp = response.json()
    assert resp["id"] == article["id"]


async def test_delete_article(authorized_client, not_authorized_client, article):
    response = await authorized_client.delete(f"/v1/articles/{article['id']}")
    assert response.status_code == 204
    response = await not_authorized_client.get(f"/v1/articles/{article['id']}")
    assert response.status_code == 404


async def test_delete_non_existing_article(authorized_client):
    response = await authorized_client.delete("/v1/articles/1")
    assert response.status_code == 404


async def test_insert_article(authorized_client):
    response = await authorized_client.post(
        "/v1/articles/", json={"title": "Adventure", "body": "Time!"}
    )
    assert response.status_code == 201
    article = response.json()
    response = await authorized_client.get(f"/v1/articles/{article['id']}")
    assert response.status_code == 200


async def test_update_article(authorized_client, article):
    new_title = "Hello World"
    response = await authorized_client.patch(
        f"/v1/articles/{article['id']}", json={"title": new_title}
    )
    assert response.status_code == 200
    article = response.json()
    assert article["title"] == new_title


async def test_update_non_existing_article(authorized_client):
    new_title = "Hello World"
    response = await authorized_client.patch(
        "/v1/articles/1", json={"title": new_title}
    )
    assert response.status_code == 404


@pytest.mark.parametrize(
    "sort",
    [True, False],
)
async def test_get_multiple_sort(not_authorized_client, articles, sort):
    response = await not_authorized_client.get(f"/v1/articles/?sort_asc={sort}")
    assert response.status_code == 200
    resp = response.json()
    assert "items" in resp
    assert len(resp["items"]) == len(articles)
    if sort:
        assert resp["items"][0]["id"] < resp["items"][1]["id"]
    else:
        assert resp["items"][0]["id"] > resp["items"][1]["id"]


async def test_get_multiple_search(not_authorized_client, articles):
    response = await not_authorized_client.get(
        f"/v1/articles/?title={articles[0]['title']}"
    )
    assert response.status_code == 200
    resp = response.json()
    assert "items" in resp
    assert len(resp["items"]) == 1
    assert resp["items"][0]["title"] == articles[0]["title"]
