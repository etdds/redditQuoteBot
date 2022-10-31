import logging


def setup_logger(level: int, logname: str = ""):
    """Setup logging

    Args:
        level (int): Log level, use logging module levels (i.e, logging.INFO)
        logname (str, optional): Filename to log to, if not supplied logs, to stdout
    """
    if logname != "":
        logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s %(name)s [%(levelname)s]: %(message)s',
                            datefmt='%H:%M:%S',
                            level=level)
    else:
        logging.basicConfig(
            format='%(asctime)s %(name)s [%(levelname)s]: %(message)s',
            datefmt='%H:%M:%S',
            level=level)
