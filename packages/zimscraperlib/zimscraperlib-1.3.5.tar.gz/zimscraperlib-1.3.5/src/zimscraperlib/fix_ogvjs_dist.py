#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


""" quick script to inject a function in ogv.js' -wasm.js scripts

    ogv.js dynamicaly loads .wasm scripts.
    it does it in two different manners, not always respecting its .base attribute
    .wasm scripts are binaries so they reside in /I/ inside ZIM files
    while javascript ones are in /-/.
    To easily circumvent this while keeping in working in HTML folder (no zim),
    we inject a `target=zim_fix_wasm_target(target)` in the -wasm.js files.
    We do it on the dist files as those files are not from the JS source of ogv.js
    but built with emscripten. Also, ogv.js toolchain is long to setup.

"""

import sys
import inspect
import logging
import pathlib

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

generic_function_block = """
if (typeof zim_fix_wasm_target === 'undefined') {
    IS_IN_ZIM = self.location.href.indexOf("/-/") != -1 || self.location.href.indexOf("/I/") != -1 || self.location.href.indexOf("/A/") != -1;
    ZIM_IMG_NS = (IS_IN_ZIM) ? '../../{extra_parent_jumps}../I/' : '';
    hasImageNamespacePrefix = function(target) { return target.indexOf("/I/") != -1; }
    hasMetaNamespacePrefix = function(target) { return target.indexOf("/-/") != -1; }
    changeNamespacePrefix = function(target, new_ns) { return target.replace("/-/", new_ns); }
    zim_fix_wasm_target = function(target) {
        console.debug("in-file zim_fix_wasm_target:", target);
        if (!IS_IN_ZIM) {
            console.debug("..not in zim");
            return target;
        }
        if (hasImageNamespacePrefix(target)) {
            // we already have a good path, leave it
        }
        else if (hasMetaNamespacePrefix(target)) {
            // we have a prefix, just replace it
            target = changeNamespacePrefix(target, "I");
        }
        else {
            // we lack the prefix, add it
            target = ZIM_IMG_NS + "{vendors_path}/ogvjs/" + target;
        }
        console.debug("..target:", target);
        return target;
    }
  }

"""


def fix_source_dir(source_vendors_path, dest_vendors_path="vendors"):
    logger.info("about to add fix to ogv.js files to dynamicaly load wasm files in ZIM")
    parent_dir_count = len(pathlib.Path(dest_vendors_path).parts)
    function_block = generic_function_block.replace(
        "{extra_parent_jumps}", "../" * (parent_dir_count - 1)
    )
    root = pathlib.Path(source_vendors_path)
    ogvjs_path = root.joinpath("ogvjs")

    for fname in [
        "ogv-decoder-audio-opus-wasm.js",
        "ogv-decoder-audio-vorbis-wasm.js",
        # "ogv-decoder-video-av1-mt-wasm.js",
        "ogv-decoder-video-av1-wasm.js",
        "ogv-decoder-video-theora-wasm.js",
        # "ogv-decoder-video-vp8-mt-wasm.js",
        "ogv-decoder-video-vp8-wasm.js",
        # "ogv-decoder-video-vp9-mt-wasm.js",
        "ogv-decoder-video-vp9-wasm.js",
        "ogv-demuxer-ogg-wasm.js",
        "ogv-demuxer-webm-wasm.js",
    ]:
        fpath = ogvjs_path.joinpath(fname)

        with open(fpath, "r") as fp:
            content = fp.read()
        if "zim_fix_wasm_target" in content:
            logger.info(f"File `{fpath}` is already fixed!")
            continue
        else:
            logger.info(f"File `{fpath}` needs to be fixed.")

        # first pass, add function block
        vara_pos = content.index("var a;a")
        before = content[0:vara_pos]
        after = content[vara_pos:]
        content = (
            before + function_block.replace("{vendors_path}", dest_vendors_path) + after
        )

        # second pass, add call to function
        locatefile_pos = content.index(".locateFile")
        bracket_pos = locatefile_pos + content[locatefile_pos:].index("}")
        before = content[0:bracket_pos]
        after = content[bracket_pos:]
        equal_pos = before[::-1].index("=")
        variable = before[::-1][equal_pos + 1 : equal_pos + 2]
        our_fix = ";{var}=zim_fix_wasm_target({var});".format(var=variable)

        with open(fpath, "w") as fp:
            fp.write(before + our_fix + after)

    logger.info("fixing videosjs-ogvjs.js")
    plugin_path = root.joinpath("videojs-ogvjs.js")
    with open(plugin_path, "r") as fp:
        content = fp.read()

    content = content.replace(
        "_OGVLoader2['default'].base = options.base;",
        "_OGVLoader2['default'].base = ZIM_META_NS + options.base;",
    )
    content = content.replace(
        "return type.indexOf('/ogg') !== -1 ? 'maybe' : '';",
        "return (type.indexOf('/webm') !== -1 || type.indexOf('/ogg') !== -1) ? 'maybe' : '';",
    )

    with open(plugin_path, "w") as fp:
        fp.write(content)

    logger.info("hack video.min.js (TEMP FIX to work aroung Qt bug in reader)")
    videojs_path = root.joinpath("videojs", "video.min.js")
    with open(videojs_path, "r") as fp:
        content = fp.read()

    content = content.replace(";return 0!==e?(t=", ";return (0!==e || IS_IN_ZIM)?(t=")

    with open(videojs_path, "w") as fp:
        fp.write(content)

    logger.info("all done.")


def run():
    args = sys.argv[1:]
    if not args:
        signature = inspect.signature(fix_source_dir)
        dvp = signature.parameters["dest_vendors_path"]
        print(f"Usage: {sys.argv[0]} <source_vendors_path> [<dest_vendors_path>]")
        print(
            f"\t<source_vendors_path>\tpath to your folder containing ogvjs/videojs/videojs-ogvjs."
        )
        print(
            f"\t<dest_vendors_path>\trelative path to that folder in dest HTML. Defaults to `{dvp.default}`"
        )
        sys.exit(1)
    return sys.exit(fix_source_dir(*args))


if __name__ == "__main__":
    run()
