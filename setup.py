from distutils.core import setup

setup(
    name="py-livecoder",
    version="1.0.0",
    author="Khair-ed-Din Husseini",
    author_email="kmhusseini@gmail.com",
    packages=["livecoder"],
    include_package_data=True,
    license="GPLv3",
    install_requires=['mido', 'python-rtmidi', 'urwid', 'lark-parser']
)
