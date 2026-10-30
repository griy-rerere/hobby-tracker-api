# Hobby Tracker - API

![Python Version](https://img.shields.io/badge/Python%20Version-3.14%2B-0969da?logo=python)
![manager](https://img.shields.io/badge/manager-poetry-0969da?logo=poetry)
![Web](https://img.shields.io/badge/Web-FastAPI-009485?logo=fastapi)


**The project is still under development and the README presents the plans and features which might change in the future!**

This repository contains the Web API for the Hobby Tracker application.

The project uses both
* The [core](https://github.com/griy-rerere/hobby-tracker-core) package
* The [infrastructure](https://github.com/griy-rerere/hobby-tracker-infrastructure) package

## 🎯 Features

See the [core](https://github.com/griy-rerere/hobby-tracker-core) package to check out the features of Hobby Tracker.

This project provides a functional REST Web API. Everything within the project is just an extra layer above the core application layer. The most essential components are the *web endpoints*, which mostly mirror the core *commands* & *queries*.

Currently, the endpoints are built using the FastAPI web framework. See the [FastAPI documentation](https://fastapi.tiangolo.com/) for additional information.

### Authorization

The key feature beyond the core package is *user management*. The core doesn't know anything about users so this project is responsible for the *authorization* as well.

#### JWT

Authorization is achieved via JWT(JSON Web Token) standard. API is responsible for:
* Creating *Access* & *Refresh* tokens
* Receiving tokens with requests and **validating** them against a `SECRET_KEY`
* Storing tokens in a database (currently no database is implemented)

## 🚀 Run

Run with `fastapi` command:
```
poetry run fastapi dev
```

## 🛠️ Code Quality & Verification

The core domain guarantees absolute reliability through strict type safety and high test coverage.

Before committing, make sure all quality gates pass successfully:

* **Formatting & Linting (Ruff):**
  ```bash
  poetry run ruff check .
  poetry run ruff format .
  ```
* **Strict Static Typing (MyPy):**
  ```bash
  poetry run mypy hobby_tracker_api
  ```
* **Unit Testing (PyTest):**
  ```bash
  poetry run pytest
  ```


## 📥 Local Installation & Integration

Add it to your `pyproject.toml` via Git URL:

```toml
[project]
dependencies = [
    "hobby-tracker-api @ git+https://github.com/griy-rerere/hobby-tracker-api.git"
]
```

Or install it directly via pip:
```bash
pip install git+https://github.com/griy-rerere/hobby-tracker-api.git
```

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
