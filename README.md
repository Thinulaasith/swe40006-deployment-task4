# Docker Deployment Portfolio

**SWE40006 · Software Deployment and Evolution · Task 4**

A Docker deployment portfolio covering environment verification, a published Python web application, a publicly tested web application, and a containerised command-line tool.

## At a glance

| Level | Application | What it demonstrates |
|---|---|---|
| Pass | Docker `hello-world` | Docker installation and container execution |
| Credit | Study Task Tracker | Flask app, Docker Hub publishing, and deployment in a secondary Docker environment |
| Distinction | Focus Planner | Optimised Dockerfile, runtime configuration, exposed port, and public HTTPS testing |
| High Distinction | CSV Study Report | Non-web container, non-root execution, logs, and persistent output through a bind mount |

> **Prerequisite:** Install Docker Desktop or Docker Engine and make sure Docker is running. The commands below are written for Windows PowerShell and should be run from the repository’s root folder.

## Credit · Study Task Tracker

A simple Flask application with a home page and a JSON health check. Its image was published to [Docker Hub](https://hub.docker.com/r/thinulaasith/study-task-tracker) and then pulled and run in a separate Docker-in-Docker environment.

```powershell
docker build -t study-task-tracker:1.0 .\credit-app
docker run -d --name credit-web -p 8080:5000 study-task-tracker:1.0
```

| Endpoint | Address |
|---|---|
| Home page | http://localhost:8080 |
| Health check | http://localhost:8080/health |

**Published image:** `thinulaasith/study-task-tracker:1.0`

## Distinction · Focus Planner

A separate Flask application that turns a selected number of focus minutes into a study plan. Its title and break duration can be changed when starting the container.

The Dockerfile installs dependencies before copying the application code, starts the app with Gunicorn, and configures a non-root user.

```powershell
docker build -t focus-planner:1.0 .\distinction-app
docker run -d --name distinction-web -p 8082:5000 -e APP_TITLE="My Focus Planner" -e BREAK_MINUTES=10 focus-planner:1.0
```

| Endpoint | Address |
|---|---|
| Focus Planner | http://localhost:8082 |
| Health check | http://localhost:8082/health |

For example, entering **75 focus minutes** produces **three 25-minute study blocks**, **two 10-minute breaks**, and **95 minutes of total planned time**.

The application was also tested through a public HTTPS address using a Cloudflare Quick Tunnel. That address is temporary: it only works while the local container and tunnel are running.

## High Distinction · CSV Study Report

A non-web Python tool that reads study tasks from a CSV file, calculates the total time, prints a summary to the container logs, and saves a text report. The application runs as a non-root user.

The input file is `hd-app/data/tasks.csv` and must contain `task` and `minutes` columns:

```csv
task,minutes
Reading,50
Coding,75
Revision,25
```

Build the image, then mount the local data folder into the container:

```powershell
docker build -t hd-csv-report:1.0 .\hd-app
$dataPath = (Resolve-Path .\hd-app\data).Path
docker run --name hd-report --mount "type=bind,source=$dataPath,target=/data" hd-csv-report:1.0
```

Check the completed container, logs, and saved output:

```powershell
docker ps -a --filter "name=hd-report"
docker logs hd-report
Get-Content .\hd-app\data\summary.txt
```

The example input produces **3 tasks and 150 total minutes**. The container completes with exit code `0`, and `summary.txt` remains in the host folder after the container stops.

To run the container again using the same name:

```powershell
docker rm hd-report
```

## Project files

```text
credit-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore

distinction-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore

hd-app/
├── report.py
├── Dockerfile
├── .dockerignore
└── data/
    └── tasks.csv
```

The accompanying submission report contains the step-by-step workflow, Docker commands, screenshots, container logs, and verification results for all four levels.
