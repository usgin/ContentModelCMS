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
        xls_file = dummy_xls_file
      )
      
    # Return the newer version
    return v2

  def stripped_regex(self):
    return "dataschema/%s/" % self.example.label

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
    
  #Created by Genhan
  def test_absolute_latest_xsd_path_for_null(self):
    """When there are no versions the absolute path to the latest version's XSD file is none"""
    self.assertIsNone(self.example.absolute_latest_xsd_path())
 
  def test_absolute_latest_xsd_path(self):
    """The xsd file should be for the latest version"""
    v = self.createTwoVersions()
    v_abs_path = '%s%s' % (settings.BASE_URL, v.xsd_file.url)
    self.assertEqual(self.example.absolute_latest_xsd_path(), v_abs_path)
    
  def test_absolute_latest_xls_path_for_null(self):
    """When there are no versions the absolute path to the latest version's XLS file is none"""
    self.assertIsNone(self.example.absolute_latest_xls_path())
  
  def test_absolute_latest_xls_path(self):
    """The xls file should be for the latest version"""
    v = self.createTwoVersions()
    v_abs_path = '%s%s' % (settings.BASE_URL, v.xls_file.url)
    self.assertEqual(self.example.absolute_latest_xls_path(), v_abs_path)
    
  def test_latest_xsd_link_for_null(self):
    """When there are no versions the link to the latest version's XSD file is none"""
    self.assertIsNone(self.example.latest_xsd_link())
  
  def test_latest_xsd_link(self):
    """There should be a link element for the latest version's xsd file"""
    v = self.createTwoVersions()
    v_link = '<a href="%s%s">%s</a>' % (settings.BASE_URL, v.xsd_file.url, v.xsd_file.name.split('/')[-1])
    self.assertEqual(self.example.latest_xsd_link(), v_link)
    
  def test_latest_xls_link_for_null(self):
    """When there are no versions the link to the latest version's XSD file is none"""
    self.assertIsNone(self.example.latest_xls_link())
  
  def test_latest_xls_link(self):
    """There should be a link element for the latest version's xls file"""
    v = self.createTwoVersions()
    v_link = '<a href="%s%s">%s</a>' % (settings.BASE_URL, v.xls_file.url, v.xls_file.name.split('/')[-1])
    self.assertEqual(self.example.latest_xls_link(), v_link)
  
  def test_my_html(self):
    """The my_html should return the correct url to the model's html page"""
    url = '%s/contentmodel/%s.html' % (settings.BASE_URL.rstrip('/'), self.example.pk)
    self.assertEqual(self.example.my_html(), url)
    
  def test_my_json(self):
    """The my_json should return the correct url to the model's json page"""
    url = '%s/contentmodel/%s.json' % (settings.BASE_URL.rstrip('/'), self.example.pk)
    self.assertEqual(self.example.my_json(), url)
  
  def test_my_atom(self):
    """The my_atom should return the correct url to the model's atom page"""
    url = '%s/contentmodel/%s.xml' % (settings.BASE_URL.rstrip('/'), self.example.pk)
    self.assertEqual(self.example.my_atom(), url)
    
  def test_stripped_regex(self):
    """The stripped_regex should return the label's path """
    self.assertEqual(self.example.stripped_regex(), self.stripped_regex())
    
  def test_regex_pattern(self):
    """The stripped_regex should generate the regular expression pattern for the label's path"""
    regex = '^%s(\.[a-zA-Z]{3,4}|/)?$' % self.stripped_regex()
    self.assertEqual(self.example.regex_pattern(), regex)

  def test_relative_uri(self):
    """The relative_uri should generate the relative uri for the ContentModel"""
    uri = '/uri-gin/%s/%s' % (settings.URI_REGISTER_LABEL, self.stripped_regex())
    self.assertEqual(self.example.relative_uri(), uri)
    
  def test_absolute_uri(self):
    """The absolute_uri should generate the absolute uri for the ContentModel"""
    uri = '%s/uri-gin/%s/%s' % (settings.BASE_URL.rstrip('/'), settings.URI_REGISTER_LABEL, self.stripped_regex())
    self.assertEqual(self.example.absolute_uri(), uri)
    
  def test_rewrite_rule_link(self):
    """The rewrite_rule_link should return a link to this ContentModel's RewriteRule"""
    url = '<a href="/admin/uriredirect/rewriterule/%s">Edit Rule</a>' % self.example.rewrite_rule.pk
    self.assertEqual(self.example.rewrite_rule_link(), url)


  
  
  
    
    
  