# Sprint 12 - Observabilidade (Prometheus + Grafana)

**Data**: 2025-01-15  
**Status**: 📋 PLANEJADA  
**Duração**: 5 dias  
**Objetivo**: Sistema completo de observabilidade com métricas, dashboards e alertas

---

## 🎯 Visão Geral

Implementar observabilidade completa do sistema usando Prometheus para coleta de métricas e Grafana para visualização e alertas.

---

## 📊 Escopo

### Métricas a Coletar

#### 1. Métricas de Sistema
- CPU usage
- Memory usage
- Disk I/O
- Network I/O

#### 2. Métricas de Aplicação
- Request rate (req/s)
- Response time (p50, p95, p99)
- Error rate (%)
- Active connections

#### 3. Métricas de Negócio
- Streams ativos
- Gravações em andamento
- Eventos LPR/hora
- Câmeras online/offline

#### 4. Métricas de Infraestrutura
- PostgreSQL connections
- Redis hit rate
- RabbitMQ queue size
- MinIO storage usage

---

## 🔧 Prometheus - Configuração

### 1. prometheus.yml

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'gtvision-prod'
    environment: 'production'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

# Load rules once and periodically evaluate them
rule_files:
  - "alerts/*.yml"

# Scrape configurations
scrape_configs:
  # Backend (Django)
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  # Streaming (FastAPI)
  - job_name: 'streaming'
    static_configs:
      - targets: ['streaming:8001']
    metrics_path: '/metrics'

  # AI (FastAPI)
  - job_name: 'ai'
    static_configs:
      - targets: ['ai:8002']
    metrics_path: '/metrics'

  # PostgreSQL
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  # Redis
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  # RabbitMQ
  - job_name: 'rabbitmq'
    static_configs:
      - targets: ['rabbitmq:15692']

  # Node Exporter (system metrics)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  # MediaMTX
  - job_name: 'mediamtx'
    static_configs:
      - targets: ['mediamtx:9998']
