# Local Service Broker

A CLI tool that spins up containerized backing services on your local machine — a
self-hosted, single-node alternative to a managed service broker.

Pick the services you need from an interactive prompt, answer a couple of questions
(host port, password), and the tool generates a `docker-compose.yml` and brings
everything up, complete with an observability stack wired in.

## Services

- PostgreSQL
- MySQL
- Redis
- Nginx

Each service gets its own host port mapping (so a port already taken
isn't a problem) and joins a shared bridge network.

## Observability

A second Compose stack runs alongside the generated one:

- **Prometheus** — scrapes `postgres_exporter` and `node_exporter`
- **Grafana** — datasources and dashboards provisioned from disk
- **Loki** — log storage
- **Exporters** — `postgres_exporter` (database metrics), `node_exporter` (host metrics)

Grafana dashboards are defined as code in `grafana/dashboards.py` using the
Grafana Foundation SDK and compiled to provisioned JSON, so panels are
version-controlled rather than clicked together in the UI.

## Stack

Python 3.12 (`StrEnum`, dataclasses, PEP 695 generics, `abc`) · Docker ·
Docker Compose · Docker SDK for Python · Prometheus · Grafana ·
Grafana Foundation SDK · Loki

## Layout

| Path | Purpose |
|---|---|
| `main.py` | Interactive prompt, service definitions, Compose generation |
| `container_runtime.py` | Abstract runtime interface (leaves room for Podman) |
| `docker_runtime.py` | Docker implementation — dependency check, up, inspect, health |
| `kill_all.py` | Tears down both stacks |
| `docker-compose.yml` | Observability stack |
| `generated/docker_compose.yml` | Generated service stack (output) |
| `grafana/dashboards.py` | Dashboards as code |
| `prometheus/prometheus.yml` | Scrape config |

## Usage

```bash
uv run python main.py    # select services, answer prompts, containers come up
uv run python kill_all.py # tear everything down

Grafana at localhost:3000, Prometheus at localhost:9090.
