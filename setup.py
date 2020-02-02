import os
import subprocess

from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    long_description = f.read()


class CMakeExtension(Extension):
    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])


class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("Cannot find CMake executable")

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(["cmake", os.path.join(here, ext.name), "-DCMAKE_BUILD_TYPE=Release",
                               "-DWITH_VIDEO_HASH=1", "-DWITH_AUDIO_HASH=1"], cwd=self.build_temp)

        subprocess.check_call(["make", "-j"], cwd=self.build_temp)


setup(
    name="pHashPy",
    version="0.0.2",
    author="Dries007",
    author_email="admin@dries007.net",
    description="Python bindings for the pHash (perceptual hashing) library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dries007/pHashPy",
    license="gpl-3",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: POSIX :: Linux",
    ],
    packages=find_packages(),
    install_requires=["cppyy>=1.6.0"],
    zip_safe=False,
    ext_modules=[
        CMakeExtension("pHash"),
    ],
    cmdclass={
        "build_ext": CMakeBuild,
    },
    entry_points={
        "console_scripts": [
            "pHashPy = pHashPy.__main__:main"
        ]
    },
    package_data={
        "": ["*.so"]
    }
)
