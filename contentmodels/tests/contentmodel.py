from django.test import TestCase
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
import datetime, os, shutil
from contentmodels.models import ContentModel, ModelVersion

class ContentModelTestCase(TestCase):
  fixtures = [
      "tests/cm-example.json"
    ]
    
  def setUp(self):
    self.example = ContentModel.objects.get(label="example")
  
  def tearDown(self):
    # Remove any files that may have been added in the course of adding versions
    example_path = os.path.join(settings.MEDIA_ROOT, self.example.folder_path())
    if os.path.exists(example_path):
      shutil.rmtree(example_path)
  
  def createTwoVersions(self):
    """Create two version, return the newer of the two"""
    # Create dummy files to be the XSD and XLS files
    dummy_xsd_content = ContentFile("Dummy Schema File")
    dummy_xls_content = ContentFile("Dummy Excel File")
    dummy_xsd_file = File(dummy_xsd_content, "dummyFile.xsd")
    dummy_xls_file = File(dummy_xls_content, "dummyFile.xls")
    
    # Create a version right now
    v1 = ModelVersion.objects.create(
        content_model = self.example,
        version = "2.0",
        xsd_file = dummy_xsd_file,
        xls_file = dummy_xsd_file
      )
      
    # Create an older version
    v2 = ModelVersion.objects.create(
        content_model = self.example,
        version = "1.0",
        date_created = datetime.datetime.now() - datetime.timedelta(days=3),
        xsd_file = dummy_xsd_file,
        xls_file = dummy_xsd_file
      )
      
    # Return the newer version
    return v2
    
  def test_name(self):
    """The model's name should be equal to its title"""
    self.assertEqual(self.example.__unicode__(), self.example.title)
    
  def test_folder_path(self):
    """The model's folder path should be a slugified version of the title"""
    self.assertEqual(self.example.folder_path(), slugify(self.example.title))
    
  def test_latest_version_for_null(self):
    """When there are no versions of a model, the model's latest_version should return None"""
    self.assertIsNone(self.example.latest_version())
  
  def test_latest_version(self):
    """The model's latest_version should return the correct version"""
    v = self.createTwoVersions()    
    self.assertEqual(self.example.latest_version(), v)
        
  def test_latest_version_number_for_null(self):
    """When there are no versions of a model, the model's latest_version_number should return None"""
    self.assertIsNone(self.example.latest_version_number())
      
  def test_latest_version_number(self):
    """The model's latest_version_number should return the correct number"""
    v = self.createTwoVersions()
    self.assertEqual(self.example.latest_version_number(), v.version)
    
  def test_date_updated_for_null(self):
    """When there are no versions the model's update date should be None"""
    self.assertIsNone(self.example.date_updated())
    
  def test_date_updated(self):
    """The model's date_updated should match the creation date of the latest version"""
    v = self.createTwoVersions()
    self.assertEqual(self.example.date_updated(), v.date_created)
    
  def test_iso_date_updated_for_null(self):
    """When there are no versions the model's iso_date_updated should be None"""
    self.assertIsNone(self.example.iso_date_updated())
    
  def test_iso_date_updated(self):
    """The model's iso_date_updated should be an ISO representation of the latest version's creation date"""
    v = self.createTwoVersions()
    self.assertEqual(self.example.iso_date_updated(), v.date_created.isoformat())
  
  
    
    
  