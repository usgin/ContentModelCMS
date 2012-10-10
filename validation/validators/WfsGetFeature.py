from WfsBase import WfsBase

#--------------------------------------------------------------------------------------
# A class representing a WFS GetFeature document.
#   Constructor requires a WfsCapabilities object, the requested TypeName and MaxFeatures
#   Inherits from WfsBase, which performs HTTP requests and XML parsing
#--------------------------------------------------------------------------------------
class WfsGetFeature(WfsBase):
  def __init__(self, capabilities, feature_type, number_of_features):
    # WfsCapabilites object constructs the GetFeature URL
    self.url = capabilities.get_feature_url(feature_type, number_of_features)
    self.feature_type = feature_type
  
  #--------------------------------------------------------------------------------------
  # Function to perform schema validation and return results and errors
  #    over an entire wfs:FeatureCollection
  #--------------------------------------------------------------------------------------  
  def validate(self, modelversion):
    # Retrieve the GetFeature document, parsed by lxml
    parsed_doc = self.fetch_parsed_doc()
    
    # Figure out namespaces...
    ns = {
      "aasg": "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/aqueouschemistry/1.9"
    }
    
    # Gather elements of the requested FeatureType
    elements = parsed_doc.xpath("//%s" % self.feature_type, namespaces=ns)
    
    # Retrieve the XMLSchema object responsible for validating this ModelVersion's schema
    schema = modelversion.schema_validator()
    
    # Perform validation on each element
    return ValidationResults(elements, schema)
  
#--------------------------------------------------------------------------------------
# Class to perform schema validation for each element in a wfs:FeatureCollection
#--------------------------------------------------------------------------------------
class ValidationResults():
  results = []
  valid = True
  
  def __init__(self, elements, schema):
    self.number_of_elements = len(elements)
    for element in elements:
      valid = schema.validate(element)
      if not valid: self.valid = False
      self.results.append({
          "valid": valid,
          "element": element                   
        })
      self.errors = schema.error_log
  
  def valid_count(self):
    return len([ result for result in self.results if result['valid'] ])
  
  def invalid_count(self):
    return len([ result for result in self.results if not result['valid'] ])
    
    