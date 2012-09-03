#!/usr/bin/env python
# -----------------------------------------------------------------------------
#    Daarmaan - Single Sign On Service for Yellowen
#    Copyright (C) 2012 Yellowen
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

from distutils.core import setup

setup(name='Daarmaan',
      version='0.2.1',
      description='Single Sign On Service for Yellowen',
      author='Sameer Rahmani',
      author_email='lxsameer@gnu.org',
      url='http://daarmaan.yellowen.com/',
      download_url="http://daarmaan.yellowen.com/downloads/",
      keywords=('SSO', 'authentication', 'authorization'),
      license='GPL v3',
      scripts=[],
      packages=['daarmaan', 'daarmaan.client', 'daarmaan.server'],
      requires=['vakhshour', ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
          ]
)
