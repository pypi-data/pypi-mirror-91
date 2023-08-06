============
xunitparserx
============

Description
-----------

xunitparserx reads a JUnit/XUnit/MSTest XML file and maps it to Python objects.
It tries to use the objects available in the standard ``unittest`` module.

xunitparserx work both for python2 and python3, with addition MSTest trx support

Usage
-----

::

    import xunitparserx
    ts, tr = xunitparserx.parse(open('/path/to/unit.xml'))


``ts`` is a ``TestSuite`` class, containing ``TestCase`` classes.
``tr`` is a ``TestResult`` class.

You can change the classes used (though they probably would not work unless
they inherit from the ``xunitparserx`` ones) by using your own
``xunitparserx.Parser`` class and changing the ``*_CLASS`` variables.

Some helpful properties are added to the ``TestCase`` class::

    for tc in ts:
        print('Class %s, method %s' % (tc.classname, tc.methodname))
        if tc.good:
            print('went well...', 'but did not run.' if tc.skip else '')
        else:
            print('went wrong.')

For more, please read the source code - it is very minimal.
The classes also inherit from the `unittest`__ module so it is actually
a good reference of what you can do with ``xunitparserx``.

__ http://docs.python.org/library/unittest.html


Changes
-------
+ 1.9.10+

  - use github action to auto publish to pypi

+ 1.9.9

  - add fromstring support, ref:https://docs.python.org/3/library/xml.etree.elementtree.html#parsing-xml
  - add MSTest trx support(parse_trx, fromstring_trx), ref: https://gist.github.com/congzhangzh/92ca9692430a95e3dce98f4ae2c0004e, https://gist.github.com/congzhangzh/30ecfd89fa9f0d4139c585869d2df81f, https://github.com/x97mdr/pickles/blob/master/src/Pickles/Pickles.Test/results-example-mstest.trx
  - add pytest record_xml_property support, ref: https://github.com/pytest-dev/pytest/issues/3130

+ 1.3.3

  - add python 3 support

+ 1.3.0

  - Multiple results in a single TestCase are seen as one.
    The previous way was never validated by real-life examples.
  - Handle system-out / system-err at the testsuite level


Development & Contribution
==================================================
Pull request is welcome.

1. dev branch is used to accept pull request and do integration
2. main branch is used to do release, once push, a release process will happen automate

Love My Software: https://www.paypal.me/medlab :)

Release Workflow
=========================
1. python setup.py sdist
2. python -m twine upload dist/*

Auto release status
-------------------------

.. image:: https://github.com/medlab/xunitparserx/workflows/Publish%20Python%20%F0%9F%90%8D%20distributions%20%F0%9F%93%A6%20to%20PyPI%20and%20TestPyPI/badge.svg
  :alt: Publish Python 🐍 distributions 📦 to PyPI and TestPyPI

Refs:

1. https://blog.jetbrains.com/pycharm/2017/05/how-to-publish-your-package-on-pypi/
2. https://packaging.python.org/guides/migrating-to-pypi-org/
3. https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/
4. https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions
