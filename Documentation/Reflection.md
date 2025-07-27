# Reflection on Assignment 10

**Author:** Hany Youssef  
**Date:** July 26, 2025

## 1. Overview

In this assignment I built a FastAPI application with a secure user model (password hashing, JWT, registration/authentication), connected to a PostgreSQL database, and wrote full test coverage (unit, integration, end‑to‑end). I then set up a CI/CD pipeline on GitHub Actions to run tests, scan for vulnerabilities with Trivy, and automatically build & push a Docker image to Docker Hub.

## 2. Key Challenges

1. **Dependency Conflicts**  
   - Upgrading `h11` to fix CVE‑2025‑43859 conflicted with `httpcore==1.0.6` (which required `h11<0.15`).  
   - Similarly, pinning `python-jose==3.4.0` required downgrading `pyasn1` to `<0.5.0`.  
   - **Solution:** I upgraded the entire `httpx`/`httpcore` stack (to 0.28.1/1.0.9) and aligned `h11` and `pyasn1` to their patched versions.

2. **CI Environment Imports**  
   - In GitHub Actions, Python couldn’t find my `app` package by default, causing `ModuleNotFoundError`.  
   - **Solution:** I added `PYTHONPATH: ${{ github.workspace }}` to the test step so that `import app.*` worked correctly.

3. **Security Scanning with Trivy**  
   - Out‑of‑the‑box, Trivy failed on critical CVEs in dependencies.  
   - **Solution (final):** I upgraded to patched releases so that Trivy no longer reported critical issues. Alternatively, I could have relaxed the exit code, but I chose to resolve the vulnerabilities upstream.

## 3. What I Learned

- How to use **PassLib** for secure password hashing and **python‑jose** for JWT creation/verification.
- Configuring **SQLAlchemy** and **Pydantic** together in a FastAPI project.
- Writing robust **pytest** suites that include unit, integration, and Playwright e2e tests.
- How to orchestrate multi‑service tests with **GitHub Actions**, ensuring a Postgres service is healthy before running tests.
- Managing **Docker** builds in CI and pushing images to Docker Hub using `docker/build-push-action`.
- Working around dependency conflicts by upgrading stacks and pinning compatible versions.

## 4. Next Steps

- Add database migrations (e.g., Alembic) for schema evolution.
- Enhance error handling and logging for production readiness.
- Explore health checks and readiness probes in Kubernetes.
- Automate tagging of Docker images with semantic versions.

---