import pytest

from pytest_lazy_fixtures import lf
from rest_framework.test import APIClient
import json

from .models import User

### Fixtures

@pytest.fixture
def NoLoginFixture(client):
    pass

@pytest.fixture
def LogInTemporaryUserFixture(client):
    response = client.post("/user/session")
    assert response.status_code == 200

@pytest.fixture
def LogInRegisteredUserFixture(client):
    user = {"username": "testUser", "email": "test@test.com", "password": "password"}
    response = client.post("/user", user)
    assert response.status_code == 201
    response = client.post("/user/session", user)
    assert response.status_code == 200

@pytest.fixture
def ChangeUserFixture(client, LogInRegisteredUserFixture):
    response = client.patch("/user/testUser", data={"username": "newUsername"})
    assert response.status_code == 200

@pytest.fixture
def LogOutTemporaryUserFixture(client, LogInTemporaryUserFixture):
    response = client.delete("/user/session")
    assert response.status_code == 200

@pytest.fixture
def LogOutRegisteredUserFixture(client, LogInRegisteredUserFixture):
    response = client.delete("/user/session")
    assert response.status_code == 200
    
@pytest.fixture
def superClient(client):
    user = User.objects.create_superuser(username="admin", email="admin@test.com", password="adminPassword")
    user.save()
    response = client.post("/user/session", {"username": "admin", "password": "adminPassword"})
    assert response.status_code == 200
    return client
    
### Test Cases for UserDetailView

@pytest.mark.django_db
def test_UseClientViewWhileUnauthorized(client, LogOutRegisteredUserFixture):
    response = client.put("/user/testUser", {
        "username": "newUsername",
        "email": "newEmail@test.com",
        "password": "newPassword"
    }, content_type='application/json')
    newResponse = client.get("/user/me")
    assert response.status_code == 403
    response = client.patch("/user/testUser", {
        "username": "newUsername",
    }, content_type='application/json')
    assert response.status_code == 403
    response = client.get("/user/testUser")
    assert response.status_code == 200

@pytest.mark.parametrize("UserFixture",[
    lf("LogInTemporaryUserFixture"),
    lf("LogInRegisteredUserFixture"),
])
@pytest.mark.django_db
def test_GetUserFromDetailView(client, UserFixture):
    response = client.post("/user", {"username": "newTestUser", "email": "abc@gmail.com", "password": "testPassword"})
    assert response.status_code == 201
    url = "/user/newTestUser"
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["username"] == "newTestUser"
    assert response.data["email"] == "abc@gmail.com"

@pytest.mark.django_db
def test_GetUndefinedUser(client):
    url = "/user/testUser"
    response = client.get(url)
    assert response.status_code == 404
    assert response.data["detail"] == "No User matches the given query."

@pytest.mark.django_db
def test_ChangeUsername(client, LogInRegisteredUserFixture):
    url = "/user/testUser"
    response = client.patch(url, {"username": "newUsername"}, content_type='application/json')
    assert response.status_code == 200
    assert response.data["username"] == "newUsername"
    assert response.data["email"] == "test@test.com"

@pytest.mark.django_db
def test_ChangeWholeUser(client, LogInRegisteredUserFixture):
    url = "/user/testUser"
    response = client.put(url, {"username": "newUsername", "password": "newPassword", "email": "newEmail@test.com"}, content_type='application/json')
    assert response.status_code == 200
    assert response.data["username"] == "newUsername"
    assert response.data["email"] == "newEmail@test.com"
    
    response = client.post("/user/session", {"username": "newUsername", "password": "newPassword"})
    assert response.status_code == 200

@pytest.mark.django_db
def test_ChangeUndefinedUser(client):
    url = "/user/testUser"
    response = client.put(url, {"username": "newUsername", "email": "newEmail@gmail.com", "password": "newPassword"})
    assert response.status_code == 403

@pytest.mark.django_db
def test_DeleteUser(client, LogInRegisteredUserFixture):
    url = "/user/testUser"
    response = client.delete(url)
    assert response.status_code == 204
    response = client.get(url)
    assert response.status_code == 404
    assert response.data["detail"] == "No User matches the given query."
    
### Test Cases for UserCreateView

@pytest.mark.django_db
def test_CreateEmptyUser(client):
    url = "/user"
    response = client.post(url)
    assert response.status_code == 400
    assert len(response.data) == 3
    assert response.data["username"][0] == "Field is required for non-temporary users."
    assert response.data["email"][0] == "Field is required for non-temporary users."
    assert response.data["password"][0] == "Field is required for non-temporary users."

@pytest.mark.django_db
def test_CreateSuccessfulUser(client):
    url = "/user"
    user = {"username": "testUser", "email": "test@test.com", "password": "password"}
    response = client.post(url, user)
    assert response.status_code == 201
    assert response.data["username"] == user["username"]
    assert response.data["email"] == user["email"]

