# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer
from libqtile.utils import guess_terminal

#Guess terminal
terminal = guess_terminal()

# Get the number of connected screens
def get_monitors():
    xr = subprocess.check_output('xrandr --query | grep " connected"', shell=True).decode().split('\n')
    monitors = len(xr) - 1 if len(xr) > 2 else len(xr)
    return monitors


monitors = get_monitors()

# Run autorandr --change and restart Qtile on screen change
@hook.subscribe.screen_change
def set_screens(event):
    subprocess.run(["autorandr", "--change"])
    qtile.restart()


#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# Most of our keybindings are in sxhkd file - except these

# SUPER + FUNCTION KEYS
    
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.hide_show_bar(), desc="Toggle bar visibility"),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),

# SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "d", lazy.spawn('rofi -show combi -combi-modes "window,run,ssh,drun" -modes combi'), desc='Run Launcher'),
    Key([mod, "shift"], "Return", lazy.spawn("thunar"), desc='Run FileManager'),

# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

# FOR AZERTY KEYBOARDS
#group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

#GROUP APPS
group_apps = [
             ["Chromium", "WebApp-Guacamoleneth4987"],
             ["firefox", "qutebrowser"],
             ["anydesk", "r-viewer"],
             ["subl", "emacs"],
             ["feh", "ristretto"],
             ["spotify", "Spotify","Spotube" "vlc", "freetube", "FreeTube"],
             ["gimp", "inkscape"],
             ["thunar ", "Thunar"],
             ["Signal", "TelegramDesktop", "zulip", "electron-mail", "WebApp-GoogleMessages8025"],
             ["Thunderbird", "Mail"],
                ]
#group_labels = [" 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 ", " 0 ",]
#group_labels = ["₁", " ₂", " ₃", "₄", " ₅", " ₆", "₇", " ₈", " ₉", " ₀",]
group_labels = ["GUAC ₁", "FRF ₂", "RMT ₃", "TRM₄", "IMG ₅", "VID ₆", "SCR ₇", "FMG ₈", "CHT ₉", "MAIL ₀",]
#group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["bsp", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "matrix", "monadtall",]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
            matches=[Match(wm_class=group_apps[i])])
        )

for i in groups:
    keys.extend([

#CHANGE WORKSPACES AND MONITOR
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        # Key([mod], "Tab", lazy.screen.next_group()),
        # Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        # Key(["mod1"], "Tab", lazy.screen.next_group()),
        # Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
        Key([mod], 'period', lazy.next_screen(), desc='Next monitor'),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#5e81ac",
            "border_normal": "#4c566a"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(margin=10, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadWide(margin=10, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
    ]

# COLORS FOR THE BAR
#Theme name : ArcoLinux Default
def init_colors():
    return [["#2F343F", "#2F343F"], # color 0
            ["#2F343F", "#2F343F"], # color 1
            ["#c0c5ce", "#c0c5ce"], # color 2
            ["#fba922", "#fba922"], # color 3
            ["#3384d0", "#3384d0"], # color 4
            ["#f3f4f5", "#f3f4f5"], # color 5
            ["#cd1f3f", "#cd1f3f"], # color 6
            ["#62FF00", "#62FF00"], # color 7
            ["#6790eb", "#6790eb"], # color 8
            ["#a9a9a9", "#a9a9a9"]] # color 9


colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize = 12,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
            widget.GroupBox(
                        font="FontAwesome",
                        disable_drag = True,
                        active = colors[5],
                        highlight_method = "line",
                        highlight_color = colors[0],
                        this_current_screen_border = colors[3],
                        foreground = colors[2],
                        background = colors[1],
                        ),
               widget.CurrentLayout(
                       fmt = ' [{}] ',
                        ),
               widget.Spacer(
                length = bar.STRETCH,
                        ),
               #widget.WindowTabs(),
               widget.Clock(
                        format="%d %b %H:%M "
                        ),
               widget.CheckUpdates(
                        distro = "Arch_checkupdates",
                        display_format = "●",
                        foreground = colors[3],
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('pamac-manager --updates')},
                        ),
               widget.Spacer(
                length = bar.STRETCH,
                        ),
              # widget.Battery(
              #          charge_char = '▲',
              #          discharge_char = '▼',
              #          format = '[Bt] {char} {percent:2.0%} ',
              #          mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('xfce4-power-manager-settings')},
              #              ),
              # widget.DF(
              #          visible_on_warn=False,
              #          format =' [Dc] {r:.0f}% ',
              #          mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('gnome-disks')},
              #          ),
              # widget.Memory(
              #         mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('alacritty -e htop')},
              #         format=" [Rm] {MemPercent: .0f}% ",
              #         ),
              # widget.CPU(
              #         format=' [Pr] {load_percent: .0f}% '
              #          ),
              # widget.PulseVolume(
              #          fmt = ' [Vl] {}     '
              #              ),
               widget.TextBox(' '),
               widget.Systray(),
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_no_systray():
    widgets_screen1 = init_widgets_list()
    # Remove Systray from screen1
    last_widget = len(widgets_screen1) - 1
    del widgets_screen1[last_widget]
    return widgets_screen1

def init_widgets_with_systray():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

#widgets_screen1 = init_widgets_no_systray()
#widgets_screen2 = init_widgets_with_systray()

screens = []

for monitor in range(monitors):
    if monitor == 0:
        screens.append(
                Screen(
                    top=bar.Bar(widgets=init_widgets_with_systray(), size=24, opacity=0.7,
                                margin=[10, 10, 0, 10],) # Margin = N E S W
                    ))
    else:
        screens.append(
                Screen(
                   top=bar.Bar(widgets=init_widgets_no_systray(), size=24, opacity=0.7,
                               margin=[10, 10, 0, 10],
                               )  # Margin = N E S W
                    ))


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-tweak-tool.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='arcolinux-logout'),
    Match(wm_class='xfce4-terminal'),
    Match(wm_class='SpeedCrunch'),

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "smart" # or smart or focus

wmname = "LG3D"
