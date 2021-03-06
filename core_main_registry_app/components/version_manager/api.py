"""
Version Manager API
"""

from core_main_app.components.version_manager import api as version_manager_api
from core_main_registry_app.components.custom_resource import api as custom_resource_api
from core_main_app.commons import exceptions as exceptions


def set_current(version):
    """Set the current version of the object, then saves it.

    Args:
        version:

    Returns:

    """
    if custom_resource_api.get_all_by_template(version).count() == 0:
        raise exceptions.ApiError(
            "Please set custom resources to template before setting it to current."
        )
    version_manager_api.set_current(version)
