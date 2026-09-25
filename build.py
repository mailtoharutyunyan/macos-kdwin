#!/usr/bin/env python3
"""Builds KDWin-style Armenian and Russian phonetic keyboard layouts, plus a US
English layout with a US flag, for macOS.

Output: layouts/*.keylayout + flag *.icns (installed by install.sh).
Option (⌥) and Command (⌘) layers type plain US English, so shortcuts and
digits always work.
"""
import os, shutil, struct, subprocess, tempfile, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "layouts")

# macOS virtual key code -> (US base, US shift)
US = {
    0: ("a", "A"), 1: ("s", "S"), 2: ("d", "D"), 3: ("f", "F"), 4: ("h", "H"),
    5: ("g", "G"), 6: ("z", "Z"), 7: ("x", "X"), 8: ("c", "C"), 9: ("v", "V"),
    10: ("§", "±"), 11: ("b", "B"), 12: ("q", "Q"), 13: ("w", "W"), 14: ("e", "E"),
    15: ("r", "R"), 16: ("y", "Y"), 17: ("t", "T"), 18: ("1", "!"), 19: ("2", "@"),
    20: ("3", "#"), 21: ("4", "$"), 22: ("6", "^"), 23: ("5", "%"), 24: ("=", "+"),
    25: ("9", "("), 26: ("7", "&"), 27: ("-", "_"), 28: ("8", "*"), 29: ("0", ")"),
    30: ("]", "}"), 31: ("o", "O"), 32: ("u", "U"), 33: ("[", "{"), 34: ("i", "I"),
    35: ("p", "P"), 37: ("l", "L"), 38: ("j", "J"), 39: ("'", '"'), 40: ("k", "K"),
    41: (";", ":"), 42: ("\\", "|"), 43: (",", "<"), 44: ("/", "?"), 45: ("n", "N"),
    46: ("m", "M"), 47: (".", ">"), 50: ("`", "~"),
}

# Keys whose output is the same in every layer.
FIXED = {
    36: "\r", 48: "\t", 49: " ", 51: "\b", 52: "\x03", 53: "\x1b", 76: "\x03",
    65: ".", 67: "*", 69: "+", 71: "\x1b", 75: "/", 78: "-", 81: "=",
    82: "0", 83: "1", 84: "2", 85: "3", 86: "4", 87: "5", 88: "6", 89: "7",
    91: "8", 92: "9", 114: "\x05", 115: "\x01", 116: "\x0b", 117: "\x7f",
    119: "\x04", 121: "\x0c", 123: "\x1c", 124: "\x1d", 125: "\x1f", 126: "\x1e",
}
for fkey in (96, 97, 98, 99, 100, 101, 103, 105, 106, 107, 109, 111, 113, 118, 120, 122):
    FIXED[fkey] = "\x10"

def table(pairs):
    """'us-key base shift' lines -> {keycode: (base, shift)}."""
    by_char = {v[0]: k for k, v in US.items()}
    out = {}
    for line in pairs.strip().splitlines():
        key, base, shift = line.split()
        out[by_char[key]] = (base, shift)
    return out

# KDWin Armenian phonetic
ARMENIAN = table("""
` ՝ ՜
1 է Է
2 թ Թ
3 փ Փ
4 ձ Ձ
5 ջ Ջ
6 ւ Ւ
7 և ԵՎ
8 ր Ր
9 չ Չ
0 ճ Ճ
- - —
= ժ Ժ
q ք Ք
w ո Ո
e ե Ե
r ռ Ռ
t տ Տ
y ը Ը
u ւ Ւ
i ի Ի
o օ Օ
p պ Պ
[ խ Խ
] ծ Ծ
\\ շ Շ
a ա Ա
s ս Ս
d դ Դ
f ֆ Ֆ
g գ Գ
h հ Հ
j յ Յ
k կ Կ
l լ Լ
; ; .
' ՛ "
z զ Զ
x ղ Ղ
c ց Ց
v վ Վ
b բ Բ
n ն Ն
m մ Մ
, , «
. ։ »
/ / ՞
""")

# KDWin Russian phonetic
RUSSIAN = table("""
` ч Ч
1 1 !
2 2 @
3 3 #
4 4 $
5 5 %
6 6 ^
7 7 &
8 8 *
9 9 (
0 0 )
- - _
= ю Ю
q я Я
w в В
e е Е
r р Р
t т Т
y ы Ы
u у У
i и И
o о О
p п П
[ ш Ш
] щ Щ
\\ э Э
a а А
s с С
d д Д
f ф Ф
g г Г
h х Х
j й Й
k к К
l л Л
; ; :
' ' "
z з З
x ь Ь
c ц Ц
v ж Ж
b б Б
n н Н
m м М
, , ъ
. . Ъ
/ / ?
""")

def esc(s):
    """Quoted XML attribute; control and markup characters as numeric refs, like Ukelele."""
    return '"' + "".join(f"&#x{ord(c):04X};" if ord(c) < 0x20 or ord(c) == 0x7F or c in "\"'&<>" else c
                         for c in s) + '"'

def keymap(index, pick):
    rows = []
    for code in range(128):
        if code in FIXED:
            out = FIXED[code]
        elif code in US:
            out = pick(code)
        else:
            continue
        rows.append(f'\t\t\t<key code="{code}" output={esc(out)}/>')
    return f'\t\t<keyMap index="{index}">\n' + "\n".join(rows) + "\n\t\t</keyMap>"

def ctrl(code):
    c = US[code][0]
    if c.isalpha():
        return chr(ord(c) - 96)
    return {"[": "\x1b", "\\": "\x1c", "]": "\x1d", "-": "\x1f"}.get(c, c)

