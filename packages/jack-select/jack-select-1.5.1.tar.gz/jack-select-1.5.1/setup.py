#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A systray app to set the JACK configuration from QjackCtl presets via DBus.

This application displays an icon in the system tray (also known as
notification area) of your desktop, which shows the status of the JACK_ audio
server and when you click on it, a menu pops up, which lets you quickly select
from the JACK configuration presets you created with QjackCtl_. When you
select a preset, its JACK engine and driver configuration settings are loaded
via DBus into JACK and then the server is restarted. This allows you to switch
between different audio setups with just two mouse clicks.

**jack-select** works with the DBus-version of JACK only. It is written in
Python 3 using the ``PyGObject`` bindings for GTK 3. Python 2 is not supported.

It is available from the source code repository on GitHub:

https://github.com/SpotlightKid/jack-select

Releases can be downloaded from the Python Package Index:

https://pypi.org/project/jack-select

**jack-select** is also available as an Arch Linux package from the Arch User
Repository:

https://aur.archlinux.org/packages/jack-select/


.. _jack: http://jackaudio.org/
.. _qjackctl: http://qjackctl.sourceforge.net/

"""

import setuptools


exec(open('jackselect/version.py').read())

setuptools.setup(
    name="jack-select",
    version=__version__,  # noqa
    url="https://github.com/SpotlightKid/jack-select",
    author="Christopher Arndt",
    author_email="chris@chrisarndt.de",
    description=__doc__.splitlines()[0],
    long_description="\n".join(__doc__.splitlines()[2:]),
    keywords="JACK,systray,GTK,DBus,audio",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'PyGObject',
        'dbus-python',
        'pyudev',
        'pyxdg'
    ],
    entry_points = {
        'console_scripts': [
            'jack-select = jackselect.jackselect:main',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Environment :: X11 Applications :: GTK',
        'Topic :: Multimedia :: Sound/Audio'
    ],
)
