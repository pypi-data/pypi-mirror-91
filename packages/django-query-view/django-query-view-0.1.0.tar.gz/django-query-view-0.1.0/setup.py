# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['query_view', 'query_view.templatetags']

package_data = \
{'': ['*'], 'query_view': ['templates/query_view/*']}

install_requires = \
['django-crispy-forms>=1.10.0,<2.0.0',
 'django-extensions>=3.1.0,<4.0.0',
 'django-filter>=2.4.0,<3.0.0',
 'django-taggit>=1.3.0,<2.0.0',
 'django_jinja>=2.7.0,<3.0.0',
 'django_jinja_helpers>=0.1.4,<0.2.0',
 'furl>=2.1.0,<3.0.0',
 'taggit-selectize>=2.10.0,<3.0.0']

setup_kwargs = {
    'name': 'django-query-view',
    'version': '0.1.0',
    'description': 'Django view for querying data',
    'long_description': 'Django Query View\n=================\n\nDjango view for querying data\n\nInstallation\n------------\n\nTo get the latest stable release from PyPi\n\n.. code-block:: bash\n\n    pip install django-query-view\n\nUsage\n-----\n\nSet up models\n-------------\n\n.. code-block:: python\n\n    class TaggedThing(TaggedItemBase):\n        content_object = models.ForeignKey(\'Thing\', on_delete=models.CASCADE)\n\n\n    class Thing(models.Model):\n        name = models.CharField(max_length=200)\n        is_good = models.BooleanField()\n\n        tags = TaggableManager(through=TaggedThing, blank=True)\n\n        def __str__(self):\n            return self.name\n\n    # Subclass TagType\n    class ActorTag(TagType):\n        pass\n\n    # Create your tagged model like this\n    ActorTaggedThing = make_tag_type_tagged_model(\'ActorTaggedThing\', ActorTag, Thing, app_label=\'testproject\')\n\n    # Or like this\n    class ActorTaggedThing(TaggedItemBase):\n        tag = models.ForeignKey(\n            ActorTag,\n            related_name="%(app_label)s_%(class)s_items",\n            on_delete=models.CASCADE,\n        )\n        content_object = models.ForeignKey(Thing, on_delete=models.CASCADE)\n\n        class Meta:\n            unique_together = [\'tag\', \'content_object\']\n\nCreate a typed tagged item\n-----------------------------\n\n.. code-block:: python\n\n    t = Tag.objects.get(name=\'clint eastwood\')\n    ActorTaggedThing.objects.create(content_object=thing, tag=t.actortag)\n\nRun the test project\n--------------------\n\n.. code-block:: bash\n\n    python manage.py migrate\n    python manage.py loaddata testproject/fixtures/tag_thing.json\n    python manage.py runserver\n\nDump fixture\n------------\n\n.. code-block:: bash\n\n    python manage.py dumpdata --indent 4 testproject.Thing testproject.TaggedThing taggit.Tag testproject.LanguageTag testproject.LanguageTaggedThing testproject.DirectorTag testproject.DirectorTaggedThing testproject.ActorTag testproject.ActorTaggedThing --output testproject/fixtures/tag_thing.json\n',
    'author': 'Enrico Barzetti',
    'author_email': 'enricobarzetti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/enricobarzetti/django-query-view',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
