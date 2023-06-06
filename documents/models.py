from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название документа')
    is_deleted = models.BooleanField(default=False)
    current_version = models.OneToOneField('DocumentVersion', on_delete=models.CASCADE, null=True, blank=True,
                                           related_name='current_version')

    def __str__(self):
        return self.name


class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    content = models.TextField(verbose_name='Содержание документа')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.document} - {self.content[:30]}'
