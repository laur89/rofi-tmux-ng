Usage
=====

Few things to keep in mind when using rft:

#. rft has a daemon component that needs to be started after tmux server and i3wm,
   assuming you're using it.
#. to interact with the daemon, you can either use the ``rft`` CLI program, or
   send signals to daemon for switching session or window.
#. rft doesn't launch a terminal/client automatically for you, so you need to start
   your main tmux client manually.
#. rft caches the last tmux session/window you have switched from either using rft
   or in tmux client itself, so it automatically pre-selects it in the rofi prompt,
   given the client window is visible; if it is not, rft assumes you probably want
   to switch over to the same session/window that is currently active.

Daemon
------

As mentioned above, rft has a daemon service that needs to be started for rft client
to be functional. It's best to configure it via your OS service manager. E.g.
with systemd it's recommended to create a user service file similar to this:

.. code:: shell

    $ cat ~/.config/systemd/user/rofi-tmux.service

    [Unit]
    Description=rofi-tmux aka rft
    BindsTo=i3wm.service tmux.service
    After=i3wm.service tmux.service

    [Service]
    Type=simple
    ExecStart=%h/.local/bin/rft-daemon
    Restart=on-failure
    RestartSec=2

    [Install]
    WantedBy=graphical-session.target

Note this assumes you also have `i3wm.service` & `tmux.service` which will be
started before rofi-tmux.

If you choose to start it yourself, just run ``rft-daemon`` in shell.

.. note::

    If you haven't added ``$HOME/.local/bin`` to your ``$PATH``, then you'll have to
    define rft or rft-daemon commands as ``$HOME/.local/bin/rft``, as that's where
    pipx-installed executables are placed by default.


Client
------

I recommend that you have shortcuts with control modifiers for rft, so if you always
have a tmux session running, it's going to be really fast to find this session and
switch to it. For example, I use these key bindings on i3 for launching rft:

.. code:: shell

    set $mod Mod4
    set $ex  exec --no-startup-id

    bindsym $mod+w       $ex  killall -s SIGUSR1 rft-daemon
    bindsym $mod+e       $ex  killall -s SIGUSR2 rft-daemon
    bindsym $mod+g       $ex  rft sw --global_scope false
    bindsym $mod+Shift+w $ex  rft kw

The first two are the ones that I use the most. They're for switching to a session
(`ss`) and switching to a window globally (`sw`).
To check all rft actions available:

.. code:: shell

  ❯ rft
  Usage: rft [OPTIONS] COMMAND [ARGS]...

    RFT (rofi-tmux) switcher.

  Options:
    --debug BOOLEAN  Enables logging at debug level.
    --help           Show this message and exit.

  Commands:
    ks  Kill tmux session.
    kw  Kill tmux window.
    ss  Switch tmux session.
    sw  Switch tmux window.
    v   Print version.

Screencast
----------

Watch this screencast to see rft in action:

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="//www.youtube.com/embed/o6tBNFJW28c" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>
