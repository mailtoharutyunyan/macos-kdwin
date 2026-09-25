# KDWin Keyboards for macOS

KDWin-style phonetic keyboards for Mac: **Armenian KDWin** 🇦🇲 and **Russian KDWin** 🇷🇺.

## Install

Open Terminal and run:

```sh
curl -fsSL https://raw.githubusercontent.com/mailtoharutyunyan/KDWin-Keyboards/main/get.sh | bash
```

macOS only loads new keyboards at login. If the installer says so, log out, log
back in, and run the same command again to turn them on.

Switch keyboards with **Ctrl+Space** or the flag in the menu bar.

Or from a clone: `git clone https://github.com/mailtoharutyunyan/KDWin-Keyboards && cd KDWin-Keyboards && ./install.sh`

## Layouts

| Key | ` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | - | = |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Armenian | ՝ | է | թ | փ | ձ | ջ | ւ | և | ր | չ | ճ | - | ժ |
| Russian | ч | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | - | ю |

| Key | q | w | e | r | t | y | u | i | o | p | [ | ] | \ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Armenian | ք | ո | ե | ռ | տ | ը | ւ | ի | օ | պ | խ | ծ | շ |
| Russian | я | в | е | р | т | ы | у | и | о | п | ш | щ | э |

| Key | a | s | d | f | g | h | j | k | l | ; | ' |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Armenian | ա | ս | դ | ֆ | գ | հ | յ | կ | լ | ; | ՛ |
| Russian | а | с | д | ф | г | х | й | к | л | ; | ' |

| Key | z | x | c | v | b | n | m | , | . | / |
|---|---|---|---|---|---|---|---|---|---|---|
| Armenian | զ | ղ | ց | վ | բ | ն | մ | , | ։ | / |
| Russian | з | ь | ц | ж | б | н | м | , | . | / |

- **Shift** types capitals (Armenian Shift+`,` `.` `/` give « » ՞; Russian Shift+`,` `.` give ъ Ъ).
- **Option (⌥)** types plain English, so digits and symbols are always one key away.
- **⌘ and Ctrl** shortcuts (⌘C, ⌘V, Ctrl+C in Terminal) work as on the English keyboard.

## Change a key

Edit the `ARMENIAN` or `RUSSIAN` table in `build.py`, then:

```sh
./build.py && ./install.sh
```

Log out and back in for the change to take effect.

## Uninstall

```sh
~/Library/Application\ Support/KDWin-Keyboards/uninstall.sh
```

(or `./uninstall.sh` from a clone)

## About the "developer can access anything you type" warning

macOS shows it in Input Sources for every keyboard not made by Apple, and it can't
be turned off. These layouts are plain XML key maps (see `layouts/*.keylayout`)
with no code, so they cannot read or send what you type.
