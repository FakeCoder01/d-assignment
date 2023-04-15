import json
from django.http import JsonResponse
from .models import Hackathon
from uuid import UUID
from .serializers import HackathonSerializer
# Create your views here.

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj) :
        try:
            if isinstance(obj, UUID):
                return obj.hex
            return json.JSONEncoder.default(self.obj)
        except:
            return    


def get_all_hackathons(request):
    try:
        return JsonResponse(json.dumps({
            "status_code" : 200,
            "hackathons" : list(Hackathon.objects.all().values())
        }, cls=UUIDEncoder), safe=False)
    except Exception as err:
        print(err)
        return JsonResponse(json.dumps({
            "status_code" : 500
        }), safe=False)
    

def get_hackathon(request, id):
    try:
        if Hackathon.objects.filter(id=id).exists():
            queryset = Hackathon.objects.get(id=id)
            data = HackathonSerializer(queryset)
            return JsonResponse(json.dumps({
                "status_code" : 200,
                "hackathon" : data.data,
                "timeline" : queryset.get_formated_datetime()
            }), safe=False)
        return JsonResponse(json.dumps({
            "status_code" : 404
        }), safe=False)  
    except Exception as err:
        print(err)
        return JsonResponse(json.dumps({
            "status_code" : 500
        }), safe=False)    