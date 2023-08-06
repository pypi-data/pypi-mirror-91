=======
History
=======

1.10.3 (2021-01-15)
-------------------

* Avoid 1.10.2post1 bug with pyup updates

1.10.2 (2021-01-12)
-------------------

* Provide CVSS values on full report for CVEs (requires a premium PyUp subscription)
* Fixed used DB wrong info
* Support line breaks on advisories

1.10.1 (2021-01-03)
-------------------

* Reduced Docker image and Binary size
* Added bare and json outputs to license command

1.10.0 (2020-12-20)
-------------------

* Added README information about Python 2.7 workaround
* Adjusted some pricing information
* Fixed MacOS binary build through AppVeyor
* Added the ability to check packages licenses (requires a premium PyUp subscription)

1.9.0 (2020-04-27)
------------------

* Dropped Python 2.7 support, requiring Python 3.5+
* Binary adjustments and enhancements on top of reported vulnerability
* Using tox to help with local tests against different Python versions

1.8.7 (2020-03-10)
------------------

* Fixed a hidden import caused the binary to produce errors on Linux.

1.8.6 (2020-03-10)
------------------

* Safety is now available as a binary release for macOS, Windows and Linux.

1.8.5 (2019-02-04)
------------------

* Wrap words in full report (Thanks @mgedmin)
* Added Dockerfile and readme instructions (Thanks @ayeks)
* Remove API dependency on pip (Thanks @benjaminp)

1.8.4 (2018-08-03)
------------------

* Update cryptography dependency from verision 1.9 to version 2.3 due to security vulnerability

1.8.3b (2018-07-24)
------------------

* Allows both unicode and non-unicode type encoding when parsing requriment files

1.8.2 (2018-07-10)
------------------

* Fixed unicode error

1.8.1 (2018-04-06)
------------------

* Fixed a packaging error with the dparse dependency

1.8.0 (2018-04-05)
------------------

* Safety now support pip 10

1.7.0 (2018-02-03)
------------------

* Safety now shows a filename if it finds an unpinned requirement. Thanks @nnadeau
* Removed official support for Python 2.6 and Python 3.3. Thanks @nnadeau

1.6.1 (2017-10-20)
------------------

* Fixed an error that caused the CLI to fail on requirement files/stdin.

1.6.0 (2017-10-20)
------------------

* Added an indicator which DB is currently used
* Added a package count how many packages have been checked
* Allow multiple version of the same library. Thanks @thatarchguy

1.5.1 (2017-07-20)
------------------

* Fixed an error on unpinned VCS requirements. This is a regression, see https://github.com/pyupio/safety/issues/72

1.5.0 (2017-07-19)
------------------

* Internal refactoring. Removed dependency on setuptools and switched to the new dparse library.

1.4.1 (2017-07-04)
------------------

* Fixed a bug where absence of ``stty`` was causing a traceback in ``safety
  check`` on Python 2.7 for Windows.

1.4.0 (2017-04-21)
------------------

* Added the ability to ignore one (or multiple) vulnerabilities by ID via the `--ignore`/`-i` flag.

1.3.0 (2017-04-21)
------------------

* Added `--bare` output format.
* Added a couple of help text to the command line interface.
* Fixed a bug that caused requirement files with unpinned dependencies to fail when using
 a recent setuptools release.

1.2.0 (2017-04-06)
------------------

* Added JSON as an output format. Use it with the `--json` flag. Thanks @Stype.

1.1.1 (2017-03-27)
------------------

* Fixed terminal size detection when fed via stdin.

1.1.0 (2017-03-23)
------------------

* Compatibility release. Safety should now run on macOs, Linux and Windows with Python 2.7, 3.3-3.6.
 Python 2.6 support is available on a best-effort basis on Linux.

1.0.2 (2017-03-23)
------------------

* Fixed another error on Python 2. The fallback function for get_terminal_size wasn't working correctly.

1.0.1 (2017-03-23)
------------------

* Fixed an error on Python 2, FileNotFoundError was introduced in Python 3.

1.0.0 (2017-03-22)
------------------

* Added terminal size detection. Terminals with fewer than 80 columns should now display nicer reports.
* Added an option to load the database from the filesystem or a mirror that's reachable via http(s).
 This can be done by using the --db flag.
* Added an API Key option that uses pyup.io's vulnerability database.
* Added an option to cache the database locally for 2 hours. The default still is to not use the cache. Use the --cache flag.


0.6.0 (2017-03-10)
------------------

* Made the requirements parser more robust. The parser should no longer fail on editable requirements
  and requirements that are supplied by package URL.
* Running safety requires setuptools >= 16

0.5.1 (2016-11-08)
------------------

* Fixed a bug where not all requirement files were read correctly.

0.5.0 (2016-11-08)
------------------

* Added option to read requirements from files.

0.4.0 (2016-11-07)
------------------

* Filter out non-requirements when reading from stdin.

0.3.0 (2016-10-28)
------------------

* Added option to read from stdin.

0.2.2 (2016-10-21)
------------------

* Fix import errors on python 2.6 and 2.7.

0.2.1 (2016-10-21)
------------------

* Fix packaging bug.

0.2.0 (2016-10-20)
------------------

* Releasing first prototype.

0.1.0 (2016-10-19)
------------------

* First release on PyPI.
