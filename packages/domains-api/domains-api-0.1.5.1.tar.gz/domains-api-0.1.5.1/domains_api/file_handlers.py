import logging
import pickle
import sys
import os
from pathlib import Path


class FileHandlers:
    def __init__(self, path='/var/www/domains-api'):
        self.log_level = self.set_log_level()
        self.path, self.op_sys = self.file_handling(path)
        self.user_file = os.path.abspath(self.path / 'domains.user')
        self.log_file = os.path.abspath(self.path / 'domains.log')
        if not os.path.exists(self.log_file) or not os.path.exists(self.user_file):
            try:
                if self.op_sys == 'nt':
                    self.make_directories()
                else:
                    self.make_directories()
                    self.set_permissions(self.path)
                    self.own_log, self.sys_log = self.initialize_loggers()
                    self.set_permissions(self.log_file)
            except (PermissionError, FileNotFoundError, KeyError) as e:
                print(e)
                print('Run with sudo first time to set permissions')
                sys.exit(1)
        else:
            self.own_log, self.sys_log = self.initialize_loggers()

    @staticmethod
    def file_handling(path):
        if os.name == 'nt':
            path = Path(os.getenv('LOCALAPPDATA')) / path
            op_sys = 'nt'
        else:
            path = Path(path)
            op_sys = 'pos'
        return path, op_sys

    def make_directories(self):
        os.makedirs(self.path, exist_ok=True)

    @staticmethod
    def set_permissions(path, gid=33):
        if os.geteuid() == 0:
            try:
                os.chown(path, int(os.environ['SUDO_GID']), gid)
                if os.path.isdir(path):
                    os.chmod(path, 0o770)
                elif os.path.isfile(path):
                    os.chmod(path, 0o665)
            except KeyError as e:
                raise e
        else:
            try:
                os.chown(path, int(os.getuid()), gid)
                if os.path.isdir(path):
                    os.chmod(path, 0o770)
                elif os.path.isfile(path):
                    os.chmod(path, 0o665)
            except PermissionError as e:
                raise e

    def initialize_loggers(self):
        sys_log = logging.getLogger('domains_api')
        own_log = logging.getLogger(__name__)
        if self.log_level == 'debug':
            sys_log.setLevel(logging.DEBUG)
        elif self.log_level == 'warning':
            sys_log.setLevel(logging.WARNING)
        else:
            sys_log.setLevel(logging.INFO)
        own_log.setLevel(logging.WARNING)
        fh = logging.FileHandler(self.log_file)
        sh = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(levelname)s]|%(asctime)s|%(message)s',
                                      datefmt='%d %b %Y %H:%M:%S')
        sh_formatter = logging.Formatter('[%(levelname)s]|[%(name)s]|%(asctime)s| %(message)s',
                                         datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        sh.setFormatter(sh_formatter)
        sys_log.addHandler(sh)
        own_log.addHandler(fh)
        sys_log.debug('Loggers initialized')
        return own_log, sys_log

    def log(self, msg, level='info'):
        if level == 'info':
            self.sys_log.info(msg)
        elif level == 'debug':
            self.sys_log.debug(msg)
        elif level == 'warning':
            self.sys_log.warning(msg)
            self.own_log.warning(msg)

    def set_log_level(self, level='info'):
        self.log_level = level
        return self.log_level

    def save_user(self, user):

        """Pickle (serialize) user instance."""

        with open(self.user_file, 'wb') as pickle_file:
            pickle.dump(user, pickle_file)
        self.log('User saved.', 'debug')

    @staticmethod
    def load_user(user_file):

        """Unpickle (deserialize) user instance."""

        with open(user_file, 'rb') as pickle_file:
            return pickle.load(pickle_file)

    def delete_user(self):

        """Delete pickle file (serialized user instance)."""

        if input('Are you sure? (Y/n): ').lower() != 'n':
            os.remove(self.user_file)

    def clear_logs(self):
        with open(self.log_file, 'r') as r:
            lines = r.readlines()
            if len(lines) > 100:
                tail = r.readlines()[-10:]
                with open(self.log_file, 'w') as w:
                    w.writelines(tail)


if __name__ == '__main__':
    fhs = FileHandlers()
    fhs.log('Testing', 'info')
