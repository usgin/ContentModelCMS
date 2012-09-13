from django.db import models
from django.template.defaultfilters import slugify
from os import path

#--------------------------------------------------------------------------------------
# Function that gets the path for a uploaded files.
#   File path will be content-model-slug/version-number/filename      
#--------------------------------------------------------------------------------------
def get_file_path(instance, filename):
  return '%s/%s/%s' % (instance.content_model.folder_path(), instance.version, filename)

#--------------------------------------------------------------------------------------
# This class represent specific USGIN content-models, which are built to convey
#   specific types of geoscience information.
#--------------------------------------------------------------------------------------
class ContentModel(models.Model):
  class Meta:
    ordering = ['title']  # Defines the order of any list of ContentModels
    
  # Define the class data members
  title = models.CharField(max_length=2500)
  uri = models.CharField(max_length=2500, unique=True)
  description = models.TextField()
  discussion = models.TextField(blank=True)
  status = models.TextField(blank=True)
  
  # Define the "display name" for an instance
  def __unicode__(self):
    return self.title
  
  # Define the folder path for an instance -- just a simplification of the title
  def folder_path(self):
    return slugify(self.title)
  
  # Simple pointer to the latest version of a instance
  def latest_version(self):
    return self.modelversion_set.latest('date_created')
  
  # The updated date for an instance is the last time that a version was created
  def date_updated(self):
    return self.latest_version().date_created
  
  # Provide a link to the latest version's XSD file
  def latest_xsd_file(self):
    latest = self.latest_version()
    return '<a href="%s">%s</a>' % (latest.xsd_file.url, latest.xsd_filename())
  latest_xsd_file.allow_tags = True
  
  # Provide a link to the latest version's XLS file
  def latest_xls_file(self):
    latest = self.latest_version()
    return '<a href="%s">%s</a>' % (latest.xls_file.url, latest.xls_filename())
  latest_xls_file.allow_tags = True
  
  # Return the instance as a dictionary that can be easily converted to JSON
  #   Include a list of versions relevant to this content model
  def serialized(self):
    as_json = {
      'title': self.title,
      'uri': self.uri,
      'description': self.description,
      'discussion': self.discussion,
      'status': self.status,
      'date_updated': self.date_updated().isoformat(),
      'versions': [ mv.serialized() for mv in self.modelversion_set.all() ]
    }    
    return as_json

#--------------------------------------------------------------------------------------
# This class represents a specific version of a particular content-model. 
#   A one-to-many relationship exists between ContentModels and ModelVersions. 
#--------------------------------------------------------------------------------------
class ModelVersion(models.Model):
  class Meta:
    ordering = ['version']  # Defines the order of any list of ModelVersions
    
  # Define the models data members
  content_model = models.ForeignKey('ContentModel')
  version = models.CharField(max_length=10)
  date_created = models.DateField(auto_now_add=True)
  xsd_file = models.FileField(upload_to=get_file_path)
  xls_file = models.FileField(upload_to=get_file_path)
  
  # Define the "display name" for an instance
  def __unicode__(self):
    return '%s v. %s' % (self.content_model.title, self.version)
  
  # Define the URI for this version -- it is simply the version number appended to the ContentModel.uri  
  def uri(self):
    return '%s/%s' % (self.content_model.uri.strip('/'), self.version)
  
  # Return just the base name of the XSD file without any associated file path
  def xsd_filename(self):
    return path.basename(self.xsd_file.name)
    
  # Return just the base name of the XLS file without any associated file path
  def xls_filename(self):
    return path.basename(self.xls_file.name)
  
  # Return an HTML anchor tag for the XSD file
  def xsd_link(self):
    return '<a href="%s">%s</a>' % (self.xsd_file.url, self.xsd_filename())
  xsd_link.allow_tags = True  # This lets the admin interface show the anchor

  # Return an HTML anchor tag for the XLS file
  def xls_link(self):
    return '<a href="%s">%s</a>' % (self.xls_file.url, self.xls_filename())
  xls_link.allow_tags = True  # This lets the admin interface show the anchor
        
  # Return the instance as a dictionary that can be easily converted to JSON.
  #   Contains URLs to directly download files 
  def serialized(self):
    as_json = {
      'uri': self.uri(),
      'version': self.version,
      'date_created': self.date_created.isoformat(),
      'xsd_file_path': self.xsd_file.url,
      'xls_file_path': self.xls_file.url
    }    
    return as_json