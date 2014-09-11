from django.shortcuts import render, render_to_response
from django.template import RequestContext

from django.conf import settings

# Create your views here.

def index(request):
  return render_to_response('index.html', context_instance=RequestContext(request))
  
def contact(request):
  return render_to_response('contact.html', context_instance=RequestContext(request))