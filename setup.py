"""
Based on:
+ https://martinopilia.com/posts/2018/09/15/building-python-extension.html
+ https://stackoverflow.com/a/51575996/4355781
"""
import os
import shutil
import subprocess

from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    long_description = f.read()


def get_cmake():
    for exe in ["cmake3", "cmake28", "cmake"]:
        try:
            subprocess.check_output([exe, "--version"])
            return exe
        except OSError:
            pass
    raise RuntimeError("No cmake version found.")


class CMakeExtension(Extension):
    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])


class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)

        _ = self.extensions
        self.extensions = []
        super().run()
        self.extensions = _

    def build_cmake(self, ext):
        folder = os.path.join(os.path.dirname(self.get_ext_fullpath(ext.name)))
        os.makedirs(self.build_temp, exist_ok=True)
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(here, ext.name, "CMakeLists.txt"), mode="a") as f:
            print("include_directories(/usr/include/ffmpeg)", file=f)
        subprocess.check_call([get_cmake(), os.path.join(here, ext.name), "-DCMAKE_BUILD_TYPE=Release", "-DWITH_VIDEO_HASH=1", "-DWITH_AUDIO_HASH=1"], cwd=self.build_temp)
        subprocess.check_call(["make", "-j"], cwd=self.build_temp)
        subprocess.check_call(["sed", "-i", "s/#define __STDC_CONSTANT_MACROS//g", os.path.join("src", "%s.h" % ext.name)], cwd=os.path.join(here, ext.name))
        self.distribution.bin_dir = folder
        shutil.copy(os.path.join(self.build_temp, "Release", "lib%s.so" % ext.name), folder)
        shutil.copy(os.path.join(here, ext.name, "src", "%s.h" % ext.name), folder)


setup(
    name="pHashPy",
    version="0.1.1",
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
