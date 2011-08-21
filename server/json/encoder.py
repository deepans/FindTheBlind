from json.utils import process_item_or_list

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
                    if relation.field.serialize:
                        if relation.var_name not in self.excludes:
                            if not self.fields or relation.var_name in self.fields:
                                if isinstance(relation.field, OneToOneField):
                                    self.handle_reverse_o2o_relation(obj, relation)
                                else:
                                    self.handle_reverse_fk_relation(obj, relation)
            for extra in self.extras:
                self.handle_extra_field(obj, extra)
            self.end_object(obj)
        self.end_serialization()
        return self.getvalue()

    def __handle_reverse_relation(self, fname, related):
        def serialize_relation(rel, **args):
            return serializer.serialize([rel], **args)[0]
            
        if related:
            if fname in self.relations:
                # perform full serialization of relation
                serializer = Serializer()
                options = {}
                if isinstance(self.relations, dict):
                    if isinstance(self.relations[fname], dict):
                        options = self.relations[fname]
                self._fields[fname] = process_item_or_list(serialize_relation, related, **options)        
            else:
                # emulate the original behaviour and serialize the pk value
                if self.use_natural_keys and hasattr(related, 'natural_key'):
                    related = process_item_or_list(lambda rel: rel.natural_key(), related)
                else:
                    # Related to remote object via primary key
                    related = process_item_or_list(lambda rel: rel._get_pk_val(), related)
                self._fields[fname] = related
        else:
            self._fields[fname] = smart_unicode(related, strings_only=True)


    def handle_reverse_fk_relation(self, obj, relation):
        fname = relation.field.rel.related_name 
        fname = fname if fname else (relation.var_name + '_set')
        for related in getattr(obj, fname).all():
            self.__handle_reverse_relation(fname, [related for related in getattr(obj, fname).all()])
            
    def handle_reverse_o2o_relation(self, obj, relation):
        """
        Called to handle a reverse relations.
        Recursively serializes relations specified in the 'relations' option.
        """
        fname = relation.var_name
        try:
            related = getattr(obj, fname)
        except relation.model.DoesNotExist:
            pass
        else:
            self.__handle_reverse_relation(fname, related)

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
                self._fields[fname] = serializer.serialize([related],
                                                           **options)[0]
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
                        related = smart_unicode(getattr(related,
                                                        field.rel.field_name), strings_only=True)
                self._fields[fname] = related
        else:
            self._fields[fname] = smart_unicode(related, strings_only=True)

    def handle_m2m_field(self, obj, field):
        """
        Called to handle a ManyToManyField.
        Recursively serializes relations specified in the 'relations' option.
        """
        if field.rel.through._meta.auto_created:
            fname = field.name
            if fname in self.relations:
                # perform full serialization of M2M
                serializer = Serializer()
                options = {}
                if isinstance(self.relations, dict):
                    if isinstance(self.relations[fname], dict):
                        options = self.relations[fname]
                self._fields[fname] = [
                    serializer.serialize([related], **options)[0]
                    for related in getattr(obj, fname).iterator()]
            else:
                # emulate the original behaviour and serialize to a list of 
                # primary key values
                if self.use_natural_keys and hasattr(field.rel.to, 'natural_key'):
                    m2m_value = lambda value: value.natural_key()
                else:
                    m2m_value = lambda value: smart_unicode(
                        value._get_pk_val(), strings_only=True)
                self._fields[fname] = [m2m_value(related)
                                       for related in getattr(obj, fname).iterator()]

        
    def end_object(self, obj):
        """
        Called when serializing of an object ends.
        """
        fields = {
            "model"  : smart_unicode(obj._meta),
            "pk"     : smart_unicode(obj._get_pk_val(), strings_only=True)}
        fields.update(self._fields)
        
        self.objects.append(fields)
        if self._extras:
            self.objects[-1]["extras"] = self._extras
        self._fields = None
        self._extras = None

        
            
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
            

