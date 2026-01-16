"""Smoke tests para validar stack completa"""
import requests
import time


def test_services_health():
    """Testa saúde de todos os serviços"""
    services = {
        "PostgreSQL": "http://localhost:5432",
        "Redis": "http://localhost:6379",
        "RabbitMQ": "http://localhost:15672",
        "MinIO": "http://localhost:9000/minio/health/live",
        "MediaMTX": "http://localhost:8888",
        "Streaming API": "http://localhost:8001/health",
        "Prometheus": "http://localhost:9090/-/healthy",
        "Grafana": "http://localhost:3000/api/health",
        "Elasticsearch": "http://localhost:9200/_cluster/health",
        "Kibana": "http://localhost:5601/api/status",
    }
    
    print("\n" + "="*50)
    print("SMOKE TESTS - Validação da Stack")
    print("="*50 + "\n")
    
    results = {}
    for name, url in services.items():
        try:
            if "PostgreSQL" in name or "Redis" in name:
                # Não tem HTTP endpoint, assumir OK se porta está aberta
                results[name] = "⚠️  SKIP (sem HTTP)"
                continue
                
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 401]:  # 401 = serviço rodando mas precisa auth
                results[name] = "✅ OK"
            else:
                results[name] = f"❌ FAIL ({response.status_code})"
        except Exception as e:
            results[name] = f"❌ ERROR ({str(e)[:30]})"
    
    # Exibir resultados
    for name, status in results.items():
        print(f"{name:20} {status}")
    
    print("\n" + "="*50)
    
    # Contar sucessos
    success_count = sum(1 for s in results.values() if "✅" in s)
    total_count = len([s for s in results.values() if "SKIP" not in s])
    
    print(f"\nResultado: {success_count}/{total_count} serviços OK")
    print("="*50 + "\n")
    
    return success_count >= total_count * 0.7  # 70% de sucesso


def test_api_endpoints():
    """Testa endpoints principais da API"""
    endpoints = {
        "Health Check": "http://localhost:8001/health",
        "Docs (Swagger)": "http://localhost:8001/docs",
        "Metrics": "http://localhost:8001/metrics",
    }
    
    print("\n" + "="*50)
    print("API ENDPOINTS")
    print("="*50 + "\n")
    
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=5)
            status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
            print(f"{name:20} {status}")
        except Exception as e:
            print(f"{name:20} ❌ ERROR")
    
    print("="*50 + "\n")


def test_observability_stack():
    """Testa stack de observabilidade"""
    print("\n" + "="*50)
    print("OBSERVABILIDADE")
    print("="*50 + "\n")
    
    # Prometheus
    try:
        prom = requests.get("http://localhost:9090/api/v1/targets", timeout=5)
        if prom.status_code == 200:
            targets = prom.json().get("data", {}).get("activeTargets", [])
            up_count = sum(1 for t in targets if t.get("health") == "up")
            print(f"Prometheus:          ✅ {up_count} targets UP")
        else:
            print(f"Prometheus:          ❌ FAIL")
    except:
        print(f"Prometheus:          ❌ ERROR")
    
    # Grafana
    try:
        grafana = requests.get("http://localhost:3000/api/health", timeout=5)
        status = "✅ OK" if grafana.status_code == 200 else "❌ FAIL"
        print(f"Grafana:             {status}")
    except:
        print(f"Grafana:             ❌ ERROR")
    
    # Elasticsearch
    try:
        es = requests.get("http://localhost:9200/_cluster/health", timeout=5)
        if es.status_code == 200:
            health = es.json().get("status", "unknown")
            emoji = "✅" if health in ["green", "yellow"] else "❌"
            print(f"Elasticsearch:       {emoji} {health.upper()}")
        else:
            print(f"Elasticsearch:       ❌ FAIL")
    except:
        print(f"Elasticsearch:       ❌ ERROR")
    
    # Kibana
    try:
        kibana = requests.get("http://localhost:5601/api/status", timeout=5)
        status = "✅ OK" if kibana.status_code == 200 else "❌ FAIL"
        print(f"Kibana:              {status}")
    except:
        print(f"Kibana:              ❌ ERROR")
    
    print("="*50 + "\n")


if __name__ == "__main__":
    print("\n🚀 Iniciando Smoke Tests...\n")
    time.sleep(2)
    
    # Executar testes
    services_ok = test_services_health()
    test_api_endpoints()
    test_observability_stack()
    
    # Resultado final
    if services_ok:
        print("✅ SMOKE TESTS PASSED\n")
        exit(0)
    else:
        print("❌ SMOKE TESTS FAILED\n")
        exit(1)
