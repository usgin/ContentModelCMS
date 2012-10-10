from WfsBase import WfsBase

class WfsGetFeature(WfsBase):
  def __init__(self, capabilities, feature_type, number_of_features):
    self.url = capabilities.get_feature_url(feature_type, number_of_features)
        
  def validate(self, modelversion):
    parsed_doc = self.fetch_parsed_doc()
    
    schema = modelversion.schema_validator()
    
    valid = schema.validate(parsed_doc)
    
    return valid, schema.error_log