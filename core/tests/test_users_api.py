def test_signup_response_409(anon_user):
    payload = {
        "email":"test@gmail.com",
        "password":"1234",
        "confirm_password":"1234"
    }
    response = anon_user.post("signup", json=payload)
    assert response.status_code == 409


def test_signup_response_201(anon_user):
    payload = {
        "email":"admin@gmail.com",
        "password":"1234",
        "confirm_password":"1234"
    }
    response = anon_user.post("/signup", json=payload)
    assert response.status_code == 201


def test_signup_response_422(anon_user):
    payload = {
        "email":"admin@gmail.com",
        "password":"1234",
        "confirm_password":"4321"
    }
    response = anon_user.post("/signup", json=payload)
    assert response.status_code == 422


def test_login_inccorect_email_response_401(anon_user):
    payload = {
        "email":"not.test@gmail.com",
        "password":"1234"
    }
    response = anon_user.post("/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "inccorect email or password"


def test_login_inccorect_password__response_401(anon_user):
    payload = {
        "email":"test@gmail.com",
        "password":"12345678"
    }
    response = anon_user.post("/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "inccorect email or password"


def test_login_response_200(anon_user):
    payload = {
        "email":"test@gmail.com",
        "password":"1234"
    }
    response = anon_user.post("/login", json=payload)
    assert response.status_code == 200