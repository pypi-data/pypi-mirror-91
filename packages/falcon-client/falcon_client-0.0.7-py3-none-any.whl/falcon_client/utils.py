# -*- coding: utf-8 -*-
import logging
import sys
from pathlib import Path, PosixPath
from configparser import ConfigParser


def set_default_logger(logger_name=None, logger_level=logging.DEBUG, propagate=False):
    if logger_name is None:
        logger = logging.getLogger(__name__)
    else:
        logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)
    logger.propagate = propagate
    return logger


def add_logger_streamhandler(logger=set_default_logger(), logger_level=logging.INFO, log_format=None, log_filter=None):
    """
    :param logger: Logging instance
    :param logger_level: Log verbosity level
    :param log_format: Log format string
    :param log_filter: logging.Filter object
    :return: logging.Logger
    """
    if format is None:
        _format = logging.Formatter(u"%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    else:
        _format = logging.Formatter(log_format)
    try:
        handler = logging.StreamHandler()
        handler.set_name("{}_stream".format(logger.name))
        handler.setLevel(logger_level)
        if log_filter is not None:
            handler.addFilter(log_filter)
    except Exception as e:
        print("Failed to set logger (%s).  Falling back to defaults." % e)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
    else:
        handler.setFormatter(_format)
        logger.addHandler(handler)
        return logger


def add_logger_filehandler(logger=set_default_logger(), logger_level=logging.INFO, filename='default.log',
                           log_format=None, log_filter=None):
    """
    add a file log handler to an existing logger
    :param logger: Typically, name of calling module
    :param logger_level: Log verbosity level
    :param filename: log output filename
    :param log_format: Log output format
    :param log_filter: Logging Filter object
    :return: logging.Logger
    """
    if format is None:
        _format = logging.Formatter(u"%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    else:
        _format = logging.Formatter(log_format)
    try:
        fh = logging.FileHandler(filename)
        fh.set_name("{}_file".format(logger.name))
        fh.setLevel(logger_level)
        fh.setFormatter(_format)
        if log_filter is not None:
            fh.addFilter(log_filter)
        logger.addHandler(fh)
    except Exception as e:
        logger.error("Failed to set %s as log file handler. Error: %s" % (filename, e))
    finally:
        return logger


def add_logger_splunkhandler(logger=set_default_logger(), log_filter=None, **kwargs):
    """
    Handler for writing logs to Splunk index.
    :param logger: logging instance
    :param log_filter: logging Filter object
    :param kwargs: Splunk configuration options
    :return: logger with Splunk Handler attached
    """
    try:
        from splunk_hec_handler import SplunkHecHandler
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except Exception as err:
        logger.warning("Failed to add Splunk log handler. Error: %s" % err)
        return logger
    else:
        try:
            host = kwargs.pop('host')
            token = kwargs.pop('token')
            level = kwargs.pop('level') if 'level' in kwargs.keys() else 'INFO'
            sh = SplunkHecHandler(host, token, **kwargs)
            sh.set_name("{}_splunk".format(logger.name))
        except Exception as err:
            logger.warning("Failed to add Splunk log handler.  Error: %s" % err)
            raise err
        else:
            sh.setLevel(level)
            if log_filter is not None:
                sh.addFilter(log_filter)
            logger.addHandler(sh)
    return logger


# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch14s08.html
def whoami():
    return sys._getframe(1).f_code.co_name


def callersname():
    return sys._getframe(2).f_code.co_name


def get_config(default_section, config_file=None):
    """
    A generic function to read configuration files for a service and return a configparser object
    :param default_section: name of service for which configuration is requested (str)
    :param config_file: path to the configuration file. (str)
    :return: ConfigParser object
    """
    try:
        api_config = ConfigParser(default_section=default_section.lower())
        config_file_path = Path(config_file).expanduser()
    except:
        raise

    try:
        if config_file_path.exists():
            api_config.read_file(config_file_path.open('r', encoding='utf-8', errors='replace'))
        else:
            raise FileNotFoundError("Configuration file ('%s') not found." % config_file)
    except:
        raise
    else:
        return api_config