from django.http import HttpResponse
from django.shortcuts import render_to_response, get_list_or_404
from models import ContentModel
import json

#--------------------------------------------------------------------------------------
# Expose all the available ContentModels
#--------------------------------------------------------------------------------------
def get_all_models(request, extension):
  all_models = ContentModel.objects.all()
  return view_models(all_models, extension)
  
#--------------------------------------------------------------------------------------
# Expose a single ContentModel
#--------------------------------------------------------------------------------------
def get_model(request, id, extension):
  contentmodels = get_list_or_404(ContentModel, pk=id)
  return view_models(contentmodels, extension)
  
#--------------------------------------------------------------------------------------
# Choose the appropriate format to expose based on the requested extension
#--------------------------------------------------------------------------------------
def view_models(contentmodels, extension):
  if extension == 'json': return as_json(contentmodels)
  elif extension == 'html': return as_html(contentmodels)
  
#--------------------------------------------------------------------------------------
# Convert a set of ContentModel instances to JSON and send as an HttpResponse
#--------------------------------------------------------------------------------------
def as_json(contentmodels):
  data = [ cm.serialized() for cm in contentmodels ]
  return HttpResponse(json.dumps(data), mimetype='application/json')
  
#--------------------------------------------------------------------------------------
# Convert a set of ContentModel instances to HTML and send as an HttpResponse
#--------------------------------------------------------------------------------------
def as_html(contentmodels):
  return render_to_response('contentmodels.html', { 'contentmodels': contentmodels })
