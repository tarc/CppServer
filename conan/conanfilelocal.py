from conans import CMake, tools
from base.conanfilebase import CppServerBase
import shutil
import os


class CppServer(CppServerBase):
    exports = ["base/conanfilebase.py"]
    exports_sources = ["local/CMakeLists.txt", "patches/*", "../tools*"]

    @property
    def _source_subfolder(self):
        return ".."

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["CPPSERVER_MODULE"] = "OFF"
            self._cmake.definitions["CPPSERVER_BENCHMARKS"] = "OFF"
            self._cmake.definitions["CPPSERVER_EXAMPLES"] = "OFF"
            self._cmake.definitions["CPPSERVER_TESTS"] = "ON" if self.options.tests else "OFF"
            self._cmake.configure(build_folder=self._build_subfolder,
                source_folder=self.build_folder)
        return self._cmake

    def _patch(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, {}).get("local", []):
            tools.patch(**patch)

        if self.options.tests:
            os.makedirs(self._build_subfolder, exist_ok=True)
            shutil.move("tools", dst=self._build_subfolder)

    def source(self):
        shutil.move("local/CMakeLists.txt", dst=".")
