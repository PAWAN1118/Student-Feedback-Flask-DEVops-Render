# Student Feedback System

A full-stack DevOps project — Flask web app with a complete local CI/CD pipeline.

```
Git Push → Jenkins → Docker Build → Ansible Deploy → Live App
```

## Quick Start (Manual)

```bash
docker build -t student-feedback-system:latest .
docker volume create feedback_data
docker run -d --name feedback-app -p 8090:5000 \
  -v feedback_data:/data student-feedback-system:latest
# Open http://localhost:8090
```

## Project Structure

```
├── app/              Flask application
├── ansible/          Deployment playbook
├── feedback-pkg/     Installable Python package
├── Dockerfile        Container build
└── Jenkinsfile       CI/CD pipeline
```

## CI/CD Pipeline (Jenkins)

1. Checkout — clone repo
2. Lint — flake8 Python checks
3. Test — pytest (if tests/ exists)
4. Build Docker Image
5. Validate Image — smoke test on port 5099
6. Deploy with Ansible — via Docker container
7. Verify Deployment — health check on port 8090

## Tech Stack

| Layer       | Technology              |
|-------------|-------------------------|
| Backend     | Python 3.12 + Flask 3.0 |
| Database    | SQLite                  |
| Frontend    | HTML5 + CSS3            |
| Container   | Docker (multi-stage)    |
| CI/CD       | Jenkins                 |
| Deployment  | Ansible                 |

## Python Package

```bash
cd feedback-pkg
pip install -e .
feedback-system run
```
