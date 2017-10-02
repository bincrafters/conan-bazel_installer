from conans import ConanFile


class TestPackage(ConanFile):
    def test(self):
        self.run("bazel version")
