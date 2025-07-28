# Reflection on Module 11 – Calculation Model & CI/CD Hardening
**Author**: Hany Youssef  
**Date**: 27 July 2025  

## 1 · What I set out to build  
Module 11 asked me to extend the FastAPI code‑base from Module 10 with:  

1. A **`Calculation`** SQLAlchemy model that supports `Add`, `Sub`, `Multiply`, `Divide`.  
2. Robust **Pydantic V2** schemas with field‑level and model‑level validation (e.g. “division‑by‑zero” guard).  
3. Optional **factory pattern** to decouple the four math operations.  
4. New **unit, integration & e2e tests**, wired into GitHub Actions.  
5. A hardened **CI/CD** pipeline that only deploys (“push to Docker Hub”) if tests + Trivy security scan succeed.

## 2 · Key pain‑points & how I solved them  

| Area | Problem | Solution |
|------|---------|----------|
| **Pydantic v2** | `orm_mode` was renamed → tests failed in CI. | Migrated to `model_config = ConfigDict(from_attributes=True)` and updated unit tests. |
| **Model validation** | Division by 0 wasn’t rejected. | Added `@field_validator("b")` **and** a model‑level `@model_validator(mode="after")` that raises `ValueError` when `type=="divide"` and `b==0`. |
| **Alembic in CI** | `alembic revision --autogenerate` failed because the runner’s DB had no `fastapi_test_db`. | Declared a dedicated Postgres service in `test.yml`, then executed `psql -c "CREATE DATABASE fastapi_test_db;"` before `alembic upgrade head`. |
| **Docker tags** | Initial workflow tried to push `***/assignment11:latest` (invalid tag). | Replaced the `***` placeholder with **`hany25/assignment11`** and removed inline comments that confused the YAML parser. |
| **Secrets** | Old Docker Hub PAT ​expired. | Generated a new PAT (`dckr_pat_xxxxxx…`) and stored it as `DOCKERHUB_TOKEN`; verified with a manual `docker login`. |

## 3 · What I learned  

* Writing **model‑level validators** in Pydantic v2.  
* How GitHub Actions can orchestrate DB migration + tests inside one workflow graph.  
* Pushing **multi‑arch** Docker images (`linux/amd64` + `linux/arm64`) with `docker/build‑push‑action@v5`.  
* The importance of **clear commit slices**: small, focused commits made debugging the pipeline far easier.

## 4 · Next steps  

* Move the calculator factory behind an interface so new operations (e.g. exponent) can be plugged in without touching the API layer.  
* Add GitHub Release‑driven semantic‑version tags (`v1.0.0`) for Docker images.  
* Enable Dependabot to keep base images & Python deps patched.

---
