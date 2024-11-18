[![Documentation Status](https://readthedocs.org/projects/rofi-tmux/badge/?version=latest)](http://rofi-tmux.readthedocs.io/en/latest/?badge=latest) [![PyPI](https://img.shields.io/pypi/v/rofi-tmux.svg)](https://pypi.python.org/pypi/rofi-tmux)

## rft (rofi-tmux)

![rft](docs/images/rft.png)

Quickly switch tmux sessions & windows via rofi. Integrates with [i3wm](https://i3wm.org/)
for a smoother switching workflow, if you have multiple workspaces.

### Use Case

I developed rft (rofi-tmux) to optimize my context-switching workflow. As a user who
relies completely on tmux for anything shell related, I wanted to have a fuzzy finder
switcher to locate any tmux session or window with seamless integration with i3wm.
I guess I've got spoiled by fuzzy finders. Watch the screencast below and you'll see
what I mean :)

### Features

- Switch or kill any tmux session
- Switch or kill any tmux window, either globally or within the current session
- Switch to any tmuxinator project
- Cache last tmux session and window for fast switching back and forth,
decreases the number of required keystrokes
- Integration with i3wm for switching to the right workspace seamlessly
- Extensible for other window managers

### Installation

```sh
pipx install rofi-tmux-ng
```

### Screencast

[![rft-demo](https://img.youtube.com/vi/o6tBNFJW28c/0.jpg)](https://www.youtube.com/watch?v=o6tBNFJW28c)

### Usage

Check [ReadTheDocs](http://rofi-tmux.readthedocs.io/) for detailed information,
usage and suggested key bindings.

### Contributing

Contributions are more than welcome. Let me know if you want to add other features
or integrations, or if you are having trouble to use rft, open an issue.
Join the [chat on gitter.im/rofi-tmux/community](https://gitter.im/rofi-tmux/community)
if you want to discuss ideas.

### License

MIT
