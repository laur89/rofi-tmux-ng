#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .window_manager import WindowManager
import i3ipc
import logging
from re import escape
from subprocess import check_output
from collections import defaultdict
import time

class aobject(object):
    """Inheriting this class allows you to define an async __init__.

    So you can create objects by doing something like `await MyClass(params)`
    """
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass

class i3WM(WindowManager):
    """Abstraction to handle i3wm"""

    def __init__(self, conf, logger_lvl = None) -> None:

        """Constructor

        """
        start_time = time.time()
        self._i3 = i3ipc.Connection()
        self._cur_ws_id = self._get_cur_workspace()
        self._conf = conf
        self.logger = logging.getLogger(__name__)
        if logger_lvl != None:
            self.logger.setLevel(logger_lvl)

        super(i3WM, self).__init__()
        print('i3wm constructor took {}'.format(time.time() - start_time))

    def focus_tmux_window(self, session) -> None:
        """Focuses window where given tmux session is running in

        :session: tmux session whose window to focus

        """
        start_time = time.time()
        if not session:
            return None

        tmux_win = self._find_tmux_window(session)
        if tmux_win:
            self.logger.debug('i3 focusing window running tmux session [{}]'.format(session.name))
            tmux_win.command('focus')
        print('focussing took {}'.format(time.time() - start_time))

    def is_tmux_win_visible(self, session) -> bool:
        """Verifies if window where given tmux session is running in is visible

        :session: tmux session whose visibility to check

        """
        start_time = time.time()
        if not session:
            return False

        tmux_win = self._find_tmux_window(session)
        if tmux_win:
            return self._is_win_visible(tmux_win)
        print('is_visible took {}'.format(time.time() - start_time))
        return False

    def _is_win_visible(self, i3_win) -> bool:
        """Verify if given i3ipc.Con housing our tmux session is visible on our
        screen(s).

        :i3_win: i3ipc.Con housing tmux session whose visibility to test.

        """
        try:
            start_time = time.time()
            xprop = check_output(['xprop', '-id', str(i3_win.window)]).decode()
            print('xprop took {}'.format(time.time() - start_time))
            return '_NET_WM_STATE_HIDDEN' not in xprop
        except FileNotFoundError:
            # if xprop not found, fall back to just checking if tmux win is on our current worksapce:
            self.logger.debug('xprop utility is not found - please install it.')
            self.logger.debug('will decide visibility simply by checking if tmux is on our current workspace')
            return self._is_tmux_win_on_current_ws(i3_win)

    def _is_tmux_win_on_current_ws(self, i3_win) -> bool:
        """Verifies if tmux is in the current (ie focused) i3 workspace

        :i3_win: i3ipc.Con housing our tmux session

        """
        workspace = i3_win.workspace()
        return workspace and workspace.id == self._cur_ws_id

    def _get_cur_workspace(self) -> int:
        """Finds & returns the id of current (ie focused) workspace.

        """
        return self._i3.get_tree().find_focused().workspace().id

    def _find_tmux_window(self, session) -> i3ipc.Con:
        """Finds and returns i3 Container instance housing tmux window that's
        currently attached to provided session.

        :session: tmux session whose window to find.

        """
        start_time = time.time()
        session_name = escape(session.name)
        window_name = escape(session.attached_window.name)
        rgx = self._conf['tmux_title_rgx'].format_map(defaultdict(str,
                session = session_name,
                window = window_name
        ))

        tmux_win = self._i3.get_tree().find_named(rgx)
        # just in case filter by container type - we want regular & floating window containers:
        tmux_win = list(filter(lambda c: c.type.endswith('con'), tmux_win))

        if tmux_win:
            if len(tmux_win) > 1:
                self.logger.debug('found [{}] windows using regex [{}], but expected 1'
                        .format(len(tmux_win), rgx))
                self.logger.debug('you should likely make conf.tmux_title_rgx more limiting')
            print('_find_tmux_win took {}'.format(time.time() - start_time))
            return tmux_win[0]

        self.logger.debug('found no windows using regex [{}]'.format(rgx))
        print('_find_tmux_win took {}'.format(time.time() - start_time))
        return None

