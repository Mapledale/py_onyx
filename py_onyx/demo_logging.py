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
