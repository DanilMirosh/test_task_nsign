from django.contrib import admin
from .models import Document, DocumentVersion
from django.contrib.auth.models import Group

admin.site.register(Document)
admin.site.register(DocumentVersion)

admin.site.unregister(Group)
