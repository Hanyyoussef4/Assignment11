# Assignment 11 – Calculation Model, Alembic Migrations & Extended CI/CD

![CI/CD Status](https://github.com/Hanyyoussef4/Assignment11/actions/workflows/ci.yml/badge.svg)

> **What’s new in Module 11?**
>
> * Added **Calculation** SQLAlchemy model (Add, Subtract, Multiply, Divide)
> * Alembic migrations folder & auto‑generated migration for `calculations` table
> * Pydantic schemas **CalculationCreate / CalculationRead** with robust validation
> * Extra unit tests + CI workflow now installs Alembic, runs migrations, and skips UI tests
> * Image pushed to **`hany25/assignment11`** on Docker Hub

The earlier functionality from Assignment 10 (secure users, JWT auth, full testing,
Dockerised FastAPI) remains intact.

---

## 🔗 Quick Links

* **GitHub Repo**: [https://github.com/Hanyyoussef4/Assignment11](https://github.com/Hanyyoussef4/Assignment11)
* **Docker Hub**: [https://hub.docker.com/r/hany25/assignment11](https://hub.docker.com/r/hany25/assignment11)
* **Reflection**: [Documentation/Reflection.md](Documentation/Reflection.md)

---

## 🐳 Docker Image

```bash
docker pull hany25/assignment11:latest
docker run -p 8000:8000 hany25/assignment11:latest
```

---

## 📂 Project Structure

```
.
├── app/
│   ├── auth/                       # JWT & auth deps
│   ├── models/
│   │   ├── user.py
│   │   └── calculation.py          # ← NEW
│   ├── operations/
│   ├── schemas/
│   │   ├── user.py
│   │   └── calculation.py          # ← NEW
│   ├── database.py
│   └── config.py
├── migrations/                     # ← NEW (Alembic)
│   ├── env.py
│   └── versions/
│       └── *_add_calculations_table.py
├── tests/
│   ├── unit/
│   │   └── test_calculation_schema.py   # ← NEW
│   ├── integration/
│   └── e2e/
├── Documentation/
│   ├── Docker Hub Deployment.png
│   ├── GitHub Actions Workflow.png
│   └── Reflection.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml                  # updated: alembic + skip e2e
└── README.md
```

---

## 🚦 CI/CD Pipeline

1. **test** – installs deps, runs Alembic `upgrade head`, then `pytest -k "not e2e"`
2. **security** – builds a local image and scans with Trivy
3. **deploy** – pushes `hany25/assignment11` (`latest` & `${{ sha }}`) to Docker Hub

<details>
<summary>Workflow screenshot</summary>

![GitHub Actions Workflow](Documentation/GitHub%20Actions%20Workflow.png)

</details>

---

## ✨ Features

* **Calculation Endpoints** (to be exposed in Module 12) already have
  database & schema support, easing future API work.
* Validators prevent *divide‑by‑zero* and enforce allowed operation types.
* Fully automated pipeline keeps the test database schema in sync via Alembic.
