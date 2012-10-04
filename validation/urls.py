from django.conf.urls import patterns, url

urlpatterns = patterns('validation.validators',

  # Validation form, and form submission
  url('^wfs$', 'validate_wfs_form')

)