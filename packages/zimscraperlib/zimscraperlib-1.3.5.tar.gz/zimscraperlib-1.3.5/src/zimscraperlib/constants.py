#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import pathlib

ROOT_DIR = pathlib.Path(__file__).parent
NAME = pathlib.Path(__file__).parent.name
with open(ROOT_DIR.joinpath("VERSION"), "r") as fh:
    VERSION = fh.read().strip()
SCRAPER = f"{NAME} {VERSION}"

UTF8 = "UTF-8"

ALPHA_NOT_SUPPORTED = ["JPEG", "BMP", "EPS", "PCX"]
