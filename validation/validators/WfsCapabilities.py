from lxml import etree
import urllib2

#--------------------------------------------------------------------------------------
# A class representing a WFS GetCapabilities document.
#   Constructor requires a URL for the GetCapabilities document
#--------------------------------------------------------------------------------------
class WfsCapabilities():
  url = None              # The URL of the WFS GetCapabilities document, passed into class constructor
  url_is_valid = True     # Whether or not the URL points to a valid WFS GetCapabilities document
  errors = []             # Any errors encountered during fetching and parsing of the given URL
  doc = None              # The document returned from the given URL
  parsed_doc = None       # The document parsed by lxml and represented as an ElementTree
  version = None          # The WFS version, parsed from the GetCapabilites document
  feature_types = []      # The names of FeatureTypes available from the WFS
  
  # Constructor function. Requires a URL passed in as a string
  def __init__(url):
    # Set the object's URL value
    self.url = url
    
    # Get a list of FeatureTypes. Any errors encountered in the process will be logged to self.errors
    self.set_feature_types()
  
  # Function to perform an HTTP request to get the document at the given URL
  def fetch_document(self):
    # Just return the document if it has already been fetched
    if self.doc is not None: return self.doc
    
    # Open the URL and return the response
    try:
      self.doc = urllib2.urlopen(self.url)
      return self.doc
    
    # There was an error processing the URL
    except urllib2.URLError, err:
      self.errors.append({"urlError": err})
    
    # There was an HTTP error retrieving the document  
    except urllib2.HTTPError, err:
      self.errors.append({"httpError": err})
    
    # Some error was encountered, set the invalid flag and return nothing
    self.url_is_valid = False
    return None
  
  # Function to parse the returned document into an ElementTree
  def fetch_parsed_doc(self):
    # Just return the ElementTree if it has already been parsed
    if self.parsed_doc is not None: return self.parsed_doc
    
    # Fetch the document
    doc = self.fetch_document()
    
    # Parse the document using lxml.etree and return the ElementTree
    try:
      self.parsed_doc = etree.parse(doc)
      return self.parsed_doc
    
    # There was an error while parsing the document
    except etree.ParseError, err:
      self.errors.append({"parseError": err})
    
    # Some error was encountered, set the invalid flag and return nothing  
    self.url_is_valid = False
    return None
  
  # Function to set FeatureType list according to the document at the given URL
  def set_feature_types(self):
    # Fetch the parsed document
    parsed_doc = self.fetch_parsed_doc()
    
    # Determine the WFS version, drop lxml's "smart string" in this case
    self.version = parsed_doc.xpath('/@version', smart_strings=False)
    
    # Namespaces are different depending on the version
    if self.version is '1.0.0' or '1.1.0':
      ns = { 'wfs': 'http://www.opengis.net/wfs' }            
    elif self.version is '2.0.0':
      ns = { 'wfs': 'http://www.opengis.net/wfs/2.0' }
    else:
      # There was some issue with getting the WFS version
      self.errors.append({"capabilitiesError": "Could not determine WFS version"})
      self.url_is_valid = False
      return
    
    # Get the FeatureType Names via XPath, plug them into self.feature_types
    feature_type_elements = parsed_doc.xpath('/wfs:FeatureTypeList/wfs:FeatureType/wfs:Name', namespaces=ns)
    self.feature_types = [ ftype.text for ftype in feature_type_elements ]
    
  # Function to spell out a GetFeature URL given the name of a FeatureType and the number of features
  def get_feature_url(self, feature_type_name, number_of_features):
    # Return nothing if the URL is invalid
    if not self.url_is_valid: return None
    
    # Fetch the parsed_doc
    parsed_doc = self.fetch_parsed_doc()
    
    # Make sure that the FeatureType requested is one of the available FeatureTypes
    if feature_type_name not in self.feature_types: return None 
    
    # Namespace setup for later XPath expressions
    ns = { 'wfs': 'http://wwww.opengis.net/wfs', 'ows': 'http://www.opengis.net/ows' }
    
    # Read URLs for GetFeature operations from the GetCapabilities document
    if self.version is '1.0.0':
      base_url = parsed_doc.xpath('/wfs:Capability/wfs:Request/wfs:GetFeature/wfs:DCPType/wfs:HTTP/wfs:Get/@onlineResource')
    elif self.version is '1.1.0':
      base_url = parsed_doc.xpath('/ows:OperationsMetadata/ows:Operation[name=GetFeature]/ows:DCP/ows:HTTP/ows:Get/@xlink:href')
    elif self.version is '2.0.0':
      # WFS 2.0 uses a new wfs namespace
      ns['wfs'] = 'http://www.opengis.net/wfs/2.0'
      base_url = parsed_doc.xpath('/ows:OperationsMetadata/ows:Operation[name=GetFeature]/ows:DCP/ows:HTTP/ows:Get/@xlink:href')      
    else:
      # There was some issue locating the GetFeature operation's description
      self.errors.append({"capabilitiesError": "Could not determine the GetFeature URL"})
      self.url_is_valid = False
      return None
      
    # Append query parameters and return
    param_values = (base_url, self.version, feature_type_name, str(number_of_features))
    return "%s&service=WFS&version=%s&request=GetFeature&typename=%s&maxfeatures=%s" % param_values