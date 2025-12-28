"""
RAG Infrastructure Layer
Document processing, embedding, and retrieval for audit intelligence
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import hashlib
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class DocumentChunk:
    """Represents a chunk of processed document"""
    id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    
    @property
    def word_count(self) -> int:
        return len(self.content.split())


@dataclass
class RetrievalResult:
    """Result from RAG retrieval"""
    chunk: DocumentChunk
    score: float
    source_document: str
    
    def __repr__(self) -> str:
        return f"RetrievalResult(source={self.source_document}, score={self.score:.3f})"


@dataclass
class ProcessedDocument:
    """Represents a fully processed document"""
    id: str
    filename: str
    chunks: List[DocumentChunk]
    metadata: Dict[str, Any]
    processed_at: datetime = field(default_factory=datetime.now)
    
    @property
    def chunk_count(self) -> int:
        return len(self.chunks)
    
    @property
    def total_words(self) -> int:
        return sum(chunk.word_count for chunk in self.chunks)


class DocumentProcessor:
    """
    Process documents for RAG indexing
    Handles chunking, metadata extraction, and classification
    """
    
    # Indonesian regulatory keywords for classification
    CATEGORY_KEYWORDS = {
        "risk_management": ["risiko", "risk", "rcsa", "kri", "risk appetite", "manajemen risiko"],
        "governance": ["tata kelola", "governance", "dewan", "komisaris", "direksi", "gcg"],
        "compliance": ["kepatuhan", "compliance", "regulasi", "pojk", "pbi", "seojk"],
        "credit": ["kredit", "credit", "pinjaman", "pembiayaan", "npl", "kolektibilitas"],
        "operational": ["operasional", "operational", "proses", "prosedur", "sop"],
        "it_audit": ["sistem informasi", "it control", "cybersecurity", "akses", "teknologi"],
        "aml": ["apu", "ppt", "money laundering", "cdd", "kyc", "str", "ppatk"],
        "financial": ["keuangan", "financial", "laporan", "akuntansi", "neraca"]
    }
    
    # Regulation patterns
    REGULATION_PATTERNS = [
        r'POJK\s*(?:No\.?)?\s*\d+[\/\-](?:POJK\.\d+[\/\-])?\d+',
        r'SEOJK\s*(?:No\.?)?\s*\d+[\/\-]\d+',
        r'PBI\s*(?:No\.?)?\s*\d+[\/\-]\d+',
        r'PP\s*(?:No\.?)?\s*\d+[\/\-]\d+',
        r'UU\s*(?:No\.?)?\s*\d+[\/\-]\d+',
        r'ISO\s*\d+[:\-]\d+',
        r'PSAK\s*\d+'
    ]
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process(self, content: str, filename: str, metadata: Dict = None) -> ProcessedDocument:
        """Process document content into chunks with metadata"""
        doc_id = self._generate_doc_id(content, filename)
        
        # Extract document-level metadata
        doc_metadata = self._extract_metadata(content, filename)
        if metadata:
            doc_metadata.update(metadata)
        
        # Create chunks
        chunks = self._create_chunks(content, doc_metadata, filename)
        
        return ProcessedDocument(
            id=doc_id,
            filename=filename,
            chunks=chunks,
            metadata=doc_metadata
        )
    
    def _create_chunks(
        self, 
        content: str, 
        doc_metadata: Dict, 
        filename: str
    ) -> List[DocumentChunk]:
        """Split content into overlapping chunks"""
        chunks = []
        sentences = self._split_into_sentences(content)
        
        current_chunk = ""
        current_sentences = []
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += sentence + " "
                current_sentences.append(sentence)
            else:
                if current_chunk.strip():
                    chunks.append(self._create_chunk(
                        current_chunk.strip(), 
                        doc_metadata, 
                        filename,
                        len(chunks)
                    ))
                
                # Start new chunk with overlap
                overlap_count = min(2, len(current_sentences))
                overlap_text = " ".join(current_sentences[-overlap_count:]) if current_sentences else ""
                current_chunk = overlap_text + " " + sentence + " "
                current_sentences = [sentence]
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append(self._create_chunk(
                current_chunk.strip(), 
                doc_metadata, 
                filename,
                len(chunks)
            ))
        
        return chunks
    
    def _create_chunk(
        self, 
        content: str, 
        doc_metadata: Dict, 
        filename: str,
        index: int
    ) -> DocumentChunk:
        """Create a single document chunk"""
        chunk_id = self._generate_chunk_id(content)
        
        chunk_metadata = {
            **doc_metadata,
            "filename": filename,
            "chunk_index": index,
            "chunk_keywords": self._extract_chunk_keywords(content)
        }
        
        return DocumentChunk(
            id=chunk_id,
            content=content,
            metadata=chunk_metadata
        )
    
    def _extract_metadata(self, content: str, filename: str) -> Dict[str, Any]:
        """Extract metadata from document content"""
        return {
            "filename": filename,
            "processed_at": datetime.now().isoformat(),
            "word_count": len(content.split()),
            "char_count": len(content),
            "language": self._detect_language(content),
            "categories": self._classify_document(content),
            "regulations_mentioned": self._extract_regulations(content),
            "risk_indicators": self._extract_risk_indicators(content)
        }
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences, handling Indonesian patterns"""
        # Handle bullet points and numbered lists
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Split on sentence endings
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _detect_language(self, text: str) -> str:
        """Detect if text is Indonesian or English"""
        indonesian_words = ["yang", "dan", "untuk", "dengan", "dari", "pada", "dalam", "adalah", "ini", "itu"]
        text_lower = text.lower()
        indonesian_count = sum(1 for word in indonesian_words if f" {word} " in f" {text_lower} ")
        return "id" if indonesian_count >= 3 else "en"
    
    def _classify_document(self, text: str) -> List[str]:
        """Classify document into audit categories"""
        categories = []
        text_lower = text.lower()
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                categories.append(category)
        
        return categories if categories else ["general"]
    
    def _extract_regulations(self, text: str) -> List[str]:
        """Extract mentioned regulations"""
        regulations = []
        for pattern in self.REGULATION_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            regulations.extend(matches)
        return list(set(regulations))
    
    def _extract_risk_indicators(self, text: str) -> Dict[str, List[str]]:
        """Extract risk-related keywords"""
        risk_keywords = {
            "high_risk": ["fraud", "penipuan", "kecurangan", "pelanggaran", "material", "critical"],
            "control_weakness": ["kelemahan", "weakness", "gap", "deficiency", "kurang", "tidak memadai"],
            "finding": ["temuan", "finding", "observasi", "catatan", "rekomendasi", "issue"]
        }
        
        found = {}
        text_lower = text.lower()
        
        for category, keywords in risk_keywords.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                found[category] = matches
        
        return found
    
    def _extract_chunk_keywords(self, content: str) -> List[str]:
        """Extract key terms from chunk content"""
        # Simple keyword extraction based on capitalized words and domain terms
        words = content.split()
        keywords = []
        
        for word in words:
            # Clean word
            clean_word = re.sub(r'[^\w]', '', word)
            if len(clean_word) < 3:
                continue
            
            # Check if it's likely a keyword (capitalized or domain term)
            if clean_word[0].isupper() or clean_word.lower() in self._get_domain_terms():
                keywords.append(clean_word)
        
        return list(set(keywords))[:20]  # Limit to 20 keywords
    
    def _get_domain_terms(self) -> set:
        """Get set of audit domain terms"""
        terms = set()
        for keywords in self.CATEGORY_KEYWORDS.values():
            terms.update(kw.lower() for kw in keywords)
        return terms
    
    def _generate_doc_id(self, content: str, filename: str) -> str:
        """Generate unique document ID"""
        hash_input = f"{filename}:{content[:1000]}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:16]
    
    def _generate_chunk_id(self, content: str) -> str:
        """Generate unique chunk ID"""
        return hashlib.md5(content.encode()).hexdigest()[:12]


