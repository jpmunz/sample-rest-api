def create_bar(client, json=None):
    if json is None:
        json = {"name": "my bar"}

    res = client.post("/v1/bar/", json=json)
    return res.get_json()["id"]


def test_create_bar(client):
    res = client.post("/v1/bar/", json={"name": "my bar"})
    assert res.status_code == 201

    created_bar = res.get_json()
    expected_bar = {"id": created_bar["id"], "name": "my bar"}
    assert created_bar == expected_bar

    # Assert that the resource was actually created
    res = client.get("/v1/bar/{}".format(created_bar["id"]))
    assert res.status_code == 200
    assert res.get_json() == expected_bar


def test_create_bar_invalid(client):
    res = client.post("/v1/bar/", json={})
    assert res.status_code == 400


def test_update_bar(client):
    id = create_bar(client)

    res = client.put("/v1/bar/{}".format(id), json={"name": "new name"})
    assert res.status_code == 200
    expected_bar = {"id": id, "name": "new name"}
    assert res.get_json() == expected_bar

    # Assert that the resource was actually updated
    res = client.get("/v1/bar/{}".format(id))
    assert res.status_code == 200
    assert res.get_json() == expected_bar


def test_update_bar_invalid(client):
    res = client.put("/v1/bar/{}".format(create_bar(client)), json={})
    assert res.status_code == 400


def test_update_bar_not_found(client):
    res = client.put("/v1/bar/1", json={"name": "new name"})
    assert res.status_code == 404


def test_delete_bar(client):
    id = create_bar(client)

    res = client.delete("/v1/bar/{}".format(id))
    assert res.status_code == 204

    # Assert that the resource was actually deleted
    res = client.get("/v1/bar/{}".format(id))
    assert res.status_code == 404


def test_delete_bar_not_found(client):
    res = client.delete("/v1/bar/1")
    assert res.status_code == 404


# If multiple resources follow the basic testing pattern as above, consider
# adding a base test class:
class BaseResourceTests(object):
    def create(self, client, json=None):
        if json is None:
            json = self.base_json

        res = client.post(self.route, json=json)
        return res.get_json()["id"]

    def test_create(self, client):
        res = client.post(self.route, json=self.base_json)
        assert res.status_code == 201

        created = res.get_json()
        expected = {"id": created["id"]}
        expected.update(self.base_json)
        assert created == expected

        # Assert that the resource was actually created
        res = client.get("{}{}".format(self.route, created["id"]))
        assert res.status_code == 200
        assert res.get_json() == expected

    def test_create_invalid(self, client):
        res = client.post(self.route, json={})
        assert res.status_code == 400

    def test_update(self, client):
        id = self.create(client)

        res = client.put("{}{}".format(self.route, id), json=self.update_json)
        assert res.status_code == 200
        expected = {"id": id}
        expected.update(self.update_json)
        assert res.get_json() == expected

        # Assert that the resource was actually updated
        res = client.get("{}{}".format(self.route, id))
        assert res.status_code == 200
        assert res.get_json() == expected

    def test_update_invalid(self, client):
        res = client.put("{}{}".format(self.route, self.create(client)), json={})
        assert res.status_code == 400

    def test_update_not_found(self, client):
        res = client.put("{}{}".format(self.route, 1), json=self.update_json)
        assert res.status_code == 404

    def test_delete(self, client):
        id = self.create(client)

        res = client.delete("{}{}".format(self.route, id))
        assert res.status_code == 204

        # Assert that the resource was actually deleted
        res = client.get("{}{}".format(self.route, id))
        assert res.status_code == 404

    def test_delete_not_found(self, client):
        res = client.delete("{}{}".format(self.route, 1))
        assert res.status_code == 404


# And inheriting it for each Resources tests:
class TestFooResource(BaseResourceTests):
    route = "/v1/foo/"
    base_json = {"name": "my foo"}
    update_json = {"name": "new name"}