def keylayout(name, layout_id, native):
    base = lambda c: native.get(c, US[c])[0]
    shift = lambda c: native.get(c, US[c])[1]
    caps = lambda c: base(c).upper() if base(c).upper() != base(c) and len(base(c).upper()) == 1 else base(c)
    maps = [
        keymap(0, base),
        keymap(1, shift),
        keymap(2, caps),
        keymap(3, lambda c: US[c][0]),
        keymap(4, lambda c: US[c][1]),
        keymap(5, ctrl),
    ]
    return f"""<?xml version="1.1" encoding="UTF-8"?>
<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">
<keyboard group="126" id="{layout_id}" name="{name}" maxout="2">
\t<layouts>
\t\t<layout first="0" last="17" mapSet="ANSI" modifiers="Modifiers"/>
\t\t<layout first="18" last="18" mapSet="ANSI" modifiers="Modifiers"/>
\t\t<layout first="21" last="23" mapSet="ANSI" modifiers="Modifiers"/>
\t\t<layout first="30" last="30" mapSet="ANSI" modifiers="Modifiers"/>
\t\t<layout first="194" last="194" mapSet="ANSI" modifiers="Modifiers"/>
\t\t<layout first="197" last="197" mapSet="ANSI" modifiers="Modifiers"/>
\t\t<layout first="200" last="201" mapSet="ANSI" modifiers="Modifiers"/>
\t\t<layout first="206" last="207" mapSet="ANSI" modifiers="Modifiers"/>
\t</layouts>
\t<modifierMap id="Modifiers" defaultIndex="0">
\t\t<keyMapSelect mapIndex="0"><modifier keys=""/></keyMapSelect>
\t\t<keyMapSelect mapIndex="1"><modifier keys="anyShift caps?"/></keyMapSelect>
\t\t<keyMapSelect mapIndex="2"><modifier keys="caps"/></keyMapSelect>
\t\t<keyMapSelect mapIndex="3"><modifier keys="anyOption caps?"/><modifier keys="caps? command anyOption? anyShift?"/></keyMapSelect>
\t\t<keyMapSelect mapIndex="4"><modifier keys="anyShift anyOption caps?"/></keyMapSelect>
\t\t<keyMapSelect mapIndex="5"><modifier keys="anyShift? caps? anyOption? command? anyControl"/></keyMapSelect>
\t</modifierMap>
\t<keyMapSet id="ANSI">
{chr(10).join(maps)}
\t</keyMapSet>
</keyboard>
"""

def stripes(*colours):
    """Flag of equal horizontal stripes, top to bottom."""
    return lambda fx, fy: colours[min(int(fy * len(colours)), len(colours) - 1)]

def us_flag(fx, fy):
    red, white, blue = (178, 34, 52), (255, 255, 255), (60, 59, 110)
    if fx < 0.4 and fy < 7 / 13:
        # 50 stars: 9 rows alternating 6 and 5, on an 11 x 9 grid.
        cx, cy = fx / 0.4 * 12, fy / (7 / 13) * 10
        col, row = round(cx), round(cy)
        on_grid = 1 <= row <= 9 and 1 <= col <= 11 and (col + row) % 2 == 0
        return white if on_grid and (cx - col) ** 2 + (cy - row) ** 2 < 0.2 else blue
    return red if int(fy * 13) % 2 == 0 else white

def png(size, flag):
    """Square PNG: a 3:2 flag with a thin border, centred on transparency.
    Each pixel is the average of 4x4 samples so small icons stay smooth."""
    height = size * 2 // 3
    top = (size - height) // 2
    rows = b""
    for y in range(size):
        row = b"\x00"
        fy = y - top
        for x in range(size):
            if not 0 <= fy < height:
                row += b"\x00\x00\x00\x00"
            elif x == 0 or fy == 0 or x == size - 1 or fy == height - 1:
                row += bytes((90, 90, 90, 255))
            else:
                samples = [flag((x + (i + 0.5) / 4) / size, (fy + (j + 0.5) / 4) / height)
                           for i in range(4) for j in range(4)]
                row += bytes(sum(c[k] for c in samples) // 16 for k in range(3)) + b"\xff"
        rows += row
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))

def flag_icns(path, flag):
    with tempfile.TemporaryDirectory() as tmp:
        iconset = os.path.join(tmp, "flag.iconset")
        os.mkdir(iconset)
        for size in (16, 32, 128, 256, 512):
            for scale in (1, 2):
                name = f"icon_{size}x{size}{'@2x' if scale == 2 else ''}.png"
                open(os.path.join(iconset, name), "wb").write(png(size * scale, flag))
        subprocess.run(["iconutil", "-c", "icns", iconset, "-o", path], check=True)

LAYOUTS = [
    # name, id, map, language, flag
    ("Armenian KDWin", -23401, ARMENIAN, "hy", stripes((217, 0, 18), (0, 51, 160), (242, 168, 0))),
    ("Russian KDWin", -23402, RUSSIAN, "ru", stripes((255, 255, 255), (0, 57, 166), (213, 43, 30))),
    ("English US", -23403, {}, "en", us_flag),
]

def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    # Loose .keylayout files (not a .bundle): macOS picks these up reliably, and
    # the .icns with the same name becomes the menu-bar flag.
    for name, layout_id, native, lang, flag in LAYOUTS:
        open(os.path.join(OUT, f"{name}.keylayout"), "w", encoding="utf-8").write(keylayout(name, layout_id, native))
        flag_icns(os.path.join(OUT, f"{name}.icns"), flag)
    print("Built", OUT)

if __name__ == "__main__":
    main()