class VectorStore(ABC):
    """Abstract base class for vector stores"""
    
    @abstractmethod
    def add(self, chunks: List[DocumentChunk], embeddings: List[List[float]] = None):
        """Add chunks to the store"""
        pass
    
    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[RetrievalResult]:
        """Search for similar chunks"""
        pass
    
    @abstractmethod
    def delete(self, chunk_ids: List[str]):
        """Delete chunks from store"""
        pass
    
    @abstractmethod
    def clear(self):
        """Clear all chunks from store"""
        pass


class InMemoryVectorStore(VectorStore):
    """
    Simple in-memory vector store
    Suitable for development and small document collections
    """
    
    def __init__(self):
        self.chunks: Dict[str, DocumentChunk] = {}
        self.embeddings: Dict[str, List[float]] = {}
    
    def add(self, chunks: List[DocumentChunk], embeddings: List[List[float]] = None):
        """Add chunks with optional embeddings"""
        for i, chunk in enumerate(chunks):
            self.chunks[chunk.id] = chunk
            if embeddings and i < len(embeddings):
                self.embeddings[chunk.id] = embeddings[i]
    
    def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 5
    ) -> List[RetrievalResult]:
        """Search using cosine similarity"""
        if not self.embeddings:
            return []
        
        results = []
        for chunk_id, embedding in self.embeddings.items():
            score = self._cosine_similarity(query_embedding, embedding)
            chunk = self.chunks.get(chunk_id)
            if chunk:
                results.append(RetrievalResult(
                    chunk=chunk,
                    score=score,
                    source_document=chunk.metadata.get("filename", "unknown")
                ))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def keyword_search(self, query: str, top_k: int = 5) -> List[RetrievalResult]:
        """Fallback keyword search"""
        query_terms = query.lower().split()
        results = []
        
        for chunk_id, chunk in self.chunks.items():
            content_lower = chunk.content.lower()
            score = sum(1 for term in query_terms if term in content_lower)
            
            if score > 0:
                results.append(RetrievalResult(
                    chunk=chunk,
                    score=score / len(query_terms),
                    source_document=chunk.metadata.get("filename", "unknown")
                ))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def hybrid_search(
        self, 
        query_text: str, 
        query_embedding: List[float],
        top_k: int = 5,
        alpha: float = 0.5
    ) -> List[RetrievalResult]:
        """Combine semantic and keyword search"""
        keyword_results = self.keyword_search(query_text, top_k * 2)
        semantic_results = self.search(query_embedding, top_k * 2) if self.embeddings else []
        
        # Combine scores
        combined_scores: Dict[str, Dict] = {}
        
        for result in keyword_results:
            combined_scores[result.chunk.id] = {
                "chunk": result.chunk,
                "score": (1 - alpha) * result.score,
                "source": result.source_document
            }
        
        for result in semantic_results:
            if result.chunk.id in combined_scores:
                combined_scores[result.chunk.id]["score"] += alpha * result.score
            else:
                combined_scores[result.chunk.id] = {
                    "chunk": result.chunk,
                    "score": alpha * result.score,
                    "source": result.source_document
                }
        
        results = [
            RetrievalResult(
                chunk=data["chunk"],
                score=data["score"],
                source_document=data["source"]
            )
            for data in combined_scores.values()
        ]
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def delete(self, chunk_ids: List[str]):
        """Delete chunks by ID"""
        for chunk_id in chunk_ids:
            self.chunks.pop(chunk_id, None)
            self.embeddings.pop(chunk_id, None)
    
    def clear(self):
        """Clear all data"""
        self.chunks.clear()
        self.embeddings.clear()
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    @property
    def size(self) -> int:
        """Number of chunks in store"""
        return len(self.chunks)


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers"""
    
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts"""
        pass
    
    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a single query"""
        pass


class SentenceTransformerEmbedding(EmbeddingProvider):
    """Embedding provider using sentence-transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
    
    def _get_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                logger.warning("sentence-transformers not installed")
                return None
        return self._model
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        model = self._get_model()
        if model is None:
            return []
        return model.encode(texts).tolist()
    
    def embed_query(self, query: str) -> List[float]:
        model = self._get_model()
        if model is None:
            return []
        return model.encode(query).tolist()


