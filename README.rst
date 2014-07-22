==========
edX JSDraw
==========

`edx-jsdraw` is an add on component for the `edX platform 
<https://github.com/edx/edx-platform>`_ which provides a new problem type: 
'JSDraw Input'.  This problem type integrates the `JSDraw molecule editor 
<http://www.scilligence.com/web/jsdraw.aspx>`_ seamlessly into an edX course.

`JSDraw` is not FOSS--it does require a license.  Scilligence has provided a 
license for edx.org to use this component, but it may not be used by other 
parties without a valid license.  As such, this repository is private and should
only be installed by edx.org.

Usage
-----

When `edx-jsdraw` is installed, a new problem type, 'JSDraw Input', is available
under 'Advanced'.  Once a 'JSDraw Input' problem is added to a course, the 
problem template itself contains instructions for editing.

Installation
------------

This package is installed on the Python path in the normal way, eg. via a pip
requirements file.  Then you just need to add this app to `INSTALLED_APPS` for
both STUDIO and the LMS::

    # Add JSDraw problem type
    INSTALLED_APPS += ('edx_jsdraw',)
    
That's it!  Pretty easy.
