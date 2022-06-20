__version__ = '0.2.6'
__description__ = 'zipapp utilities'
__app_name__ = 'zipapp-utils'

try:
    from logging_utils_tddschn import get_logger

    logger, _ = get_logger(__app_name__)
except:
    import logging
    from logging import NullHandler

    logger = logging.getLogger(__app_name__)
    logger.addHandler(NullHandler())


class EntryPointNotFoundError(Exception):
    pass


class ProjectNameNotFoundError(Exception):
    pass