class RAGEngine:
    """
    Main RAG Engine for AURIX
    Combines document processing, embedding, and retrieval
    """
    
    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.processor = DocumentProcessor(chunk_size, chunk_overlap)
        self.vector_store = InMemoryVectorStore()
        self.embedding_provider: Optional[EmbeddingProvider] = None
        
        try:
            self.embedding_provider = SentenceTransformerEmbedding(embedding_model)
        except Exception as e:
            logger.warning(f"Could not initialize embedding provider: {e}")
    
    def index_document(
        self, 
        content: str, 
        filename: str, 
        metadata: Dict = None
    ) -> ProcessedDocument:
        """Index a document for retrieval"""
        # Process document
        doc = self.processor.process(content, filename, metadata)
        
        # Generate embeddings if available
        embeddings = None
        if self.embedding_provider:
            texts = [chunk.content for chunk in doc.chunks]
            embeddings = self.embedding_provider.embed(texts)
        
        # Add to vector store
        self.vector_store.add(doc.chunks, embeddings)
        
        logger.info(f"Indexed document '{filename}' with {doc.chunk_count} chunks")
        return doc
    
    def query(
        self, 
        query: str, 
        top_k: int = 5, 
        use_hybrid: bool = True
    ) -> List[RetrievalResult]:
        """Query the RAG engine"""
        if self.embedding_provider:
            query_embedding = self.embedding_provider.embed_query(query)
            
            if use_hybrid:
                return self.vector_store.hybrid_search(query, query_embedding, top_k)
            else:
                return self.vector_store.search(query_embedding, top_k)
        else:
            return self.vector_store.keyword_search(query, top_k)
    
    def generate_context(self, query: str, top_k: int = 5) -> str:
        """Generate context string from retrieved documents"""
        results = self.query(query, top_k)
        
        if not results:
            return "No relevant documents found."
        
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Source {i}: {result.source_document}]\n"
                f"{result.chunk.content}\n"
                f"[Relevance: {result.score:.2f}]"
            )
        
        return "\n\n---\n\n".join(context_parts)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about indexed documents"""
        categories: Dict[str, int] = {}
        
        for chunk in self.vector_store.chunks.values():
            for cat in chunk.metadata.get("categories", ["unknown"]):
                categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_chunks": self.vector_store.size,
            "has_embeddings": len(self.vector_store.embeddings) > 0,
            "categories": categories
        }
    
    def clear(self):
        """Clear all indexed documents"""
        self.vector_store.clear()


class AuditRAGHelper:
    """
    Audit-specific RAG operations
    Provides specialized retrieval for audit use cases
    """
    
    def __init__(self, rag_engine: RAGEngine):
        self.rag = rag_engine
    
    def find_risk_indicators(self, audit_area: str, top_k: int = 10) -> List[Dict]:
        """Find risk indicators for specific audit area"""
        query = f"risk indicators problems issues findings {audit_area}"
        results = self.rag.query(query, top_k)
        
        indicators = []
        for result in results:
            risk_indicators = result.chunk.metadata.get("risk_indicators", {})
            if risk_indicators:
                indicators.append({
                    "source": result.source_document,
                    "content": result.chunk.content[:300],
                    "score": result.score,
                    "risk_level": "high" if risk_indicators.get("high_risk") else "medium",
                    "indicators": risk_indicators
                })
        
        return indicators
    
    def find_regulatory_references(self, regulation: str, top_k: int = 10) -> List[Dict]:
        """Find document sections referencing specific regulation"""
        results = self.rag.query(regulation, top_k)
        
        references = []
        for result in results:
            if regulation.upper() in result.chunk.content.upper():
                references.append({
                    "source": result.source_document,
                    "content": result.chunk.content,
                    "score": result.score,
                    "regulations": result.chunk.metadata.get("regulations_mentioned", [])
                })
        
        return references
    
    def find_control_descriptions(self, process_name: str, top_k: int = 10) -> List[Dict]:
        """Find control descriptions for specific process"""
        query = f"control procedure {process_name} verification approval authorization"
        results = self.rag.query(query, top_k)
        
        controls = []
        control_keywords = ["control", "kontrol", "prosedur", "procedure", "verifikasi", "approval"]
        
        for result in results:
            content_lower = result.chunk.content.lower()
            if any(kw in content_lower for kw in control_keywords):
                controls.append({
                    "source": result.source_document,
                    "description": result.chunk.content,
                    "score": result.score
                })
        
        return controls
    
    def generate_audit_context(
        self, 
        audit_area: str, 
        focus_areas: List[str] = None
    ) -> str:
        """Generate comprehensive audit context for LLM"""
        context_parts = []
        
        # General context
        general_results = self.rag.query(audit_area, top_k=3)
        if general_results:
            context_parts.append("## Background Information")
            for r in general_results:
                context_parts.append(f"From {r.source_document}:\n{r.chunk.content}")
        
        # Risk context
        risk_results = self.rag.query(f"{audit_area} risk issues problems", top_k=3)
        if risk_results:
            context_parts.append("\n## Risk Indicators")
            for r in risk_results:
                context_parts.append(f"From {r.source_document}:\n{r.chunk.content}")
        
        # Control context
        control_results = self.rag.query(f"{audit_area} control procedure", top_k=3)
        if control_results:
            context_parts.append("\n## Existing Controls")
            for r in control_results:
                context_parts.append(f"From {r.source_document}:\n{r.chunk.content}")
        
        # Focus area context
        if focus_areas:
            for focus in focus_areas:
                focus_results = self.rag.query(f"{audit_area} {focus}", top_k=2)
                if focus_results:
                    context_parts.append(f"\n## Focus: {focus}")
                    for r in focus_results:
                        context_parts.append(f"From {r.source_document}:\n{r.chunk.content}")
        
        return "\n\n".join(context_parts)


__all__ = [
    'DocumentChunk',
    'RetrievalResult',
    'ProcessedDocument',
    'DocumentProcessor',
    'VectorStore',
    'InMemoryVectorStore',
    'EmbeddingProvider',
    'SentenceTransformerEmbedding',
    'RAGEngine',
    'AuditRAGHelper'
]
