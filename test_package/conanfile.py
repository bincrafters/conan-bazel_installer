from conans import ConanFile


class TestPackageConan(ConanFile):
    def test(self):
        self.run("bazel version")
