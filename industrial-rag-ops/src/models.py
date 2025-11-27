"""Data models for the Industrial RAG application."""
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

class DocumentType(str, Enum):
    """Types of documents in the system."""
    INSPECTION_REPORT = "inspection_report"
    MAINTENANCE_REPORT = "maintenance_report"
    SAFETY_REPORT = "safety_report"
    OPERATIONAL_LOG = "operational_log"
    OTHER = "other"

class DocumentStatus(str, Enum):
    """Status of a document in the processing pipeline."""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"

class DocumentMetadata(BaseModel):
    """Metadata for a document."""
    title: str = Field(..., description="Title of the document")
    document_type: DocumentType = Field(..., description="Type of the document")
    source: str = Field(..., description="Source of the document")
    author: Optional[str] = Field(None, description="Author of the document")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    custom_metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class DocumentChunk(BaseModel):
    """A chunk of a document for vector storage."""
    id: str = Field(..., description="Unique identifier for the chunk")
    document_id: str = Field(..., description="ID of the parent document")
    content: str = Field(..., description="Text content of the chunk")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Chunk metadata")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding of the chunk")
    chunk_index: int = Field(..., description="Index of the chunk in the document")

class Document(BaseModel):
    """A document in the system."""
    id: str = Field(..., description="Unique identifier for the document")
    content: str = Field(..., description="Text content of the document")
    metadata: DocumentMetadata = Field(..., description="Document metadata")
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADED, description="Processing status")
    chunks: List[DocumentChunk] = Field(default_factory=list, description="Document chunks")
    processing_errors: List[str] = Field(default_factory=list, description="Processing errors if any")

class DocumentCreate(BaseModel):
    """Schema for creating a new document."""
    content: str = Field(..., description="Text content of the document")
    metadata: DocumentMetadata = Field(..., description="Document metadata")

class DocumentUpdate(BaseModel):
    """Schema for updating a document."""
    content: Optional[str] = Field(None, description="Updated text content")
    metadata: Optional[DocumentMetadata] = Field(None, description="Updated metadata")

class DocumentResponse(BaseModel):
    """Response schema for a document."""
    id: str
    content: str
    metadata: DocumentMetadata
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime

class SearchQuery(BaseModel):
    """Schema for a search query."""
    query: str = Field(..., description="Search query text")
    limit: int = Field(10, ge=1, le=100, description="Maximum number of results to return")
    min_score: float = Field(0.5, ge=0.0, le=1.0, description="Minimum similarity score")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filters to apply to the search")

class SearchResult(BaseModel):
    """Schema for a search result."""
    id: str
    document_id: str
    content: str
    metadata: Dict[str, Any]
    score: float
    chunk_index: int

class SearchResponse(BaseModel):
    """Response schema for a search."""
    results: List[SearchResult]
    total: int
    query: str

class UserBase(BaseModel):
    """Base user model."""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    full_name: Optional[str] = Field(None, max_length=100)
    disabled: bool = False

class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=8)

class UserInDB(UserBase):
    """User model for database storage."""
    id: str
    hashed_password: str
    scopes: List[str] = []

class UserResponse(UserBase):
    """Response schema for a user."""
    id: str
    scopes: List[str]

class Token(BaseModel):
    """Authentication token response."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Data stored in a JWT token."""
    username: Optional[str] = None
    scopes: List[str] = []

class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime
