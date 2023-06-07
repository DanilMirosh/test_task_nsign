from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Document, DocumentVersion


class CreateDocumentView(View):
    template_name = 'documents/create_document.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        content = request.POST.get('content')

        if not name or Document.objects.filter(name=name).exists():
            error = f'Error - Document named {name} already exists'
            return render(request, self.template_name, {'error': error})

        document = Document.objects.create(name=name)
        current_version = DocumentVersion.objects.create(document=document, content=content)
        document.current_version = current_version
        document.save()

        return redirect('documents:view_document', document_id=document.id)


class EditDocumentView(View):
    template_name = 'documents/edit_document.html'

    def get(self, request, document_id):
        document = get_object_or_404(Document, id=document_id)
        current_version = document.current_version
        context = {'document': document, 'current_version': current_version}
        return render(request, self.template_name, context)

    def post(self, request, document_id):
        document = get_object_or_404(Document, id=document_id)
        current_version = document.current_version

        name = request.POST.get('name')
        content = request.POST.get('content')

        if not name or Document.objects.filter(name=name).exclude(id=document_id).exists():
            error = f'Error - Document named {name} already exists'
            context = {'document': document, 'current_version': current_version, 'error': error}
            return render(request, self.template_name, context)

        document.name = name
        document.save()

        if current_version is None or current_version.content != content:
            current_version = DocumentVersion.objects.create(document=document, content=content)
            document.current_version = current_version
            document.save()

        return redirect('documents:view_document', document_id=document.id)


class ViewDocumentView(View):
    template_name = 'documents/view_document.html'

    def get(self, request, document_id):
        document = get_object_or_404(Document, id=document_id)
        context = {'document': document}
        return render(request, self.template_name, context)


class DeleteDocumentView(View):
    template_name = 'documents/delete_document.html'

    def get(self, request, document_id):
        document = get_object_or_404(Document, id=document_id)
        context = {'document': document}
        return render(request, self.template_name, context)

    def post(self, request, document_id):
        document = get_object_or_404(Document, id=document_id)
        document.is_deleted = True
        document.save()
        return redirect('documents:document_list')


class CompareVersionsView(View):
    template_name = 'documents/compare_versions.html'

    def get(self, request, document_id):
        document = get_object_or_404(Document, id=document_id)
        doc_versions = DocumentVersion.objects.filter(document=document)
        current_version = document.current_version

        if len(doc_versions) > 1:
            previous_version = doc_versions.exclude(id=current_version.id).latest('created_at')
            context = {
                'current_version': current_version.created_at,
                'previous_version': previous_version.created_at,
                'current_content': current_version.content,
                'previous_content': previous_version.content,
                'document_id': document.id,
            }
        else:
            context = {
                'current_version': current_version.created_at,
                'previous_version': None,
                'document_id': document.id}

        context['document_id'] = document_id

        return render(request, self.template_name, context)


class DocumentListView(View):
    template_name = 'documents/index.html'

    def get(self, request):
        documents = Document.objects.filter(is_deleted=False)
        context = {'documents': documents}
        return render(request, self.template_name, context)
