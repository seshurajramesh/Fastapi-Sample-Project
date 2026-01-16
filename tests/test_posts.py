from schemas import PostNestedUser,PostCreate
import pytest



async def test_get_all_posts(authorized_client,test_posts):
    response = await authorized_client.get("/posts/")
    assert response.status_code == 200
    print(response.json())
    assert len(response.json()) == len(test_posts)


async def test_unauthorized_user_get_all_posts(client,test_posts):
    response = await client.get("/posts/")
    assert response.status_code == 401


async def test_unauthorized_user_get_one_post(client,test_posts):
    response = await client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

async def test_get_one_post_not_exist(authorized_client,test_posts):
    response = await authorized_client.get(f"/posts/88888")
    assert response.status_code == 403


async def test_get_one_post(authorized_client,test_posts):
    response = await authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200
    post = PostNestedUser(**response.json())
    assert post.id == test_posts[0].id
    assert post.content == test_posts[0].content   


@pytest.mark.parametrize("title,content,published",[
    ("awesome new title","awesome new content",True),
    ("dsomdosamoom","snfodsnfosnfo",False),
    ("huhwqiwedwdouewhdu","whdouewqhuwqdouwq",True)])

async def test_create_post(authorized_client,test_user,title,content,published):
    response = await authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
    assert response.status_code == 201
    new_post = PostCreate(**response.json())
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert new_post.owner_id == test_user["id"]

async def test_create_post_default_published_true(authorized_client,test_user):
    response = await authorized_client.post("/posts/",json={"title":"random title","content":"random content"})
    assert response.status_code == 201
    new_post = PostCreate(**response.json())
    assert new_post.title == "random title"
    assert new_post.content == "random content"
    assert new_post.published == True
    assert new_post.owner_id == test_user["id"]

async def test_unauthorized_user_create_post(client,test_user):
    response = await client.post("/posts/",json={"title":"random title","content":"random content"})
    assert response.status_code == 401

async def test_unauthorized_user_delete_post(client,test_user,test_posts):
    response = await client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

async def test_delete_post_success(authorized_client,test_user,test_posts):
    response = await authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204 

async def test_delete_post_non_exist(authorized_client,test_user,test_posts):
    response = await authorized_client.delete(f"/posts/88888")
    assert response.status_code == 403

async def test_update_post(authorized_client,test_user,test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id}

    response = await authorized_client.put(f"/posts/{test_posts[0].id}",json=data)
    assert response.status_code == 202
    update_post = PostNestedUser(**response.json())
    assert update_post.title == data["title"]
    assert update_post.content == data["content"]

async def test_update_unauthorized_user_post(client,test_user,test_posts):
    response = await client.put(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

async def test_update_non_exist_post(authorized_client,test_user,test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id}
    response = await authorized_client.put(f"/posts/88888",json=data)
    assert response.status_code == 403