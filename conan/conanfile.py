from conans import ConanFile, CMake, tools
import os
import shutil


class CppCommon(ConanFile):
    name = "cppcommon"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/chronoxor/CppCommon"
    description = "C++ Common Library contains reusable components and patterns" \
        " for error and exceptions handling, filesystem manipulations, math," \
        " string format and encoding, shared memory, threading, time management" \
        " and others."
    topics = ("conan", "utils", "library")
    settings = "os", "compiler", "build_type", "arch"
    options = {"fPIC": [True, False],
               "shared": [True, False]}
    default_options = {"fPIC": True,
                       "shared": False}
    requires = ["fmt/7.0.3"]
    generators = "cmake", "visual_studio"
    exports_sources = ["../**"]
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["CPPCOMMON_MODULE"] = "ON"
            self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def source(self):
        os.makedirs(self._source_subfolder, exist_ok=True)
        shutil.move("include", dst=self._source_subfolder)
        shutil.move("source", dst=self._source_subfolder)
        shutil.move("plugins", dst=self._source_subfolder)
        shutil.move("CMakeLists.txt", dst=self._source_subfolder)
        shutil.move("conan/patches", dst=".")
        shutil.move("conan/CMakeLists.txt", dst=".")
        self.output.warn(os.getcwd())

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, "17")

        if self.options.shared:
            del self.options.fPIC

    def build(self):
        patches = self.conan_data["patches"][self.version]
        for patch in patches or []:
            tools.patch(**patch)

        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        include = os.path.join(self._source_subfolder, "include")
        self.copy("*.h", src=include, dst="include", keep_path=True)
        self.copy("*.inl", src=include, dst="include", keep_path=True)
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
