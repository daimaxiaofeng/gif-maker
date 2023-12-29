#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os
import sys
import time
import threading
from subprocess import Popen, PIPE
from jinja2 import Template

CACHE_PATH = "cache"
CACHE_TIME = 3 * 60

STATIC_PATH = "static"

TPL_MP4 = "template.mp4"
TPL = "template.tpl"


def delete_file(file_path):
    time.sleep(CACHE_TIME)
    os.remove(file_path)

def clear_cache(*paths):
    for p in paths:
        delete_thread = threading.Thread(target=delete_file, args=(p,))
        delete_thread.start()

def calculate_hash(src):
    m2 = hashlib.md5()
    m2.update(str(src).encode("utf8"))
    return m2.hexdigest()

def normalize_path(*args):
    path = os.path.join(*args)
    if sys.platform == 'win32':
        path = path.replace('\\', '/')
    return path

def make(template_name, sentences):
    filename = template_name + "-" + calculate_hash(sentences) + ".gif"
    video_path = normalize_path(STATIC_PATH, template_name, TPL_MP4)
    ass_path = render_ass(template_name, sentences, filename)
    gif_path = normalize_path(CACHE_PATH, filename)

    if not os.path.exists(gif_path):
        make_gif_with_ffmpeg(video_path, ass_path, gif_path)

    clear_cache(ass_path, gif_path)

    return gif_path


def ass_text(template_name):
    tpl_path = normalize_path(STATIC_PATH, "%s", TPL)
    with open(tpl_path % template_name) as fp:
        content = fp.read()
    return content


def render_ass(template_name, sentences, filename):
    output_file_path = normalize_path(CACHE_PATH, "%s.ass") % filename
    template = ass_text(template_name)
    rendered_ass_text = Template(template).render(sentences=sentences)
    with open(output_file_path, "w", encoding="utf8") as fp:
        fp.write(rendered_ass_text)
    return output_file_path


def make_gif_with_ffmpeg(video_path, ass_path, gif_path):
    cmd = "ffmpeg -i {video_path} -r 8 -vf ass={ass_path},scale=300:-1 -y {gif_path}" \
        .format(video_path=video_path, ass_path=ass_path, gif_path=gif_path)
    print(cmd)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    p.wait()
    return p.returncode