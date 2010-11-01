from setuptools import setup

__author__ = "Armand Lynch <lyncha@users.sourceforge.net>"
__contributors__ = "Pau Aliagas <pau@newtral.org>"
__copyright__ = "Copyright 2006-2010, Armand Lynch"
__license__ = "LGPL"
__url__ = "http://celljam.net/"
__version__ = "7.1.1"
doc = "HOLDER"


# By Armand Sat Apr 18 18:35:45 EDT 2009
# Pau Aliagas was a major contributor to this effort
# Thanks

setup (name="pywurfl",
       version=__version__,
       author=["Armand Lynch"],
       author_email=["lyncha@users.sourceforge.net"],
       contact="Armand Lynch",
       contact_email="lyncha@users.sourceforge.net",
       license=__license__,
       url=__url__,
       packages=['pywurfl', 'pywurfl.algorithms', 'pywurfl.algorithms.wurfl'],
       install_requires = [
           'python-Levenshtein',
           'elementtree',
       ],
       scripts=['bin/wurfl2python.py'],
       description=doc,
       long_description=doc,
       platforms="All",
       classifiers=['Development Status :: 5 - Production/Stable',
                    'Environment :: Console',
                    'Environment :: Web Environment',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Telecommunications Industry',
                    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                    'Natural Language :: English',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Topic :: Database :: Front-Ends',
                    'Topic :: Internet :: WAP',
                    'Topic :: Software Development :: Libraries :: Python Modules',
                    'Topic :: Utilities'
                    ])
