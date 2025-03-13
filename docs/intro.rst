Introduction
============

.. image:: images/rft.png

Quickly switch tmux sessions and windows via `rofi <https://github.com/davatorium/rofi>`_.
Integrates with `i3wm <http://www.i3wm.org>`_ for a smoother switching workflow
if you have multiple workspaces.

Use Case
--------

Rft (rofi-tmux) was developed to optimize context-switching workflow. As a user who
relies completely on tmux for anything shell related, I wanted to have a fuzzy finder
switcher to locate any tmux session or window with seamless integration with i3wm.

Features
--------

- Switch or kill any tmux session.
- Switch or kill any tmux window, either globally or within the current session.
- :strike:`Switch to any tmuxinator project.`
- Cache last tmux session and window for fast switching back and forth,
  decreases the number of keystrokes needed.
- Integration with i3wm for focusing the right workspace & window seamlessly.
- Extensible for other window managers.
