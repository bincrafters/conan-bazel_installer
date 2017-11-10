#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile


class TestPackageConan(ConanFile):
    def test(self):
        self.run("bazel version")
