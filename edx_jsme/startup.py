"""
Django initialization.
"""
from edxmako import add_lookup
from xmodule.x_module import ResourceTemplates


def run():
    """
    Add our templates to the Django site.
    """
    # Add our problem boiler plate templates
    ResourceTemplates.template_packages.append(__name__)

    # Add our mako templates
    add_lookup('main', 'templates', __name__)      # For LMS
    add_lookup('lms.main', 'templates', __name__)  # For CMS
