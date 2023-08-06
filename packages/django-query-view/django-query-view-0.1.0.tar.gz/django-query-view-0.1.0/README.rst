Django Query View
=================

Django view for querying data

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-query-view

Usage
-----

Set up models
-------------

.. code-block:: python

    class TaggedThing(TaggedItemBase):
        content_object = models.ForeignKey('Thing', on_delete=models.CASCADE)


    class Thing(models.Model):
        name = models.CharField(max_length=200)
        is_good = models.BooleanField()

        tags = TaggableManager(through=TaggedThing, blank=True)

        def __str__(self):
            return self.name

    # Subclass TagType
    class ActorTag(TagType):
        pass

    # Create your tagged model like this
    ActorTaggedThing = make_tag_type_tagged_model('ActorTaggedThing', ActorTag, Thing, app_label='testproject')

    # Or like this
    class ActorTaggedThing(TaggedItemBase):
        tag = models.ForeignKey(
            ActorTag,
            related_name="%(app_label)s_%(class)s_items",
            on_delete=models.CASCADE,
        )
        content_object = models.ForeignKey(Thing, on_delete=models.CASCADE)

        class Meta:
            unique_together = ['tag', 'content_object']

Create a typed tagged item
-----------------------------

.. code-block:: python

    t = Tag.objects.get(name='clint eastwood')
    ActorTaggedThing.objects.create(content_object=thing, tag=t.actortag)

Run the test project
--------------------

.. code-block:: bash

    python manage.py migrate
    python manage.py loaddata testproject/fixtures/tag_thing.json
    python manage.py runserver

Dump fixture
------------

.. code-block:: bash

    python manage.py dumpdata --indent 4 testproject.Thing testproject.TaggedThing taggit.Tag testproject.LanguageTag testproject.LanguageTaggedThing testproject.DirectorTag testproject.DirectorTaggedThing testproject.ActorTag testproject.ActorTaggedThing --output testproject/fixtures/tag_thing.json
