import logging

import uvicorn

logger: logging.Logger = logging.getLogger(__name__)

def start_uvicorn() -> None:
    logger.info("Starting Uvicorn")

    host = "0.0.0.0"
    port = 8080
    workers = 1
    log_level = logging.INFO

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,
        log_level=log_level,
        use_colors=True,
        access_log=True,
    )
