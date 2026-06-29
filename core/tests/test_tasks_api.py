def test_tasks_list_response_200(auth_user):
    response = auth_user.get("/tasks")
    assert response.status_code == 200


def test_tasks_list_response_401(anon_user):
    response = anon_user.get("/tasks")
    assert response.status_code == 401


def test_task_detail_response_200(auth_user, random_task):
    task = random_task
    response = auth_user.get(f"/tasks/{task.id}")
    assert response.status_code == 200


def test_task_detail_response_401(anon_user, random_task):
    task = random_task
    response = anon_user.get(f"/tasks/{task.id}")
    assert response.status_code == 401


def test_task_detail_response_404(auth_user):
    response = auth_user.get("/tasks/20")
    assert response.status_code == 404


def test_task_create_response_201(auth_user):
    payload = {
        "title":"test",
        "description":"description",
        "is_completed":True
    }
    response = auth_user.post("/task/create", json=payload)
    assert response.status_code == 201


def test_task_create_response_401(anon_user):
    payload = {
        "title":"test",
        "description":"description",
        "is_completed":True
    }
    response = anon_user.post("/task/create", json=payload)
    assert response.status_code == 401


def test_task_create_response_422(auth_user):
    payload = {
        "description":"description",
        "is_completed":True
    }
    response = auth_user.post("/task/create", json=payload)
    assert response.status_code == 422


def test_task_update_response_200(auth_user, random_task):
    task = random_task
    payload = {
        "title":"test update",
        "description":"description update",
        "is_completed":False
    }
    response = auth_user.put(f"/tasks/update/{task.id}", json=payload)
    assert response.status_code == 200


def test_task_update_response_401(anon_user):
    payload = {
        "title":"test update",
        "description":"description update",
        "is_completed":False
    }
    response = anon_user.put("/tasks/update/10", json=payload)
    assert response.status_code == 401


def test_task_update_response_404(auth_user):
    payload = {
        "title":"test update",
        "description":"description update",
        "is_completed":False
    }
    response = auth_user.put("/tasks/update/20", json=payload)
    assert response.status_code == 404


def test_task_delete_response_204(auth_user, random_task):
    task = random_task
    response = auth_user.delete(f"/task/delete/{task.id}")
    assert response.status_code == 204


def test_task_delete_response_401(anon_user):
    response = anon_user.delete("/task/delete/20")
    assert response.status_code == 401


def test_task_delete_response_404(auth_user):
    response = auth_user.delete("/task/delete/20")
    assert response.status_code == 404