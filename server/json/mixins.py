from server.json.encoder import JsonEncoder

class JsonEncodable(JsonEncoder):

    @classmethod
    def json_encode_all_entities(cls, **options):
        if hasattr(cls,'relations_included_in_json') and not options.get('relations'):
            options['relations'] = cls.relations_included_in_json
            serialized_str = JsonEncoder().serialize(list(cls.objects.all()), **options)
            #eliminate brackets in the beginning and the end
            return serialized_str
        
    
    def json_encode(self, **options):
        if hasattr(self,'relations_included_in_json') and not options.get('relations'):
            options['relations'] = self.relations_included_in_json
        serialized_str = self.serialize([self], **options)
        #eliminate brackets in the beginning and the end
        return serialized_str[1:len(serialized_str)-1]
    
