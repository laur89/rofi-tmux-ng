import os
import json
from datetime import datetime

STATE_VER = 1  # bump this whenever persisted state data structure changes
TIME_DIFF_DELTA_THRESHOLD_S = 10


CONF_DIR: str = os.environ.get("XDG_CONFIG_HOME", f"{os.environ['HOME']}/.config")


RUNTIME_PATH: str = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
CACHE_PATH: str = os.environ.get("XDG_CACHE_HOME", os.environ["HOME"] + "/.cache")

EMPTY_STATE = {
        'timestamp': 0,
        'ver': -1,
        'tmux': {}
        }


def load_config(load_state=False) -> dict:
    """Load json config file XDG_CONFIG_HOME/rofi-tmux/config.json

    Currently supported window managers: 'i3'

    """
    conf = {
            'wm': 'i3',
            'tmux_title_rgx': '{session}',
            'ignored_sessions': [],
            'sw_signals': ['SIGUSR1'],
            'ss_signals': ['SIGUSR2'],
            'socket_path': f"{RUNTIME_PATH}/rofi-tmux-ipc.sock",
            'state_f_path': f'{CACHE_PATH}/rofi-tmux.state',
            'state': None,  # will be read from state_f_path
            'tmux_cc_cmd': ["tmux", "-C", "attach", "-f",
                            "no-output,no-detach-on-destroy,ignore-size,active-pane"]  # note single -C flag as per https://github.com/tmux/tmux/issues/3085
    }
    conf.update(_read_dict_from_file(os.path.join(CONF_DIR, 'rofi-tmux', 'config.json')))

    if load_state:
        conf['state'] = _load_state(conf['state_f_path'])

    # self.logger.debug('effective config: {}'.format(conf))
    return conf


def _load_state(file_loc) -> dict:
    s = _read_dict_from_file(file_loc)

    t = s.get('timestamp', 0)
    v = s.get('ver', -1)
    if (_unix_time_now() - t <= TIME_DIFF_DELTA_THRESHOLD_S and v == STATE_VER):
        return s
    return EMPTY_STATE.copy()


def write_state(conf, tmux_state) -> None:
    data = {
            'timestamp': _unix_time_now(),
            'ver': STATE_VER,
            'tmux': tmux_state
            }

    try:
        with open(conf['state_f_path'], 'w') as f:
            f.write(
                json.dumps(
                    data,
                    indent=4,
                    sort_keys=True,
                    separators=(',', ': '),
                    ensure_ascii=False))
        # self.logger.debug('wrote cache: {}'.format(self._cache))
    except IOError as e:
        raise e


def _read_dict_from_file(file_loc) -> dict:
    if not (os.path.isfile(file_loc) and os.access(file_loc, os.R_OK)):
        return {}

    try:
        with open(file_loc, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f'error trying to read file {file_loc}')
        return {}


def _unix_time_now() -> int:
    return int(datetime.now().timestamp())


