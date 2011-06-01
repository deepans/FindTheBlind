"""New base serializer class to handle full serialization of model objects."""
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from wadofstuff.django.serializers import python
from django.utils.encoding import smart_unicode
from django.db.models.fields.related import OneToOneField

class Serializer(python.Serializer):
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
            for relation in obj._meta.get_all_related_objects():
                if isinstance(relation.field, OneToOneField):
                    if relation.field.serialize:
                        if relation.var_name not in self.excludes:
                            if not self.fields or relation.var_name in self.fields:
                                self.handle_reverse_relation(obj, relation)
            for extra in self.extras:
                self.handle_extra_field(obj, extra)
            self.end_object(obj)
        self.end_serialization()
        return self.getvalue()
    
    def handle_reverse_relation(self, obj, relation):
        """
        Called to handle a reverse relations.
        Recursively serializes relations specified in the 'relations' option.
        """
        fname = relation.var_name
        related = getattr(obj, fname)
        if related is not None:
            if fname in self.relations:
                # perform full serialization of relation
                serializer = Serializer()
                options = {}
                if isinstance(self.relations, dict):
                    if isinstance(self.relations[fname], dict):
                        options = self.relations[fname]
                self._fields[fname] = serializer.serialize([related], **options)[0]
            else:
                # emulate the original behaviour and serialize the pk value
                if self.use_natural_keys and hasattr(related, 'natural_key'):
                    related = related.natural_key()
                else:
                    # Related to remote object via primary key
                    related = related._get_pk_val()
                self._fields[fname] = related
        else:
            self._fields[fname] = smart_unicode(related, strings_only=True)

from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder

class JsonEncoder(Serializer):
    """
    Convert a queryset to JSON.
    """
    def end_serialization(self):
        """Output a JSON encoded queryset."""
        simplejson.dump(self.objects, self.stream, cls=DjangoJSONEncoder,
                        **self.options)

    def getvalue(self):
        """
        Return the fully serialized queryset (or None if the output stream
        is not seekable).
        """
        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()
            

