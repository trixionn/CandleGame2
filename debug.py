import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class DebugFlags:
    enabled: bool = False
    show_rects: bool = False
    show_hitboxes: bool = False
    show_fps: bool = False
    log_events: bool = False

flags = DebugFlags()

def configure(enabled: bool) -> None:
    flags.enabled = enabled
    logging.basicConfig(
        level=logging.DEBUG if enabled else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    if enabled:
        logger.info("Debug mode enabled")
