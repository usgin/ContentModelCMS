from django.conf.urls import patterns, url

urlpatterns = patterns('contentmodels.views',

  # Get all the ContentModels as JSON or HTML
  url(r'^contentmodels\.(?P<extension>json|html)', 'get_all_models'),
  
  # Get a single ContentModel as JSON or HTML
  url(r'^contentmodel/(?P<id>\d*)\.(?P<extension>json|html)', 'get_model')
  
)
