from django.contrib import admin
from models import ContentModel, ModelVersion

class ContentModelAdmin(admin.ModelAdmin):
  list_display = ['__unicode__', 'latest_xsd_file', 'latest_xls_file']
  search_fields = ['title']
  
class ModelVersionAdmin(admin.ModelAdmin):
  list_display = ['__unicode__', 'xsd_link', 'xls_link']
  list_filter = ['content_model']
  ordering = ['content_model__title', 'version']
  search_fields = ['content_model__title']

admin.site.register(ContentModel, ContentModelAdmin)
admin.site.register(ModelVersion, ModelVersionAdmin)