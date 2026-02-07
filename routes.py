"""API Routes - Simple endpoints for infrastructure monitoring."""

from fastapi import APIRouter, Depends
from datetime import datetime
import psutil
import platform
import socket

from auth import get_current_user

router = APIRouter()


# ==================== Public Routes (No login needed) ====================

@router.get("/api/home", tags=["General"])
def home():
    """Home endpoint. No authentication required."""
    return {"message": "Welcome to SOX Compliance Monitor API"}


@router.get("/api/health", tags=["General"])
def health_check():
    """Check if the API is running. No authentication required."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


# ==================== Protected Routes (Login required) ====================

@router.get("/api/system-info", tags=["Monitoring"])
def get_system_info(current_user: dict = Depends(get_current_user)):
    """Get basic system information. Requires login."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "requested_by": current_user["username"],
    }


@router.get("/api/cpu", tags=["Monitoring"])
def get_cpu(current_user: dict = Depends(get_current_user)):
    """Get CPU usage. Requires login."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_cores": psutil.cpu_count(),
    }


@router.get("/api/memory", tags=["Monitoring"])
def get_memory(current_user: dict = Depends(get_current_user)):
    """Get memory usage. Requires login."""
    mem = psutil.virtual_memory()
    return {
        "memory_percent": mem.percent,
        "total_gb": round(mem.total / (1024**3), 2),
        "used_gb": round(mem.used / (1024**3), 2),
        "free_gb": round(mem.available / (1024**3), 2),
    }


@router.get("/api/disk", tags=["Monitoring"])
def get_disk(current_user: dict = Depends(get_current_user)):
    """Get disk usage. Requires login."""
    disk = psutil.disk_usage("/")
    return {
        "disk_percent": disk.percent,
        "total_gb": round(disk.total / (1024**3), 2),
        "used_gb": round(disk.used / (1024**3), 2),
        "free_gb": round(disk.free / (1024**3), 2),
    }


@router.get("/api/metrics", tags=["Monitoring"])
def get_all_metrics(current_user: dict = Depends(get_current_user)):
    """Get all system metrics in one call. Requires login."""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "timestamp": datetime.now().isoformat(),
        "hostname": socket.gethostname(),
        "cpu_percent": cpu,
        "memory_percent": mem.percent,
        "disk_percent": disk.percent,
        "requested_by": current_user["username"],
    }


@router.get("/api/compliance", tags=["Compliance"])
def check_compliance(current_user: dict = Depends(get_current_user)):
    """Run a simple SOX compliance check. Requires login."""
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
        "checked_by": current_user["username"],
    }
