import os

from conans.client.conan_api import Conan

script_path = os.path.realpath(__file__)
script_path_dir = os.path.dirname(script_path)
conanfile_path = os.path.join(script_path_dir, "conanfile.py")

conan = Conan()

conan.create(conanfile_path, settings=["compiler.cppstd=17"], version="1.0.0")
