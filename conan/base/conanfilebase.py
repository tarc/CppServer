from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os
import shutil


class CppServerBase(ConanFile):
    name = "cppserver"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/chronoxor/CppServer"
    description = "Ultra fast and low latency asynchronous socket server and" \
        " client C++ library with support TCP, SSL, UDP, HTTP, HTTPS, WebSocket" \
        " protocols and 10K connections problem solution."
    topics = ("network", "socket", "async", "low-latency")
    settings = "os", "compiler", "build_type", "arch"
    options = {"fPIC": [True, False],
               "shared": [True, False],
               "tests": [True, False]}
    default_options = {"fPIC": True,
                       "shared": False,
                       "tests": False}
    requires = ["asio/1.17.0", "openssl/1.1.1g", "cppcommon/1.0.0.0"]
    generators = "cmake"
    exports_sources = ["../**"]
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    @property
    def _compilers_minimum_version(self):
        return {
            "apple-clang": 10,
            "clang": 6,
            "gcc": 7,
            "Visual Studio": 16,
        }

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["CPPSERVER_MODULE"] = "OFF"
            self._cmake.definitions["CPPSERVER_BENCHMARKS"] = "OFF"
            self._cmake.definitions["CPPSERVER_EXAMPLES"] = "OFF"
            self._cmake.definitions["CPPSERVER_TESTS"] = "ON" if self.options.tests else "OFF"
            self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def _patch(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, {}).get("package", []):
            tools.patch(**patch)

        if self.options.tests:
            os.makedirs(self._build_subfolder, exist_ok=True)
            shutil.move("tools", dst=self._build_subfolder)

    def source(self):
        os.makedirs(self._source_subfolder, exist_ok=True)

        if self.options.tests:
            shutil.copytree("tests", dst=os.path.join(self._source_subfolder, "tests"))
        else:
            shutil.rmdir("tests")
            shutil.rmdir("tools")

        shutil.move("include", dst=self._source_subfolder)
        shutil.move("source", dst=self._source_subfolder)
        shutil.move("CMakeLists.txt", dst=self._source_subfolder)
        shutil.move("conan/patches", dst=".")
        shutil.move("conan/CMakeLists.txt", dst=".")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.settings.compiler == "Visual Studio" and self.settings.arch == "x86":
            raise ConanInvalidConfiguration("Visual Studio x86 builds are not supported.")

        if self.options.shared:
            del self.options.fPIC

        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, "17")

        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if minimum_version:
            if tools.Version(self.settings.compiler.version) < minimum_version:
                raise ConanInvalidConfiguration(
                    "cppserver requires C++17, which your compiler does not support.")
        else:
            self.output.warn(
                "cppserver requires C++17. Your compiler is unknown. Assuming it supports C++17.")

    def requirements(self):
        if self.options.tests:
           self.requires("catch2/2.13.2")

    def build(self):
        self._patch()

        cmake = self._configure_cmake()
        cmake.build()

        if self.options.tests:
            cmake.test(output_on_failure=True)

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread", "rt", "dl"]

        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["ws2_32", "crypt32", "rpcrt4"]
            self.cpp_info.defines.extend(
                ["_WIN32_WINNT=_WIN32_WINNT_WIN7",
                "_WINSOCK_DEPRECATED_NO_WARNINGS",
                "_SILENCE_CXX17_ALLOCATOR_VOID_DEPRECATION_WARNING"])
