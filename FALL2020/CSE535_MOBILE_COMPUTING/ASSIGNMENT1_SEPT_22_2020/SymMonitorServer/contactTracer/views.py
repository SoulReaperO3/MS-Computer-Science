from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.

def index(request):
    return render(request,'contactTracer/index.html')

@csrf_exempt
def traceContact(request, subjectID, date):
	print(subjectID)
	print(date)


	# if request.method == 'GET':
	# 	return JsonResponse(json.dumps(retData), safe = False)
