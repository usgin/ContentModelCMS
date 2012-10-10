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
    
  def validate(self, modelversion):
    # Retrieve the GetFeature document, parsed by lxml
    parsed_doc = self.fetch_parsed_doc()
    
    # Retrieve the XMLSchema object responsible for validating this ModelVersion's schema
    schema = modelversion.schema_validator()
    
    # Perform validation
    valid = schema.validate(parsed_doc)
    
    # Return the validation result and error log
    return valid, schema.error_log