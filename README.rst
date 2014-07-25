========
edX JSME
========

`edx-jsme` is an add on component for the `edX platform
<https://github.com/edx/edx-platform>`_ which provides a new problem type:
'Molecular Structure'.  This problem type integrates the `JSME molecule editor
<http://peter-ertl.com/jsme/>`_ seamlessly into an edX course.

Usage
-----

When `edx-jsme` is installed, a new problem type, 'Molecular Structure', is
available under 'Advanced'.  Once a 'Molecular Structure' problem is added to a
course, the problem template itself contains instructions for editing.

Installation
------------

This package is installed on the Python path in the normal way, eg. via a pip
requirements file.  Then you just need to add this app to `INSTALLED_APPS` for
both STUDIO and the LMS::

    # Add Molecular Structure problem type
    INSTALLED_APPS += ('edx_jsme',)
    
That's it!  Pretty easy.
