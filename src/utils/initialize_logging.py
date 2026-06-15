import logging

def initialize_logging() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger("DynatraceExecutionLogs")
    logger.setLevel(logging.INFO)

    return logger