@pytest.mark.django_db
def test_CreateSameUserTwice(client):
    url = "/user"
    user = {"username": "testUser", "email": "test@test.com", "password": "password"}
    response = client.post(url, user)
    assert response.status_code == 201
    response = client.post(url, user)
    assert response.status_code == 400
    assert response.data["username"][0] == "user with this username already exists."


### Test Cases for CurrentUserView

@pytest.mark.parametrize("UserFixture",[
    lf("NoLoginFixture"),
    lf("LogOutTemporaryUserFixture"),
    lf("LogOutRegisteredUserFixture"),
])
@pytest.mark.django_db
def test_CheckLoggedOutUser(client, UserFixture):
    url = "/user/me"
    response = client.get(url)
    assert response.status_code == 404
    assert response.data["detail"] == "User not found."

@pytest.mark.parametrize("UserFixture",[
    lf("LogInTemporaryUserFixture"),
    lf("LogInRegisteredUserFixture"),
])
@pytest.mark.django_db
def test_CheckLoggedInUser(client, UserFixture):
    url = "/user/me"
    response = client.get(url)
    assert response.status_code == 200

### Test Cases for UserListView

@pytest.mark.django_db
def test_CheckUsersWithNoAuthentication(client):
    url = "/users"
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_CheckOneUser(client, superClient):
    url = "/users"
    response = superClient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    
### Test Cases for SessionView

@pytest.mark.django_db
def test_LogInAnonymousUser(client):
    url = "/user/session"
    response = client.post(url)
    assert response.status_code == 200
    assert response.data["message"] == "User logged in."

@pytest.mark.django_db
def test_LogInAnonymousUserTwice(client, LogInTemporaryUserFixture):
    url = "/user/session"
    response = client.post(url)
    assert response.status_code == 401
    assert response.data["message"] == "User already logged in."

@pytest.mark.django_db
def test_LogInRegisteredUser(client):
    url = "/user/session"
    user = {"username": "testUser", "email": "test@test.com", "password": "password"}
    response = client.post("/user", user)
    assert response.status_code == 201
    session_response = client.post(url, user)
    assert session_response.status_code == 200
    assert session_response.data["message"] == "User logged in."

@pytest.mark.django_db
def test_LogInRegisteredUserWithWrongPassword(client):
    url = "/user/session"
    user = {"username": "testUser", "password": "wrongPassword"}
    response = client.post(url, user)
    assert response.status_code == 401
    assert response.data["error"] == "Invalid username or password."
    
@pytest.mark.django_db
def test_LogOutRegisteredUser(client, LogInRegisteredUserFixture):
    oldUsername = client.get("/user/me").data["username"]
    url = "/user/session"
    response = client.delete(url)
    assert response.status_code == 200
    assert response.data == None
    
    # Check the user is logged out
    response = client.get("/user/me")
    assert response.status_code == 404
    
    # Check the user still exists
    response = client.get(f"/user/{oldUsername}")
    assert response.status_code == 200

@pytest.mark.django_db
def test_LogOutTemporaryUser(client, LogInTemporaryUserFixture):
    oldUsername = client.get("/user/me").data["username"]
    url = "/user/session"
    response = client.delete(url)
    assert response.status_code == 200
    assert response.data == None
    
    # Check the user is logged out
    response = client.get("/user/me")
    assert response.status_code == 404
    
    # Check the user is deleted
    response = client.get(f"/user/{oldUsername}")
    assert response.status_code == 404
    
@pytest.mark.django_db
def test_LogOutNoUser(client):
    url = "/user/session"
    response = client.delete(url)
    assert response.status_code == 401
    assert response.data["message"] == "User not logged in."
    
@pytest.mark.django_db 
def test_LogOutDeletesSinglePlayerGame(client, superClient, LogInRegisteredUserFixture):
    client.post("/game/session/testGame")
    response = client.delete("/user/session")
    assert response.status_code == 200
    response = superClient.get("/game/testGame")
    assert response.status_code == 404
    assert response.data["detail"] == "No Game matches the given query."

@pytest.mark.django_db
def test_LogOutRemovesPlayerFromMultiplayerGame(client, superClient, LogInRegisteredUserFixture):
    # Create a game using player 1
    response = client.post("/game/testGame")
    response = client.post("/game/testGame/player")
    
    # Create and Login with player 2
    client2 = APIClient()
    client2.post("/user", {"username": "testUser1", "email": "test1@test.com", "password": "test1Password"})
    response = client2.post("/user/session", {"username": "testUser1", "password": "test1Password"})
    assert response.status_code == 200
    
    # Add player 2 to the game
    response = client2.post("/game/testGame/player")
    print(f"Response: {response.data}")
    assert response.status_code == 201
    
    # Log out with Player 1
    response = client.delete("/user/session")
    assert response.status_code == 200
    
    # Check that player 2 is still in the game
    response = superClient.get("/game/testGame")
    assert response.status_code == 200
    assert "testUser1" in [user["username"] for user in response.data["users"]]
    assert response.data["admin"]["username"] == "testUser1"