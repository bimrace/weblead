#!/usr/bin/env python3
r"""
BIMRACE — recolour the raster icons.

    python recolour-icons.py            # apply
    python recolour-icons.py --check    # report only, write nothing

The tile colour lives in favicon.svg, but icon-192.png, icon-512.png,
apple-touch-icon.png and favicon.ico are rasters and cannot inherit it. This
re-maps the tile colour in place so all five stay the same colour.

Why recolour rather than re-render: headless Edge (which make-og.sh uses) is
non-functional on this machine — it exits 0 and writes nothing, so `--screenshot`
silently produces no file. There is no Pillow and no ImageMagick either;
`convert` here is C:\Windows\system32\convert.exe, the FAT-to-NTFS filesystem
converter, which must never be invoked on an image path.

Recolouring is also more faithful than re-rendering would be: the geometry,
anti-aliasing and corner radii already in these files are preserved exactly, and
only the hue moves.

The maths. Every pixel in these icons is a blend of the tile colour and the
white mark: px = OLD*(1-t) + WHITE*t. The red channel separates the two by 244
of 255, so t is recovered from red alone with negligible quantisation error,
then re-applied against the new tile colour. Alpha is carried through untouched,
which is what keeps the rounded corners clean.
"""
import pathlib, struct, sys, zlib

ROOT = pathlib.Path(__file__).resolve().parent
OLD = (11, 124, 116)      # #0B7C74 — the signal teal
NEW = (11, 20, 32)        # #0B1420 — the site's ink token, same black as the wordmark
WHITE = (255, 255, 255)

FILES = ["icon-192.png", "icon-512.png", "apple-touch-icon.png", "favicon.ico"]


# --------------------------------------------------------------- PNG codec --
def png_decode(blob):
    """-> (width, height, colour_type, [rows of bytes]). 8-bit, non-interlaced."""
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    i, idat, meta = 8, bytearray(), {}
    while i < len(blob):
        ln = struct.unpack(">I", blob[i:i + 4])[0]
        typ = blob[i + 4:i + 8]
        data = blob[i + 8:i + 8 + ln]
        if typ == b"IHDR":
            w, h, bd, ct, comp, filt, inter = struct.unpack(">IIBBBBB", data)
            if bd != 8:
                raise ValueError(f"bit depth {bd} unsupported")
            if inter:
                raise ValueError("interlaced PNG unsupported")
            meta = dict(w=w, h=h, ct=ct)
        elif typ == b"IDAT":
            idat += data
        elif typ == b"IEND":
            break
        i += 12 + ln

    ch = {0: 1, 2: 3, 4: 2, 6: 4}[meta["ct"]]
    raw = zlib.decompress(bytes(idat))
    w, h, stride = meta["w"], meta["h"], meta["w"] * ch
    rows, prev, pos = [], bytearray(stride), 0
    for _ in range(h):
        ft = raw[pos]; pos += 1
        line = bytearray(raw[pos:pos + stride]); pos += stride
        # Undo the per-scanline filter. Paeth is the only fiddly one.
        for x in range(stride):
            a = line[x - ch] if x >= ch else 0
            b = prev[x]
            c = prev[x - ch] if x >= ch else 0
            if ft == 1:
                line[x] = (line[x] + a) & 0xFF
            elif ft == 2:
                line[x] = (line[x] + b) & 0xFF
            elif ft == 3:
                line[x] = (line[x] + ((a + b) >> 1)) & 0xFF
            elif ft == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 0xFF
        rows.append(line)
        prev = line
    return w, h, meta["ct"], rows


def png_encode(w, h, ct, rows):
    """Filter type 0 on every row. Larger than an optimal encoder would manage,
    by a few hundred bytes on a 512px icon — worth it for code you can read."""
    raw = bytearray()
    for line in rows:
        raw.append(0)
        raw += line

    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data
                + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, ct, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


# ----------------------------------------------------------------- remap ---
def remap_rows(ct, rows):
    """Return (rows, pixels_changed). Alpha and pure white are left alone."""
    ch = {2: 3, 6: 4}[ct]
    span = WHITE[0] - OLD[0]
    changed = 0
    for line in rows:
        for x in range(0, len(line), ch):
            r, g, b = line[x], line[x + 1], line[x + 2]
            if (r, g, b) == WHITE:
                continue                       # the mark itself
            t = (r - OLD[0]) / span
            t = 0.0 if t < 0 else (1.0 if t > 1 else t)
            nr = round(NEW[0] + t * (WHITE[0] - NEW[0]))
            ng = round(NEW[1] + t * (WHITE[1] - NEW[1]))
            nb = round(NEW[2] + t * (WHITE[2] - NEW[2]))
            if (nr, ng, nb) != (r, g, b):
                line[x], line[x + 1], line[x + 2] = nr, ng, nb
                changed += 1
    return rows, changed


def recolour_png(blob):
    w, h, ct, rows = png_decode(blob)
    rows, changed = remap_rows(ct, rows)
    return png_encode(w, h, ct, rows), changed


def recolour_ico(blob):
    """An .ico is a directory of images. Ours holds three PNGs (16/32/48).
    Recolour each payload and rebuild the directory with corrected offsets."""
    reserved, typ, count = struct.unpack("<HHH", blob[:6])
    if typ != 1:
        raise ValueError("not an icon file")
    entries, total = [], 0
    for i in range(count):
        e = struct.unpack("<BBBBHHII", blob[6 + i * 16:6 + i * 16 + 16])
        payload = blob[e[7]:e[7] + e[6]]
        if payload[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("BMP-encoded icon entry unsupported")
        new, changed = recolour_png(payload)
        total += changed
        entries.append((e, new))

    out = struct.pack("<HHH", 0, 1, count)
    offset = 6 + 16 * count
    dirs = b""
    for e, payload in entries:
        dirs += struct.pack("<BBBBHHII", e[0], e[1], e[2], e[3], e[4], e[5],
                            len(payload), offset)
        offset += len(payload)
    return out + dirs + b"".join(p for _, p in entries), total


# ------------------------------------------------------------------ main ---
def main():
    check = "--check" in sys.argv
    print(f"tile #{OLD[0]:02X}{OLD[1]:02X}{OLD[2]:02X} -> "
          f"#{NEW[0]:02X}{NEW[1]:02X}{NEW[2]:02X}"
          f"{'   (check only, nothing written)' if check else ''}\n")
    touched = 0
    for name in FILES:
        p = ROOT / name
        if not p.exists():
            print(f"  {name:<22} MISSING")
            continue
        blob = p.read_bytes()
        new, changed = (recolour_ico(blob) if p.suffix == ".ico"
                        else recolour_png(blob))
        if changed and not check:
            p.write_bytes(new)
        touched += changed
        print(f"  {name:<22} {changed:>7,} px remapped   "
              f"{len(blob):>6} -> {len(new):>6} bytes"
              f"{'' if changed else '   (already black)'}")
    print(f"\n{touched:,} pixels total"
          + ("" if check else ".  Now run: python build.py --install"))


if __name__ == "__main__":
    main()
