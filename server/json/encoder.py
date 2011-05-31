"""New base serializer class to handle full serialization of model objects."""
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from wadofstuff.django.serializers import json
from django.utils.encoding import smart_unicode
    
class Serializer(json.Serializer):
    def serialize(self, queryset, **options):
        """Serialize a queryset with the following options allowed:
            fields - list of fields to be serialized. If not provided then all
            fields are serialized.
            excludes - list of fields to be excluded. Overrides ``fields``.
            relations - list of related fields to be fully serialized.
            extras - list of attributes and methods to include.
            Methods cannot take arguments.
        """
        self.options = options
        self.stream = options.pop("stream", StringIO())
        self.fields = options.pop("fields", [])
        self.excludes = options.pop("excludes", [])
        self.relations = options.pop("relations", [])
        self.extras = options.pop("extras", [])
        self.use_natural_keys = options.pop("use_natural_keys", False)

        self.start_serialization()
        for obj in queryset:
            self.start_object(obj)
            for field in obj._meta.local_fields:
                attname = field.attname
                if field.serialize:
                    if field.rel is None:
                        if attname not in self.excludes:
                            if not self.fields or attname in self.fields:
                                self.handle_field(obj, field)
                    else:
                        if attname[:-3] not in self.excludes:
                            if not self.fields or attname[:-3] in self.fields:
                                self.handle_fk_field(obj, field)
            for field in obj._meta.many_to_many:
                if field.serialize:
                    if field.attname not in self.excludes:
                        if not self.fields or field.attname in self.fields:
                            self.handle_m2m_field(obj, field)
            for extra in self.extras:
                self.handle_extra_field(obj, extra)
            self.end_object(obj)
        self.end_serialization()
        return self.getvalue()

    def handle_fk_field(self, obj, field):
        """
        Called to handle a ForeignKey field.
        Recursively serializes relations specified in the 'relations' option.
        """
        fname = field.name
        related = getattr(obj, fname)
        if related is not None:
            if fname in self.relations:
                # perform full serialization of FK
                serializer = Serializer()
                options = {}
                if isinstance(self.relations, dict):
                    if isinstance(self.relations[fname], dict):
                        options = self.relations[fname]
                print type(serializer.serialize([related], **options))
                self._fields[fname] = serializer.serialize([related], **options)[0]
            else:
                # emulate the original behaviour and serialize the pk value
                if self.use_natural_keys and hasattr(related, 'natural_key'):
                    related = related.natural_key()
                else:
                    if field.rel.field_name == related._meta.pk.name:
                        # Related to remote object via primary key
                        related = related._get_pk_val()
                    else:
                        # Related to remote object via other field
                        related = smart_unicode(getattr(related, field.rel.field_name), strings_only=True)
                self._fields[fname] = related
        else:
            self._fields[fname] = smart_unicode(related, strings_only=True)
