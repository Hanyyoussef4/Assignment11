# Assignment 10 – Secure FastAPI with CI/CD & Docker

![CI/CD Status](https://github.com/Hanyyoussef4/Assignment10/actions/workflows/test.yml/badge.svg)

A FastAPI application with:

1. Secure User model (bcrypt password hashing, JWT auth)
2. PostgreSQL backend via SQLAlchemy
3. Full test coverage (unit, integration, e2e)
4. GitHub Actions CI pipeline (tests → security scan → Docker build & push)
5. Docker image published to Docker Hub

---

## 🔗 Quick Links

* **GitHub Repo**: [https://github.com/Hanyyoussef4/Assignment10](https://github.com/Hanyyoussef4/Assignment10)
* **Docker Hub**: [https://hub.docker.com/r/hany25/assignment10](https://hub.docker.com/r/hany25/assignment10)
* **Reflection**: [Documentation/Reflection.md](Documentation/Reflection.md)

---

## 🐳 Docker Image

```bash
docker pull hany25/assignment10:latest
docker run -p 8000:8000 hany25/assignment10:latest
```

---

## 📂 Project Structure

```
.
├── app/
│   ├── auth/                   # Authentication dependencies & JWT
│   ├── models/                 # SQLAlchemy ORM models
│   ├── operations/             # Business logic functions
│   ├── schemas/                # Pydantic request/response models
│   ├── database.py             # Engine & session setup
│   └── config.py               # SECRET_KEY, token expiry, etc.
├── tests/                      # Unit, integration & e2e tests
├── Documentation/              # Screenshots & reflection (rename doc to Documentation)
│   ├── Docker Hub Deployment.png
│   ├── GitHub Actions Workflow.png
│   └── reflection.md
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container instructions
├── docker-compose.yml          # Dev environment
├── main.py                     # FastAPI entrypoint
├── .github/
│   └── workflows/
│       └── test.yml            # CI/CD pipeline
└── README.md                   # (this file)
```

---

## 🚦 CI/CD Pipeline

1. **test** – runs unit, integration & e2e tests
2. **security** – builds a local image and scans with Trivy
3. **deploy** – builds and pushes `hany25/assignment10` (latest & SHA tags)

<details>
<summary>View workflow screenshot</summary>

!\[GitHub Actions Workflow]\(Documentation/GitHub\ Actions\ Workflow\.png)

</details>

---

**Author:** Hany Youssef
**Course:** IS601 – Module 10
**Date:** July 26, 2025
