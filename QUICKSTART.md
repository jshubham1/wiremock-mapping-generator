# Quick Start Guide

## 🚀 Development Environment

### Recommended: Hybrid Setup
Start WireMock in Docker + Web UI locally (best performance, no SSL issues):
```bash
make dev-hybrid
```

### Alternative: Full Docker Setup
Start everything in Docker containers:
```bash
make dev
```

Both will start:
- **Web UI** at http://localhost:5001
- **WireMock server** at http://localhost:8080  
- **WireMock admin** at http://localhost:8080/__admin

## 📋 Common Commands

| Command | Description |
|---------|-------------|
| `make dev-hybrid` | Start hybrid development (recommended) |
| `make dev` | Start full Docker development |
| `make start` | Start all services in background |
| `make stop` | Stop all services |
| `make restart` | Restart all services |
| `make status` | Show service status |
| `make logs` | Watch live logs |
| `make health` | Check service health |
| `make clean` | Clean up everything |

## 🔧 Individual Services

| Command | Description |
|---------|-------------|
| `make wiremock` | Start only WireMock server |
| `make web-local` | Start only Web UI locally |
| `make web` | Start only Web UI in Docker |

## 🔧 Workflow

1. **Setup** (first time):
   ```bash
   make setup
   ```

2. **Start development**:
   ```bash
   make dev-hybrid    # Recommended
   # OR
   make dev           # Full Docker
   ```

3. **Upload API specs** via Web UI at http://localhost:5001

4. **Test endpoints** using the enhanced modal in the Web UI

5. **View logs** (in another terminal):
   ```bash
   make logs
   ```

6. **Stop when done**:
   ```bash
   make stop
   ```

## 🌐 URLs

- **Web UI**: http://localhost:5001
- **WireMock API**: http://localhost:8080  
- **WireMock Admin**: http://localhost:8080/__admin

## 🐛 Troubleshooting

- **Check status**: `make status`
- **Check health**: `make health`
- **View logs**: `make logs`
- **Clean restart**: `make clean && make dev-hybrid`

## ⚡ Performance Tips

- Use `make dev-hybrid` for better performance (local Web UI, Docker WireMock)
- Use `make web-local` if WireMock is already running
- Use `make clean` periodically to remove unused Docker resources
