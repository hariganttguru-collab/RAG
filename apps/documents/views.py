from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .models import Project, Document


@login_required
def document_view(request, document_id):
    """View a document"""
    document = get_object_or_404(Document, id=document_id)
    # Check if user has access to the project
    if document.project.user != request.user:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You don't have access to this document.")
    
    return FileResponse(document.file.open(), content_type='application/pdf')

