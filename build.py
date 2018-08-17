#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_installer

if __name__ == "__main__":

    builder = build_template_installer.get_builder()

    builder.run()