```

### 2. Alerts (alerts/system.yml)

```yaml
groups:
  - name: system_alerts
    interval: 30s
    rules:
      # High CPU
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is above 80% (current: {{ $value }}%)"

      # High Memory
      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is above 85% (current: {{ $value }}%)"

      # Disk Space
      - alert: LowDiskSpace
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 15
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Disk space is below 15% (current: {{ $value }}%)"
```

### 3. Alerts (alerts/application.yml)

```yaml
groups:
  - name: application_alerts
    interval: 30s
    rules:
      # High Error Rate
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.job }}"
          description: "Error rate is above 5% (current: {{ $value }}%)"

      # Slow Response Time
      - alert: SlowResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Slow response time on {{ $labels.job }}"
          description: "P95 response time is above 1s (current: {{ $value }}s)"

      # Service Down
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"
```

### 4. Alerts (alerts/business.yml)

```yaml
groups:
  - name: business_alerts
    interval: 1m
    rules:
      # No Active Streams
      - alert: NoActiveStreams
        expr: gtvision_active_streams == 0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "No active streams"
          description: "There are no active streams for 10 minutes"

      # High Camera Offline Rate
      - alert: HighCameraOfflineRate
        expr: (gtvision_cameras_offline / gtvision_cameras_total) > 0.2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High camera offline rate"
          description: "More than 20% of cameras are offline"

      # Recording Failures
      - alert: RecordingFailures
        expr: rate(gtvision_recording_errors_total[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High recording failure rate"
          description: "Recording failures detected"
```

---

## 📊 Grafana - Dashboards

### 1. Dashboard: System Overview

```json
{
  "dashboard": {
    "title": "GT-Vision - System Overview",
    "panels": [
      {
        "title": "CPU Usage",
        "targets": [
          {
            "expr": "100 - (avg(irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Memory Usage",
        "targets": [
          {
            "expr": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Disk Usage",
        "targets": [
          {
            "expr": "100 - ((node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100)"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Network I/O",
        "targets": [
          {
            "expr": "rate(node_network_receive_bytes_total[5m])",
            "legendFormat": "RX"
          },
          {
            "expr": "rate(node_network_transmit_bytes_total[5m])",
            "legendFormat": "TX"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

### 2. Dashboard: Application Metrics

```json
{
  "dashboard": {
    "title": "GT-Vision - Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (job)"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Response Time (P95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Active Connections",
        "targets": [
          {
            "expr": "sum(http_connections_active) by (job)"
          }
        ],
        "type": "stat"
      }
    ]
  }
}
```

### 3. Dashboard: Business Metrics

```json
{
  "dashboard": {
    "title": "GT-Vision - Business Metrics",
    "panels": [
      {
        "title": "Active Streams",
        "targets": [
          {
            "expr": "gtvision_active_streams"
          }
        ],
        "type": "stat"
      },
      {
        "title": "Recordings in Progress",
        "targets": [
          {
            "expr": "gtvision_recordings_active"
          }
        ],
        "type": "stat"
      },
      {
        "title": "LPR Events/Hour",
        "targets": [
          {
            "expr": "rate(gtvision_lpr_events_total[1h]) * 3600"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Cameras Status",
        "targets": [
          {
            "expr": "gtvision_cameras_online",
            "legendFormat": "Online"
          },
          {
            "expr": "gtvision_cameras_offline",
            "legendFormat": "Offline"
          }
        ],
        "type": "piechart"
      }
    ]
  }
}
```

---

## 🔌 Instrumentação - FastAPI

### 1. Prometheus Middleware

```python
"""Prometheus metrics middleware for FastAPI."""
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request, Response
from time import time

# Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

http_connections_active = Gauge(
    'http_connections_active',
    'Active HTTP connections'
)

# Business metrics
gtvision_active_streams = Gauge('gtvision_active_streams', 'Active streams')
gtvision_recordings_active = Gauge('gtvision_recordings_active', 'Active recordings')
gtvision_lpr_events_total = Counter('gtvision_lpr_events_total', 'Total LPR events')
gtvision_cameras_online = Gauge('gtvision_cameras_online', 'Online cameras')
gtvision_cameras_offline = Gauge('gtvision_cameras_offline', 'Offline cameras')


async def prometheus_middleware(request: Request, call_next):
    """Prometheus metrics middleware."""
    http_connections_active.inc()
    start_time = time()
    
    response = await call_next(request)
    
    duration = time() - start_time
    
    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    http_connections_active.dec()
    
    return response


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type="text/plain")
```

### 2. Business Metrics Helper

```python
"""Business metrics helper."""
from prometheus_client import Gauge, Counter

class BusinessMetrics:
    """Business metrics helper."""
    
    @staticmethod
    def update_active_streams(count: int):
        """Update active streams count."""
        gtvision_active_streams.set(count)
    
    @staticmethod
    def update_active_recordings(count: int):
        """Update active recordings count."""
        gtvision_recordings_active.set(count)
    
    @staticmethod
    def increment_lpr_events():
        """Increment LPR events counter."""
        gtvision_lpr_events_total.inc()
    
    @staticmethod
    def update_cameras_status(online: int, offline: int):
        """Update cameras status."""
        gtvision_cameras_online.set(online)
        gtvision_cameras_offline.set(offline)
```

---

## 🐳 Docker Compose - Atualização

```yaml
# Prometheus
prometheus:
  image: prom/prometheus:latest
  ports:
    - "9090:9090"
  volumes:
    - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    - ./monitoring/alerts:/etc/prometheus/alerts
    - prometheus_data:/prometheus
  command:
    - '--config.file=/etc/prometheus/prometheus.yml'
    - '--storage.tsdb.path=/prometheus'
    - '--web.console.libraries=/usr/share/prometheus/console_libraries'
    - '--web.console.templates=/usr/share/prometheus/consoles'
  networks:
    - gtvision

# Grafana
grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_USER=admin
    - GF_SECURITY_ADMIN_PASSWORD=admin
    - GF_INSTALL_PLUGINS=grafana-piechart-panel
  volumes:
    - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
    - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    - grafana_data:/var/lib/grafana
  networks:
    - gtvision

# Alertmanager
alertmanager:
  image: prom/alertmanager:latest
  ports:
    - "9093:9093"
  volumes:
    - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml
  command:
    - '--config.file=/etc/alertmanager/alertmanager.yml'
  networks:
    - gtvision

# Node Exporter
node-exporter:
  image: prom/node-exporter:latest
  ports:
    - "9100:9100"
  networks:
    - gtvision

# PostgreSQL Exporter
postgres-exporter:
  image: prometheuscommunity/postgres-exporter:latest
  environment:
    - DATA_SOURCE_NAME=postgresql://gtvision:gtvision_password@postgres:5432/gtvision?sslmode=disable
  ports:
    - "9187:9187"
  networks:
    - gtvision

# Redis Exporter
redis-exporter:
  image: oliver006/redis_exporter:latest
  environment:
    - REDIS_ADDR=redis:6379
  ports:
    - "9121:9121"
  networks:
    - gtvision

volumes:
  prometheus_data:
  grafana_data:
```

---

## 📝 Checklist de Implementação

### Prometheus
- [ ] Configurar prometheus.yml
- [ ] Criar alerts (system, application, business)
- [ ] Configurar scrape configs
- [ ] Testar coleta de métricas

### Grafana
- [ ] Configurar datasource (Prometheus)
- [ ] Criar dashboard System Overview
- [ ] Criar dashboard Application Metrics
- [ ] Criar dashboard Business Metrics
- [ ] Configurar alertas

### Instrumentação
- [ ] Adicionar middleware Prometheus (FastAPI)
- [ ] Adicionar métricas de negócio
- [ ] Endpoint /metrics em todos os serviços
- [ ] Testar coleta

### Alertmanager
- [ ] Configurar alertmanager.yml
- [ ] Configurar notificações (Slack/Email)
- [ ] Testar alertas

### Exporters
- [ ] Node Exporter (system)
- [ ] PostgreSQL Exporter
- [ ] Redis Exporter
- [ ] RabbitMQ metrics

---

## 🚀 Ordem de Implementação

1. **Prometheus** (1 dia)
   - Configuração
   - Alerts
   - Scrape configs

2. **Grafana** (1 dia)
   - Dashboards
   - Datasources
   - Alertas

3. **Instrumentação** (2 dias)
   - Middleware
   - Business metrics
   - Endpoints /metrics

4. **Exporters** (0.5 dia)
   - Node, PostgreSQL, Redis
   - Validação

5. **Validação** (0.5 dia)
   - Testes
   - Documentação

**Total**: ~5 dias

---

## 📊 Métricas de Sucesso

- ✅ Prometheus coletando métricas
- ✅ 3 dashboards Grafana funcionando
- ✅ Alertas configurados
- ✅ Todos os serviços instrumentados
- ✅ Exporters funcionando
- ✅ Documentação completa

---

**Status**: 📋 GUIA COMPLETO - Pronto para implementação
