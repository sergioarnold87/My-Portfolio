"""
API endpoints for the Industrial RAG application.
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
import json
import uuid
from datetime import datetime, timedelta

from .models import (
    Document, DocumentCreate, DocumentResponse, DocumentUpdate,
    SearchQuery, SearchResponse, UserCreate, UserResponse, Token,
    HealthCheck, DocumentType, DocumentStatus
)
from .security import get_current_active_user, is_admin, is_operator, is_viewer
from .vector_store import vector_store
from .processing import document_processor
from .config import settings, logger

router = APIRouter()

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.utcnow()
    }

@router.post("/documents/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    document: DocumentCreate,
    current_user: dict = Depends(is_operator)
):
    """Create a new document."""
    try:
        # Create a new document
        doc = Document(
            id=str(uuid.uuid4()),
            content=document.content,
            metadata=document.metadata,
            status=DocumentStatus.UPLOADED,
            chunks=[]
        )
        
        # Process the document
        doc = document_processor.process_document(doc)
        
        # Add to vector store if processing was successful
        if doc.status == DocumentStatus.PROCESSED:
            vector_store.add_document(doc)
        
        return DocumentResponse(
            id=doc.id,
            content=doc.content,
            metadata=doc.metadata,
            status=doc.status,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Error creating document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating document: {str(e)}"
        )

@router.post("/documents/upload/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    metadata: str = Form(...),
    current_user: dict = Depends(is_operator)
):
    """Upload and process a document file."""
    try:
        # Parse metadata
        try:
            metadata_dict = json.loads(metadata)
            doc_metadata = DocumentMetadata(**metadata_dict)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid metadata format: {str(e)}"
            )
        
        # Read file content
        content = await file.read()
        try:
            content = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a text file with UTF-8 encoding"
            )
        
        # Create and process document
        doc = Document(
            id=str(uuid.uuid4()),
            content=content,
            metadata=doc_metadata,
            status=DocumentStatus.UPLOADED,
            chunks=[]
        )
        
        doc = document_processor.process_document(doc)
        
        # Add to vector store if processing was successful
        if doc.status == DocumentStatus.PROCESSED:
            vector_store.add_document(doc)
        
        return DocumentResponse(
            id=doc.id,
            content=doc.content,
            metadata=doc.metadata,
            status=doc.status,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading document: {str(e)}"
        )

@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: dict = Depends(is_viewer)
):
    """Get a document by ID."""
    # In a real implementation, you would fetch this from your database
    # For now, we'll return a 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Document {document_id} not found"
    )

@router.get("/documents/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 10,
    document_type: Optional[DocumentType] = None,
    current_user: dict = Depends(is_viewer)
):
    """List all documents with optional filtering."""
    # In a real implementation, you would query your database with pagination
    # For now, return an empty list
    return []

@router.post("/search/", response_model=SearchResponse)
async def search_documents(
    query: SearchQuery,
    current_user: dict = Depends(is_viewer)
):
    """Search for documents."""
    try:
        return vector_store.search(query)
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search error: {str(e)}"
        )

@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    current_user: dict = Depends(is_admin)
):
    """Delete a document."""
    success = vector_store.delete_document(document_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found or could not be deleted"
        )
    return None

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 token endpoint."""
    # In a real implementation, you would validate the username and password
    # against your user database
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Helper functions for authentication (to be implemented properly in a real app)
def authenticate_user(username: str, password: str):
    # This is a placeholder - in a real app, you would check against a database
    if username == "admin" and password == "admin":
        return {
            "username": "admin",
            "scopes": ["admin", "operator", "viewer"],
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # 'secret'
        }
    return None
