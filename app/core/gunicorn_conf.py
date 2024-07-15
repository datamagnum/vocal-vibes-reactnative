import json
import logging
import multiprocessing
import os
import sys

from loguru import logger

from app.core.config import settings

# from app.utils.logger import InterceptHandler, StubbedGunicornLogger

# ref: https://guide.biznetgio.dev/guide/gunicorn/
# logging.root.setLevel(settings.LOG_LEVEL)

seen = set()
# for name in [
#     *logging.root.manager.loggerDict.keys(),
#     "gunicorn",
#     "gunicorn.access",
#     "gunicorn.error",
#     "uvicorn",
#     "uvicorn.access",
#     "uvicorn.error",
# ]:
#     if name not in seen:
#         seen.add(name.split(".")[0])
#         logging.getLogger(name).handlers = [intercept_handler]

# logger.configure(
#     handlers=[{"sink": sys.stdout, "serialize": settings.json_logging_enabled}]
# )

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
max_workers_str = os.getenv("MAX_WORKERS")
use_max_workers = None
if max_workers_str:
    use_max_workers = int(max_workers_str)
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8000")
bind_env = os.getenv("BIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")
if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)
    if use_max_workers:
        web_concurrency = min(web_concurrency, use_max_workers)
accesslog_var = os.getenv("ACCESS_LOG", "-")
use_accesslog = accesslog_var or None
errorlog_var = os.getenv("ERROR_LOG", "-")
use_errorlog = errorlog_var or None
graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
timeout_str = os.getenv("TIMEOUT", "120")
keepalive_str = os.getenv("KEEP_ALIVE", "5")
max_requests_jitter = os.getenv("MAX_REQUESTS_JITTER", 0)
workers = os.getenv("WORKERS", (2 * cores) + 1)
threads = os.getenv("THREADS", (2 * cores) + 1)

# Gunicorn config variables
loglevel = use_loglevel
# logger_class = StubbedGunicornLogger

worker_connections = 1000
bind = use_bind
errorlog = use_errorlog
accesslog = use_accesslog
graceful_timeout = int(graceful_timeout_str)
timeout = int(timeout_str)
keepalive = int(keepalive_str)

# For debugging and testing
log_data = {
    "cores": cores,
    "loglevel": loglevel,
    "workers": workers,
    "threads": threads,
    "worker_connections": worker_connections,
    "bind": bind,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "keepalive": keepalive,
    "errorlog": errorlog,
    "accesslog": accesslog,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "use_max_workers": use_max_workers,
    "max_requests_jitter": max_requests_jitter,
    "host": host,
    "port": port,
}
logger.info(log_data)
