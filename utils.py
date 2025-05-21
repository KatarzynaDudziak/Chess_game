import logging, coloredlogs


def get_logger(name: str) -> logging.Logger:
    coloredlogs.install(level=logging.DEBUG)
    logger = logging.getLogger(name)
    logger.info("Information: ")
    logger.debug("Debug: ")
    logger.warning("Warning: ")
    return logger

logger = get_logger(__name__)

def is_move_valid(pawn, current_pos, new_pos, check_handler, turn) -> bool:
    if pawn.can_move(current_pos, new_pos):
        if board.get_piece(new_pos) == EMPTY_SQUARE:
            if self.is_piece_move_valid(pawn, current_pos, new_pos, check_handler, turn):
                return True
            else:
                logger.debug(f"Invalid piece move")
        else:
            logger.debug(f"Target pos is not empty")
    else:
        logger.debug(f"{pawn} cannot move")
    return False