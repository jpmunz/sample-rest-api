![deploy status](https://github.com/jpmunz/decidel-flask/workflows/Build%20and%20Deploy/badge.svg)
![code style: black](https://img.shields.io/badge/code_style-black-000000.svg?style=plastic")

A sample repo demonstrating the steps outlined in [this documentation](https://development-recipes.readthedocs.io/en/latest/rest-api.html).

### DEVELOPMENT

### Setup

```
  python3 -m venv venv
  . venv/bin/activate
  pip install -r requirements.txt
```

Make sure redis is installed

```
  wget http://download.redis.io/redis-stable.tar.gz
  tar xvzf redis-stable.tar.gz
  cd redis-stable
  make
```

### Run

```
  redis-server
```

```
  . venv/bin/activate
  FLASK_APP=sample FLASK_ENV=development flask run
```

### Deployment

See [these instructions](https://development-recipes.readthedocs.io/en/latest/hosting.html) for initial setup.

Actual deployment is handled by the [Deploy Action](.github/workflows/deploy.yml).
