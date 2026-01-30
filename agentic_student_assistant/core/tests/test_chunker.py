"""
Comprehensive tests for core.utils.chunker module.
100% coverage target - no mocks.
"""
import pytest
from agentic_student_assistant.core.utils.chunker import chunk_text


class TestChunkerComprehensive:
    """Comprehensive tests for text chunker - 100% coverage."""
    
    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        text = "word " * 100
        chunks = chunk_text(text, source="test.txt", chunk_size=50, chunk_overlap=10)
        
        assert isinstance(chunks, list)
        assert len(chunks) > 0
        assert all('content' in chunk for chunk in chunks)
        assert all('metadata' in chunk for chunk in chunks)
    
    def test_chunk_text_with_source(self):
        """Test that source is included in metadata."""
        text = "test content"
        chunks = chunk_text(text, source="document.pdf")
        
        assert all(chunk['metadata']['source'] == "document.pdf" for chunk in chunks)
    
    def test_chunk_text_chunk_indices(self):
        """Test that chunk indices are sequential."""
        text = "word " * 200
        chunks = chunk_text(text, source="test.txt", chunk_size=50)
        
        for idx, chunk in enumerate(chunks):
            assert chunk['metadata']['chunk_index'] == idx
    
    def test_chunk_text_small_text(self):
        """Test chunking small text."""
        text = "small text"
        chunks = chunk_text(text, source="small.txt", chunk_size=100)
        
        assert len(chunks) == 1
        assert chunks[0]['content'] == text
    
    def test_chunk_text_empty(self):
        """Test chunking empty text."""
        chunks = chunk_text("", source="empty.txt")
        
        assert isinstance(chunks, list)
    
    def test_chunk_text_exact_chunk_size(self):
        """Test text exactly matching chunk size."""
        text = "a" * 50
        chunks = chunk_text(text, source="test.txt", chunk_size=50, chunk_overlap=0)
        
        assert len(chunks) >= 1
    
    def test_chunk_text_no_overlap(self):
        """Test chunking with no overlap."""
        text = "word " * 100
        chunks = chunk_text(text, source="test.txt", chunk_size=50, chunk_overlap=0)
        
        assert isinstance(chunks, list)
        assert all('content' in chunk for chunk in chunks)
    
    def test_chunk_text_large_overlap(self):
        """Test chunking with large overlap."""
        text = "word " * 100
        chunks = chunk_text(text, source="test.txt", chunk_size=100, chunk_overlap=80)
        
        assert isinstance(chunks, list)
    
    def test_chunk_text_different_sizes(self):
        """Test chunking with various chunk sizes."""
        text = "word " * 200
        
        for size in [10, 50, 100, 200]:
            chunks = chunk_text(text, source="test.txt", chunk_size=size)
            assert isinstance(chunks, list)
    
    def test_chunk_text_multiline(self):
        """Test chunking multiline text."""
        text = "line1\nline2\nline3\nline4\nline5"
        chunks = chunk_text(text, source="multiline.txt", chunk_size=20)
        
        assert isinstance(chunks, list)
    
    def test_chunk_text_special_characters(self):
        """Test chunking text with special characters."""
        text = "Special !@#$%^&*() characters " * 20
        chunks = chunk_text(text, source="special.txt")
        
        assert isinstance(chunks, list)
    
    def test_chunk_text_unicode(self):
        """Test chunking unicode text."""
        text = "Hello 世界 🌍 " * 50
        chunks = chunk_text(text, source="unicode.txt")
        
        assert isinstance(chunks, list)
    
    def test_chunk_text_very_long(self):
        """Test chunking very long text."""
        text = "word " * 10000
        chunks = chunk_text(text, source="long.txt", chunk_size=500)
        
        assert len(chunks) > 1
    
    def test_chunk_text_metadata_structure(self):
        """Test metadata structure is correct."""
        text = "test content"
        chunks = chunk_text(text, source="test.txt")
        
        for chunk in chunks:
            assert 'source' in chunk['metadata']
            assert 'chunk_index' in chunk['metadata']
            assert isinstance(chunk['metadata']['chunk_index'], int)
