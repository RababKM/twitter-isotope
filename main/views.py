from django.shortcuts import render, render_to_response
from django.template import RequestContext
# Create your views here.

from main.models import Tweet

def home(request):

    context = {}

    context['tweets'] = Tweet.objects.all()

    return render_to_response('home.html', context, context_instance=RequestContext(request))