""" Custom Resource model
"""

from django.utils.text import slugify
from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE


class CustomResource(Document):
    """
    Custom resource model
    """

    template = fields.ReferenceField(Template, blank=False)
    name_in_schema = fields.StringField(blank=True)
    title = fields.StringField(unique_with='template')
    slug = fields.StringField()
    description = fields.StringField(blank=True)
    type = fields.StringField(blank=False, choices=(CUSTOM_RESOURCE_TYPE.RESOURCE, CUSTOM_RESOURCE_TYPE.ALL))
    icon = fields.StringField(blank=False)
    icon_color = fields.StringField(blank=True)
    display_icon = fields.BooleanField(blank=True)
    role_choice = fields.StringField(blank=True)
    role_type = fields.StringField(blank=True)
    sort = fields.IntField(unique_with='template', min_value=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(CustomResource, self).save(*args, **kwargs)

    @staticmethod
    def get_all_by_template(template):
        """ Get all custom resource by template.

        Args:
            template:

        Returns:

        """
        return CustomResource.objects(template=template).all()

    @staticmethod
    def get_custom_resource_by_template_and_type(template, type):
        """ Get custom resource by template and type.

        Args:
            template:
            type:

        Returns:

        """
        return CustomResource.objects(template=template, type=type).all()

    @staticmethod
    def get_custom_resource_by_template_and_slug(template, slug):
        """ Get custom resource by template and slug.

        Args:
            template:
            slug:

        Returns:

        """
        try:
            return CustomResource.objects.get(template=template, slug=slug)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

