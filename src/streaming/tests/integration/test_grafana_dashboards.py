"""Test Grafana dashboards."""
import json
import pytest
from pathlib import Path


DASHBOARDS_DIR = Path("monitoring/grafana/dashboards")


def test_system_overview_dashboard_exists():
    """Test system overview dashboard file exists."""
    dashboard_path = DASHBOARDS_DIR / "system-overview.json"
    assert dashboard_path.exists()


def test_application_metrics_dashboard_exists():
    """Test application metrics dashboard file exists."""
    dashboard_path = DASHBOARDS_DIR / "application-metrics.json"
    assert dashboard_path.exists()


def test_business_metrics_dashboard_exists():
    """Test business metrics dashboard file exists."""
    dashboard_path = DASHBOARDS_DIR / "business-metrics.json"
    assert dashboard_path.exists()


def test_system_overview_dashboard_valid_json():
    """Test system overview dashboard is valid JSON."""
    dashboard_path = DASHBOARDS_DIR / "system-overview.json"
    with open(dashboard_path) as f:
        data = json.load(f)
    
    assert "dashboard" in data
    assert data["dashboard"]["title"] == "GT-Vision - System Overview"
    assert len(data["dashboard"]["panels"]) == 4


def test_application_metrics_dashboard_valid_json():
    """Test application metrics dashboard is valid JSON."""
    dashboard_path = DASHBOARDS_DIR / "application-metrics.json"
    with open(dashboard_path) as f:
        data = json.load(f)
    
    assert "dashboard" in data
    assert data["dashboard"]["title"] == "GT-Vision - Application Metrics"
    assert len(data["dashboard"]["panels"]) == 5


def test_business_metrics_dashboard_valid_json():
    """Test business metrics dashboard is valid JSON."""
    dashboard_path = DASHBOARDS_DIR / "business-metrics.json"
    with open(dashboard_path) as f:
        data = json.load(f)
    
    assert "dashboard" in data
    assert data["dashboard"]["title"] == "GT-Vision - Business Metrics"
    assert len(data["dashboard"]["panels"]) == 8


def test_all_dashboards_have_refresh():
    """Test all dashboards have refresh interval."""
    dashboards = [
        "system-overview.json",
        "application-metrics.json",
        "business-metrics.json"
    ]
    
    for dashboard_file in dashboards:
        dashboard_path = DASHBOARDS_DIR / dashboard_file
        with open(dashboard_path) as f:
            data = json.load(f)
        
        assert "refresh" in data["dashboard"]
        assert data["dashboard"]["refresh"] == "5s"
