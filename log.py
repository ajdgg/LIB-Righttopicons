import time
import logging
from pathlib import Path
from file_handle import xj_file_handle

dayt = time.strftime('%Y-%m-%d', time.localtime())


def x_log(value: str, logtype: str):
    logging.basicConfig(filename=Path(__file__).resolve().parent / f'log/{dayt}.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    if logtype == 'info':
        logging.info(value)
    elif logtype == 'debug':
        logging.debug(value)
    elif logtype == 'warning':
        logging.warning(value)
    elif logtype == 'error':
        logging.error(value)
    elif logtype == 'critical':
        logging.critical(value)

    # logging.debug('这是一条debug信息')
    # logging.info('这是一条info信息')
    # logging.warning('这是一条warning信息')
    # logging.error('这是一条error信息')
    # logging.critical('这是一条critical信息')


class XJ_Log:
    def __init__(self):
        pass

    def w_log(self, conten: str, logtype: str = 'info'):
        try:
            log_data = xj_file_handle.read_filenames_with_pathlib('log')
        except FileNotFoundError:
            path_obj = Path('log')
            path_obj.mkdir(parents=True, exist_ok=True)
            log_data = []
        if log_data == []:
            with open(Path(__file__).resolve().parent / f'log/{dayt}.log', 'w', encoding='utf-8'):
                pass
            x_log(conten, logtype)
            return
        x_log(conten, logtype)


if __name__ == '__main__':
    XJ_Log().w_log('test', 'error')
