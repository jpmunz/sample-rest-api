import pytest
from sample import create_app, sql, redis_store


def create_test_app():
    return create_app(
        test_config=dict(
            SQLALCHEMY_DATABASE_URI="sqlite:////tmp/sample_test.db",
            REDIS_URL="redis://:@localhost:6379/1",
            TESTING=True,
        )
    )


@pytest.fixture(autouse=True, scope="session")
def sql_cleanup():
    sql.create_all(app=create_test_app())
    yield
    sql.drop_all(app=create_test_app())


@pytest.fixture(autouse=True, scope="session")
def redis_cleanup():
    yield
    redis_store.flushdb()


# http://alexmic.net/flask-sqlalchemy-pytest
@pytest.fixture(scope="function")
def client():
    app = create_test_app()
    with app.test_client() as client:
        with app.app_context():
            connection = sql.engine.connect()
            transaction = connection.begin()
            options = dict(bind=connection, binds={})
            session = sql.create_scoped_session(options=options)

        sql.session = session

        yield client

        transaction.rollback()
        connection.close()
        session.remove()
