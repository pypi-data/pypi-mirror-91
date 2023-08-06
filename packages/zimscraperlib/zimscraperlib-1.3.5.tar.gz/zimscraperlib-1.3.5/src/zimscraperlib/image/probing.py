#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import io
import re
import pathlib
import colorsys
from typing import Tuple, Optional, Union

import PIL.Image
import colorthief


def get_colors(
    src: pathlib.Path, use_palette: Optional[bool] = True
) -> Tuple[str, str]:
    """ (main, secondary) HTML color codes from an image path """

    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """ hexadecimal HTML-friendly color code for RGB tuple """
        return "#{}{}{}".format(*[str(hex(x)[2:]).zfill(2) for x in (r, g, b)]).upper()

    def solarize(r: int, g: int, b: int) -> Tuple[int, int, int]:
        # calculate solarized color for main
        h, l, s = colorsys.rgb_to_hls(float(r) / 256, float(g) / 256, float(b) / 256)
        r2, g2, b2 = [int(x * 256) for x in colorsys.hls_to_rgb(h, 0.95, s)]
        return r2, g2, b2

    ct = colorthief.ColorThief(src)

    if use_palette:
        # extract two main colors from palette, solarizing second as background
        palette = ct.get_palette(color_count=2, quality=1)

        # using the first two colors of the palette?
        mr, mg, mb = palette[0]
        sr, sg, sb = solarize(*palette[1])
    else:
        # extract main color from image and solarize it as background
        mr, mg, mb = ct.get_color(quality=1)
        sr, sg, sb = solarize(mr, mg, mb)

    return rgb_to_hex(mr, mg, mb), rgb_to_hex(sr, sg, sb)


def is_hex_color(text: str) -> bool:
    """ whether supplied text is a valid hex-formated color code """
    return re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", text)


def format_for(src: Union[pathlib.Path, io.BytesIO], from_suffix: bool = True) -> str:
    """ Pillow format of a given filename, either Pillow-detected or from suffix """
    if not from_suffix:
        with PIL.Image.open(src) as img:
            return img.format

    from PIL.Image import EXTENSION as ext_fmt_map, init as init_pil

    init_pil()
    return ext_fmt_map[src.suffix]  # might raise KeyError on unknown extension
