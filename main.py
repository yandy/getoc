#!/usr/bin/env python
import os.path
import sys
import os
import json
import subprocess
import shlex


def extract_courses(course_idx):
    with open(course_idx) as f:
        name = json.loads(f.readline())['name']
        lessons = [json.loads(l) for l in f.readlines()]
        return (name, lessons)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Get open course resoures')
    parser.add_argument(
        'urls', metavar='URL', nargs='+', help="urls of open courses' urls")
    parser.add_argument(
        '-o', '--output', default='tmp', help="output location")
    args = parser.parse_args(sys.argv[1:])
    kwargs = vars(args)
    urls = kwargs['urls']
    course_idx = os.path.join(kwargs['output'], 'idx.jl')
    for url in urls:
        cmd = "scrapy crawl oc163 -o %s -a url=%s" % (course_idx, url)
        subprocess.check_call(shlex.split(cmd))
        name, lessons = extract_courses(course_idx)
        course_dir = os.path.join(kwargs['output'], name)
        for l in lessons:
            cmd = 'you-get -o %s %s' % (course_dir, l['url'])
            subprocess.check_call(shlex.split(cmd))
