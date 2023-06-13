import logging
from logging.handlers import TimedRotatingFileHandler
import time
import sys


ts = time.strftime('%Y%m%d-%H%M%S')
fname = f'test_logging_{ts}.log'


# -------- Case 1 -------
# using basicConfig w/o key of handlers
# logging to a file
# -----------------------
# logging.basicConfig(
#     filename=fname,
#     level=logging.INFO,
#     format='[%(asctime)s] %(module)-20s %(levelname)-8s %(message)s'
# )
# logger = logging.getLogger(__name__)


# -------- Case 2 -------
# using basicConfig w/o key of handlers
# logging to console
# -----------------------
# logging.basicConfig(
#     stream=sys.stdout,
#     # sys.stderr is used when stream is not specified
#     level=logging.DEBUG,
#     format='[%(asctime)s] %(module)-20s %(levelname)-8s %(message)s'
# )
# logger = logging.getLogger(__name__)


# -------- case 3 -------
# using basicConfig w/ key of handlers
# logging to console
# -----------------------
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(name)-20s %(levelname)-8s %(message)s',
#     handlers=[
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)


# -------- case 4 -------
# adding handlers to logger
# logging to console AND a file
# NOTE: the logger has to be set a level explictly,
# otherwise the default level (WARNING) will be used
# -----------------------
# clog_format = logging.Formatter('%(name)-20s %(levelname)-8s %(message)s')
# flog_format = logging.Formatter(
#     '[%(asctime)s] %(module)-20s %(levelname)-8s %(message)s')

# c_handler = logging.StreamHandler(sys.stdout)
# c_handler.setLevel(logging.DEBUG)
# c_handler.setFormatter(clog_format)

# f_handler = logging.FileHandler(fname)
# f_handler.setLevel(logging.DEBUG)
# f_handler.setFormatter(flog_format)

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.addHandler(c_handler)
# logger.addHandler(f_handler)


# -------- case 5 -------
# using basicConfig w/ key of handlers
# logging to console AND file, each with its own level and format
# NOTE: the logger has to be set a level explictly,
# otherwise the default level (WARNING) will be used
# -----------------------
# clog_format = logging.Formatter('%(name)-10s %(levelname)-8s %(message)s')
# flog_format = logging.Formatter(
#     '[%(asctime)s] %(module)-20s %(levelname)-8s %(message)s')

# c_handler = logging.StreamHandler()
# c_handler.setLevel(logging.ERROR)
# c_handler.setFormatter(clog_format)

# f_handler = logging.FileHandler(fname)
# f_handler.setLevel(logging.INFO)
# f_handler.setFormatter(flog_format)
# logging.basicConfig(
#     level=logging.NOTSET,
#     handlers=[
#         c_handler,
#         f_handler
#     ]
# )
# logger = logging.getLogger(__name__)


# -------- case 6 -------
# recommended practice
#
# use TimedRotatingFileHandler
# -----------------------
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                              '%(message)s')
LOG_FILE = 'my_log.log'


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.INFO)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when='midnight', backupCount=30)
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's nto necessary to propagate the error up to parent
    logger.propagate = False
    return logger


logger = get_logger('my_log')


# Now we use our logger object instead of logging
logger.debug('debug')
logger.info('info')
logger.warning('warning')
logger.error('error')
logger.critical('critical'' long line')


class MyObj:
    def __init__(self) -> None:
        pass

    def met(self):
        logger.debug('debug msg')


def test():
    my_obj = MyObj()
    my_obj.met()


def main():
    pass


if __name__ == '__main__':
    pass
    # breakpoint()
    # MyObj().met()

    # c_handler = logging.StreamHandler()
    # c_handler.setLevel(logging.DEBUG)

    # print(c_handler.level)

    # fname = 'log.log'
    # f_handler = logging.FileHandler(fname)
    # print(f_handler.level)
    # f_handler.setLevel(logging.INFO)
    # print(f_handler.level)
=======
""" A collection of differnet types of logging

Also refer to Python HOWTOs - Logging Cookbook:
https://docs.python.org/3/howto/logging-cookbook.html#\
using-concurrent-futures-processpoolexecutor
"""
from concurrent.futures import ThreadPoolExecutor
import logging
import os
from random import randint
import time

# console logging handler
clog_format = logging.Formatter(
    '[%(asctime)s] %(name)-10s %(levelname)-8s %(message)s')
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_handler.setFormatter(clog_format)


def create_logger(dir_log: str, logger_total: int) -> dict[logging.Logger]:
    """Creates a list of loggers with a file handler

    Args:
        dir_log: the directory for log files
        logger_total: total number of loggers to create

    Returns:
        a dict of created loggers
    """
    loggers = {}

    for i in range(logger_total):
        ts = time.strftime('%Y%m%d-%H%M%S')
        logger_name = f'Logger{i:02}'
        fn_log = os.path.join(dir_log, f'{logger_name}_{ts}.log')
        flog_format = logging.Formatter(
            '[%(asctime)s] %(name)s %(levelname)-8s %(message)s')
        f_handler = logging.FileHandler(fn_log)
        f_handler.setLevel(logging.DEBUG)
        f_handler.setFormatter(flog_format)

        loggers[i] = logging.getLogger(logger_name)
        loggers[i].setLevel(logging.DEBUG)
        loggers[i].addHandler(f_handler)
        loggers[i].addHandler(c_handler)

    return loggers


def foo(logger: logging.Logger, time_total: int = 10, time_step: int = 1
        ) -> None:
    """Generates logs in a loop

    Args:
        logger (logging.Logger): a logger to generate logs
        time_total (int, optional): the total time in seconds for the loop.
            Defaults to 100.
        # time_step (int, optional): the time interval in seconds for
        #     each loop steps. Defaults to 10.

    Returns:
        None

    Raises:
        AnyError: If anything bad happens
    """
    time_passed = 0
    while_count = 0
    while time_passed < time_total:
        time_step = randint(1, int(time_total / 2))
        time.sleep(time_step)
        logger.info(f'Loop#{while_count}: slept {time_step}s')

        time_passed += time_step
        while_count += 1


def main():
    def logging_serial():
        """Logging in serial
        """
        for i in range(logger_total):
            foo(logger=loggers[i])

    def logging_parallel():
        """Logging in parallel
        """
        with ThreadPoolExecutor(logger_total) as executor:
            _ = [executor.submit(foo, loggers[i]) for i in range(len(loggers))]

    logger_total = 3
    loggers = create_logger(os.path.join(os.getcwd(), 'logs'),
                            logger_total=logger_total)

    # logging_serial()
    logging_parallel()


if __name__ == '__main__':
    main()
