#!/usr/bin/env python
import os

import livereload


DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATTERN = os.path.join(DOCS_DIR, "*.rst")
BUILD_DIR = os.path.join(DOCS_DIR, "_build", "html")


def main():
    server = livereload.Server()
    server.watch(SOURCE_PATTERN, livereload.shell("make html", cwd=DOCS_DIR))
    server.serve(root=BUILD_DIR)


if __name__ == "__main__":
    main()
