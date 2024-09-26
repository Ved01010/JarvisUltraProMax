import psutil


def get_system_info():
    """Fetches system information such as CPU usage and memory availability."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    return (f"CPU Usage: {cpu_usage}%\n"
            f"Memory Available: {memory.available // (1024 * 1024)} MB\n"
            f"Memory Used: {memory.used // (1024 * 1024)} MB\n"
            f"Memory Total: {memory.total // (1024 * 1024)} MB")
