from __future__ import absolute_import
from __future__ import unicode_literals
from setuptools import setup

__version__ = 'undefined'
exec(open('forgehg/version.py').read())

TOOL_DESCRIPTION = """ForgeHg enables an Allura installation to use the Mercurial
source code management system. Mercurial (Hg) is an open source distributed
version control system (DVCS) similar to git and written in Python.
"""

setup(name='ForgeHg',
      version=__version__,
      description="Mercurial (Hg) SCM support for Apache Allura",
      long_description=TOOL_DESCRIPTION,
      classifiers=[
        ## From http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: TurboGears',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
      ],
      keywords='Allura forge Mercurial Hg scm',
      author_email='dev@allura.apache.org',
      url='http://sourceforge.net/p/forgehg',
      license='GPLv2',
      packages=[
        'forgehg',
        'forgehg.model',
        'forgehg.templates'
      ],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # 5.2.2 was latest version tested
          # Restricting max version since mercurial is tightly integrated and changes often can break our code
          'mercurial < 5.3, >= 4.6',
          'six',
      ],
      entry_points="""
      [allura]
      Hg=forgehg.hg_main:ForgeHgApp

      [allura.timers]
      hg = forgehg.hg_main:hg_timers
      forgehg = forgehg.hg_main:forgehg_timers

      [nose.plugins]
      monkeypatch_capture = forgehg:MonkeyPatchCapture
      """,
      )
