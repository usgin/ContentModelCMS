from contentmodels.models import ContentModel, ModelVersion
from WfsCapabilities import WfsCapabilities
from django import forms
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render

#--------------------------------------------------------------------------------------
# A Form to gather user's input: Just the WFS URL
#   Also validates that the URL returns a GetCapabilities doc and that the WFS
#   provides some FeatureTypes
#--------------------------------------------------------------------------------------
class WfsSelectionForm(forms.Form):
  wfs_get_capabilities_url = forms.URLField() # Just one field in this form: the WFS GetCapabilities URL
  
  # Function to validate the wfs_get_capabilites_url
  def clean_wfs_get_capabilities_url(self):
    # Get the URL that the user provided
    url = self.cleaned_data['wfs_get_capabilities_url']
    
    # Check the validity of the given URL
    capabilities = WfsCapabilities(url)
    if not capabilities.url_is_valid:
      raise forms.ValidationError('The URL given is invalid')
      
    # Check that the WFS provides some FeatureTypes
    if len(capabilities.feature_types) is 0:
      raise forms.ValidationError('The WFS you specified does not provide any FeatureTypes')
    
#--------------------------------------------------------------------------------------
# A Form to gather user's input required to validate a WFS against some ModelVersion
#   Note that the constructor for the form requires a URL
#--------------------------------------------------------------------------------------
class WfsValidationParametersForm(forms.Form):
  # Redefine the constructor for this form to accomodate an input URL
  def __init__(self, url, *args, **kwargs):
    super(forms.Form, self).__init__(*args, **kwargs)
    
    # Set the feature_type field's choices to the available WFS FeatureTypes
    capabilities = WfsCapabilities(url)
    self.fields['feature_type'].choices = [ (typename, typename) for typename in capabilities.feature_types ]
    
    # Set the form object's capabilities_url
    self.url = url
    
  # Define form fields
  url = forms.URLField(widget=forms.HiddenInput) 
  content_model = forms.ModelChoiceField(queryset=ContentModel.objects.all())
  version = forms.ModelChoiceField(queryset=ModelVersion.objects.all())
  feature_type = forms.ChoiceField(choices=[])
  number_of_features = forms.IntegerField()

def validate_wfs_form(req):
  # Insure that HTTP requests are of the proper type
  allowed = [ 'GET', 'POST' ] 
  if req.method not in allowed:
    return HttpResponseNotAllowed(allowed)
  
  # When a data is passed in during a POST request...  
  if req.method is 'POST':
    # ... determine if the req.POST contains WfsSelectionForm or WfsValidationParametersForm
    
    # This is a WfsValidationParametersForm
    if 'version' in req.POST:
      form = WfsValidationParametersForm(req.POST)
      
      # Check the form's validity
      if form.is_valid:
        # Perform WFS Validation
        return HttpResponse('Now the WFS would be validated')
      
    # Otherwise it is treated as a WfsSelectionForm
    else:
      form = WfsSelectionForm(req.POST)
      
      # Check the form's validity
      if form.is_valid:
        # We need to send back a WfsValidationParametersForm, which takes a URL as input
        second_form = WfsValidationParametersForm(url=form.cleaned_data['wfs_get_capabilities_url'])
        return render(req, 'wfs-form.html', { 'form': second_form })
        
  # A GET request should just a data-free WfsSelectionForm
  else:
    form = WfsSelectionForm()
    
  # You'll get here if it was a GET request, or if form validation failed
  return render(req, 'wfs-form.html', { 'form': form })