"""API Routes - Simple endpoints for infrastructure monitoring."""

from fastapi import APIRouter
from datetime import datetime
import psutil
import platform
import socket

router = APIRouter()


# ==================== Health Check ====================

@router.get("/", tags=["General"])
def home():
    """Home endpoint."""
    return {"message": "Welcome to SOX Compliance Monitor API"}


@router.get("/health", tags=["General"])
def health_check():
    """Check if the API is running."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


# ==================== System Info ====================

@router.get("/api/system-info", tags=["Monitoring"])
def get_system_info():
    """Get basic system information."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
    }


# ==================== CPU ====================

@router.get("/api/cpu", tags=["Monitoring"])
def get_cpu():
    """Get CPU usage."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_cores": psutil.cpu_count(),
    }


# ==================== Memory ====================

@router.get("/api/memory", tags=["Monitoring"])
def get_memory():
    """Get memory usage."""
    mem = psutil.virtual_memory()
    return {
        "memory_percent": mem.percent,
        "total_gb": round(mem.total / (1024**3), 2),
        "used_gb": round(mem.used / (1024**3), 2),
        "free_gb": round(mem.available / (1024**3), 2),
    }


# ==================== Disk ====================

@router.get("/api/disk", tags=["Monitoring"])
def get_disk():
    """Get disk usage."""
    disk = psutil.disk_usage("/")
    return {
        "disk_percent": disk.percent,
        "total_gb": round(disk.total / (1024**3), 2),
        "used_gb": round(disk.used / (1024**3), 2),
        "free_gb": round(disk.free / (1024**3), 2),
    }


# ==================== All Metrics ====================

@router.get("/api/metrics", tags=["Monitoring"])
def get_all_metrics():
    """Get all system metrics in one call."""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "timestamp": datetime.now().isoformat(),
        "hostname": socket.gethostname(),
        "cpu_percent": cpu,
        "memory_percent": mem.percent,
        "disk_percent": disk.percent,
    }


# ==================== SOX Compliance Check ====================

@router.get("/api/compliance", tags=["Compliance"])
def check_compliance():
    """Run a simple SOX compliance check."""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    checks = [
        {
            "check": "CPU Usage",
            "value": f"{cpu}%",
            "threshold": "85%",
            "status": "PASS" if cpu < 85 else "FAIL",
        },
        {
            "check": "Memory Usage",
            "value": f"{mem.percent}%",
            "threshold": "90%",
            "status": "PASS" if mem.percent < 90 else "FAIL",
        },
        {
            "check": "Disk Usage",
            "value": f"{disk.percent}%",
            "threshold": "80%",
            "status": "PASS" if disk.percent < 80 else "FAIL",
        },
    ]

    passed = sum(1 for c in checks if c["status"] == "PASS")
    total = len(checks)

    return {
        "report_time": datetime.now().isoformat(),
        "score": f"{passed}/{total}",
        "overall": "COMPLIANT" if passed == total else "NON-COMPLIANT",
        "checks": checks,
    }
