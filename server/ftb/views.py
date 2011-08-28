from ftb.models import Patient
from django.http import HttpResponse
from server.json.persister import persist
from server.json.persister import ReplaceLatestMergeStrategy

def patients(request):
    def doGET(request):
        return HttpResponse(Patient.json_encode_all_entities(), mimetype='application/json')

    def doPOST(request):
        try:
            persist(request.POST['patients'], ReplaceLatestMergeStrategy)
        except KeyError:
            return HttpResponse(status=400)
        else:
            return HttpResponse(status=201)
    if request.method == 'GET':
        return doGET(request)
    elif request.method == 'POST':
        return doPOST(request)