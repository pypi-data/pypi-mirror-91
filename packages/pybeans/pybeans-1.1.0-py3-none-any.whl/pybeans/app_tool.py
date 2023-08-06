import os, sys, logging
from os import path
from email.utils import formataddr
from collections.abc import Iterable
from logging import handlers
import functools
import time
import re
from typing import Union

from .utils import deep_merge, send_email, get
from .exception import AppToolError


class MySMTPHandler(handlers.SMTPHandler):
    def getSubject(self, record):
        #all_formatter = logging.Formatter(fmt='%(name)s - %(levelno)s - %(levelname)s - %(pathname)s - %(filename)s - %(module)s - %(lineno)d - %(funcName)s - %(created)f - %(asctime)s - %(msecs)d  %(relativeCreated)d - %(thread)d -  %(threadName)s -  %(process)d - %(message)s ')        
        #print('Ex. >>> ',all_formatter.formatMessage(record))

        #help(record)
        #help(formatter)
        
        formatter = logging.Formatter(fmt=self.subject)
        return formatter.formatMessage(record)


class AppTool(object):
    def __init__(self, app_name: str, app_path: str, local_config_dir: str='', config_name: str='config', ignore_env:bool=False):
        self._app_name = app_name
        self._app_path = app_path
        self._config = {}
        self._logger = None

        self.load_config(local_config_dir, config_name)
        self.init_logger()


    @property
    def config(self):
        return self._config


    @property
    def logger(self):
        return self._logger


    def _use_env_var(self, config: dict, parent_key: str) -> dict:
        """Replace config variable with env

        Args:
            config (dict): config dict
            parent_key (str, optional): parent key (connected by dot). Defaults to ''.

        Returns:
            dict: result
        """
        if type(config) is tuple:
            config = list(config)

        if type(config) is dict:
            for key in config.keys():
                full_key = (parent_key + '_' + re.sub(r'\W+', '_', key)).upper()
                #print(full_key)
                if full_key in os.environ.keys():
                    config[key] = os.environ.get(full_key)
                elif type(config[key]) in (list, dict, tuple):
                    config[key] = self._use_env_var(config[key], full_key)
        elif type(config) is list:
            for index, _ in enumerate(config):
                full_key = (parent_key + '_' + str(index)).upper()
                #print(full_key)
                if full_key in os.environ.keys():
                    config[index] = os.environ.get(full_key)
                elif type(config[index]) in (list, dict, tuple):
                    config[index] = self._use_env_var(config[index], full_key)
        return config


    def load_config(self, local_config_dir: str = '', config_name: str='config', read_env:bool=True) -> dict:
        """Load config locally then replace some with env value if NOT ignore_env
        NOTE! 
            - env key of config key will be UPPER of APP_NAME and KEY_NAMEs (connected by '_')
            - ANY char which is NOT A-Za-z0-9_ , that's say \\w in re, will be replaced by '_'
            Ex. a.b             -> APP_A
                a.b[0][1].e'    -> APP_A_B_0_1_E

        Keyword Arguments:
            local_config_dir {str} -- Dir name of local config files. (default: {''})
        
        Returns:
            [dict] -- Merged config dictionary.
        """
        assert(type(local_config_dir) == str)

        sys.path.append(self._app_path)
        try:
            self._config = __import__(config_name).CONFIG
        except Exception:
            self._config = {}

        config_local_path = path.join(self._app_path, local_config_dir)
        sys.path.append(config_local_path)
        try:
            config_local = __import__(config_name + '_local').CONFIG
            self._config = deep_merge(self._config, config_local)
        except Exception:
            pass
        
        regular_app_name = re.sub(r'\W+', '_', self._app_name.upper())
        env_key = regular_app_name + '_ENV'        
        env = os.environ.get(env_key)
        
        if env:
            try:
                config_test = __import__(config_name + f'_{env}').CONFIG
                self._config = deep_merge(self._config, config_test)
            except Exception:
                pass
        
        if read_env:
            self._use_env_var(self._config, regular_app_name)
        return self._config


    def init_logger(self) -> logging.Logger:
        """Initialize logger
        
        Returns:
            [logger] -- Initialized logger.
        """

        smtp = self._config.get('smtp')
        mail = self._config.get('mail')
        logConfig = self._config.get('log', {})

        logs_path = path.join(self._app_path, 'logs')
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)

        logger = logging.getLogger(self._app_name)
        logLevel = logConfig.get('level', logging.DEBUG)
        logger.setLevel(logLevel)

        logDest = logConfig.get('dest', {})

        fileDest = logDest.get('file')
        if str(fileDest) == '1':
            regular_log_name = re.sub(r'\W+', '_', self._app_name.lower())
            rf_handler = handlers.TimedRotatingFileHandler(path.join(logs_path, f'{regular_log_name}.log'), when='D', interval=1, backupCount=7)
            rf_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
            rf_handler.level = logging.INFO
            rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            logger.addHandler(rf_handler)

        mailDest = logDest.get('mail')
        if smtp and str(mailDest) != '0':
            from_addr = mail.get('from')
            #TODO: Use schema to validate smtp
            if str(mailDest) == '1':
                to_addrs = mail.get('to')
            else:   # Ex. 'Henry TIAN <chariothy@gmail.com>'
                to_addrs = mailDest

            mail_handler = MySMTPHandler(
                    mailhost = (smtp['host'], smtp['port']),
                    fromaddr = from_addr,
                    toaddrs = to_addrs,
                    subject = '%(name)s - %(levelname)s - %(message)s',
                    credentials = (smtp['user'], smtp['pwd']))
            mail_handler.setLevel(logging.ERROR)
            logger.addHandler(mail_handler)

        stdoutDest = logDest.get('stdout')
        if str(stdoutDest) == '1':
            st_handler = logging.StreamHandler()
            st_handler.level = logging.DEBUG
            st_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            logger.addHandler(st_handler)
        self._logger = logger
        return logger


    def send_email(self, subject: str, text_body: str='', from_addr: str=None, to_addrs:str=None, html_body: str=None, 
        image_paths: tuple=None, file_paths: tuple=None, 
        debug: bool=False, send_to_file: bool=False, email_file_dir=None) -> dict:
        """A shortcut of global send_email
        """
        smtp = self._config.get('smtp')
        #TODO: Use schema to validate smtp_config
        assert smtp
        assert text_body or html_body
        
        mail = self._config.get('mail')
        mail_from = from_addr if from_addr else mail['from']
        mail_to = to_addrs if to_addrs else mail['to']
        return send_email(mail_from, mail_to, subject, 
            text_body=text_body, 
            smtp_config=smtp, 
            html_body=html_body,
            image_paths=image_paths,
            file_paths=file_paths,
            debug=debug,
            send_to_file=send_to_file,
            email_file_dir=email_file_dir
        )


    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)


    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)


    def warn(self, msg, *args, **kwargs):
        self._logger.warn(msg, *args, **kwargs)


    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)


    def err(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)


    def exception(self, msg, *args, **kwargs):
        self._logger.exception(msg, *args, **kwargs)


    def ex(self, msg, *args, **kwargs):
        self._logger.exception(msg, *args, **kwargs)


    def fatal(self, msg, *args, **kwargs):
        self._logger.fatal(msg, *args, **kwargs)


    def log(self, throw=False, message=''):
        """Decorator
        !!! Should be decorated first to avoid being shielded by other decorators, such as @click.
        
        Keyword Arguments:
            throw {bool} -- Re-raise exception (default: {False})
            message {str} -- Specify message
        
        Raises:
            ex: Original exception
        
        Example:
            @log()
            def func():
                pass

            @log(True)
            def func():
                pass

            @log(message='foo')
            def func():
                pass
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kw):
                try:
                    return func(*args, **kw)
                except Exception as ex:
                    self._logger.exception(message if message else str(ex))
                    if throw:
                        raise ex
            return wrapper
        return decorator


    def get(self, key:str, default=None, check:bool=False, replacement_for_dot_in_key:str='#'):
        return get(self._config, key, default, check, replacement_for_dot_in_key)


    def __getitem__(self, key):
        return self.get(key, replacement_for_dot_in_key='#', check=True)