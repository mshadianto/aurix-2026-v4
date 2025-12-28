"""
Documents Page Module
Upload, manage, and organize audit documents
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional
import hashlib

from ui.components import (
    render_page_header,
    render_footer,
    render_alert,
    render_badge,
    render_metric_card,
    render_section_title
)
from ui.styles.css_builder import get_current_theme


def render_documents_page():
    """Render the documents management page"""
    t = get_current_theme()
    
    render_page_header(
        "Document Management",
        "Upload, organize, and manage audit documents for RAG processing"
    )
    
    # Initialize documents in session state
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        _render_upload_section(t)
    
    with col2:
        _render_document_library(t)
    
    # Document statistics
    st.markdown("<br>", unsafe_allow_html=True)
    _render_document_stats(t)
    
    render_footer()


def _render_upload_section(t: Dict):
    """Render document upload section"""
    st.markdown(f'''
    <div class="pro-card">
        <h3 style="color:{t['text']} !important; margin-bottom: 1rem;">📤 Upload Documents</h3>
        <p style="color:{t['text_muted']} !important; font-size: 0.9rem;">
            Supported formats: PDF, DOCX, XLSX, TXT, CSV
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Select files to upload",
        type=['pdf', 'docx', 'xlsx', 'csv', 'txt'],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    # Category selection
    category = st.selectbox(
        "Document Category",
        options=[
            "Audit Reports",
            "SOP/Policies",
            "Regulations",
            "Working Papers",
            "Risk Assessment",
            "Financial Data",
            "Compliance Documents",
            "Other"
        ]
    )
    
    # Tags input
    tags = st.text_input(
        "Tags (comma-separated)",
        placeholder="e.g., credit, risk, 2024"
    )
    
    # Upload button
    if st.button("📥 Upload & Process", type="primary", use_container_width=True):
        if uploaded_files:
            _process_uploaded_files(uploaded_files, category, tags, t)
        else:
            st.warning("Please select files to upload")


def _process_uploaded_files(files: List, category: str, tags: str, t: Dict):
    """Process and store uploaded files"""
    success_count = 0
    
    for file in files:
        # Check if file already exists
        existing_names = [d['name'] for d in st.session_state.documents]
        if file.name in existing_names:
            st.warning(f"⚠️ '{file.name}' already exists, skipping...")
            continue
        
        # Read file content
        try:
            if file.type == "text/plain" or file.name.endswith('.txt'):
                content = file.read().decode('utf-8')
            elif file.name.endswith('.csv'):
                content = file.read().decode('utf-8')
            else:
                content = f"[Binary content: {file.name}]"
                file.seek(0)  # Reset for later processing
            
            # Generate content hash
            content_hash = hashlib.md5(file.read()).hexdigest()[:12]
            file.seek(0)  # Reset after hashing
            
            # Parse tags
            tag_list = [t.strip() for t in tags.split(',') if t.strip()]
            
            # Create document entry
            doc_entry = {
                'name': file.name,
                'category': category,
                'content': content if isinstance(content, str) else "",
                'size': file.size,
                'type': file.type or _get_file_type(file.name),
                'hash': content_hash,
                'tags': tag_list,
                'uploaded': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'file': file
            }
            
            st.session_state.documents.append(doc_entry)
            success_count += 1
            
        except Exception as e:
            st.error(f"❌ Error processing '{file.name}': {str(e)}")
    
    if success_count > 0:
        st.success(f"✅ Successfully uploaded {success_count} file(s)")
        st.rerun()


def _get_file_type(filename: str) -> str:
    """Get file type from extension"""
    ext = filename.split('.')[-1].lower()
    type_map = {
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'csv': 'text/csv',
        'txt': 'text/plain'
    }
    return type_map.get(ext, 'application/octet-stream')


def _render_document_library(t: Dict):
    """Render document library section"""
    st.markdown(f'''
    <div class="pro-card">
        <h3 style="color:{t['text']} !important; margin-bottom: 1rem;">📚 Document Library</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    documents = st.session_state.documents
    
    if not documents:
        st.info("📁 No documents uploaded yet. Use the uploader to add documents.")
        return
    
    # Filter options
    categories = list(set(d['category'] for d in documents))
    filter_category = st.selectbox(
        "Filter by Category",
        options=["All"] + categories,
        key="doc_filter"
    )
    
    # Search
    search_query = st.text_input(
        "🔍 Search documents",
        placeholder="Search by name...",
        key="doc_search"
    )
    
    # Filter documents
    filtered_docs = documents
    if filter_category != "All":
        filtered_docs = [d for d in filtered_docs if d['category'] == filter_category]
    if search_query:
        filtered_docs = [d for d in filtered_docs if search_query.lower() in d['name'].lower()]
    
    # Display documents
    st.markdown(f"**{len(filtered_docs)} document(s)**")
    
    for idx, doc in enumerate(filtered_docs):
        _render_document_item(doc, idx, t)


def _render_document_item(doc: Dict, idx: int, t: Dict):
    """Render a single document item"""
    # Get file icon
    icon = _get_file_icon(doc['name'])
    
    # Format file size
    size_str = _format_file_size(doc['size'])
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(f'''
        <div style="padding: 0.5rem 0;">
            <div style="font-weight: 600; color: {t['text']} !important;">
                {icon} {doc['name']}
            </div>
            <div style="font-size: 0.8rem; color: {t['text_muted']} !important;">
                {doc['category']} • {size_str} • {doc['uploaded']}
            </div>
            {_render_tags(doc.get('tags', []), t)}
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        if st.button("👁️ View", key=f"view_{idx}_{doc['hash']}", use_container_width=True):
            _show_document_preview(doc)
    
    with col3:
        if st.button("🗑️", key=f"del_{idx}_{doc['hash']}", use_container_width=True):
            _delete_document(doc, idx)


def _get_file_icon(filename: str) -> str:
    """Get appropriate icon for file type"""
    ext = filename.split('.')[-1].lower()
    icons = {
        'pdf': '📕',
        'docx': '📘',
        'doc': '📘',
        'xlsx': '📗',
        'xls': '📗',
        'csv': '📊',
        'txt': '📄'
    }
    return icons.get(ext, '📄')


def _format_file_size(size: int) -> str:
    """Format file size to human-readable string"""
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    else:
        return f"{size / (1024 * 1024):.2f} MB"


def _render_tags(tags: List[str], t: Dict) -> str:
    """Render document tags"""
    if not tags:
        return ""
    
    tag_html = " ".join([
        f'<span style="background:{t["primary"]}20; color:{t["primary"]}; '
        f'padding:2px 8px; border-radius:12px; font-size:0.7rem; margin-right:4px;">'
        f'{tag}</span>'
        for tag in tags[:5]
    ])
    return f'<div style="margin-top:0.25rem;">{tag_html}</div>'


def _show_document_preview(doc: Dict):
    """Show document preview in modal"""
    st.markdown("### 📄 Document Preview")
    st.markdown(f"**{doc['name']}**")
    st.markdown(f"Category: {doc['category']}")
    st.markdown(f"Uploaded: {doc['uploaded']}")
    
    if doc.get('content') and isinstance(doc['content'], str) and len(doc['content']) > 0:
        if doc['content'].startswith('[Binary'):
            st.info("Binary file - preview not available")
        else:
            with st.expander("Content Preview", expanded=True):
                st.text(doc['content'][:2000] + ('...' if len(doc['content']) > 2000 else ''))
    else:
        st.info("Content preview not available")


def _delete_document(doc: Dict, idx: int):
    """Delete a document from the library"""
    # Find and remove the document
    for i, d in enumerate(st.session_state.documents):
        if d['hash'] == doc['hash'] and d['name'] == doc['name']:
            st.session_state.documents.pop(i)
            st.success(f"✓ Deleted '{doc['name']}'")
            st.rerun()
            break


def _render_document_stats(t: Dict):
    """Render document statistics section"""
    documents = st.session_state.documents
    
    if not documents:
        return
    
    st.markdown(render_section_title("📊 Document Statistics"), unsafe_allow_html=True)
    
    # Calculate stats
    total_docs = len(documents)
    total_size = sum(d['size'] for d in documents)
    categories = {}
    for d in documents:
        cat = d['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(render_metric_card(
            "Total Documents",
            str(total_docs),
            icon="📁"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(render_metric_card(
            "Total Size",
            _format_file_size(total_size),
            icon="💾"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(render_metric_card(
            "Categories",
            str(len(categories)),
            icon="📂"
        ), unsafe_allow_html=True)
    
    with col4:
        indexed = len([d for d in documents if d.get('content')])
        st.markdown(render_metric_card(
            "Indexed",
            str(indexed),
            icon="🔍"
        ), unsafe_allow_html=True)
    
    # Category breakdown
    if categories:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Documents by Category")
        
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_docs) * 100
            st.markdown(f'''
            <div style="display:flex; align-items:center; margin-bottom:0.5rem;">
                <span style="width:150px; color:{t['text']} !important;">{cat}</span>
                <div style="flex:1; height:8px; background:{t['border']}; border-radius:4px; margin:0 1rem;">
                    <div style="width:{pct}%; height:100%; background:{t['primary']}; border-radius:4px;"></div>
                </div>
                <span style="color:{t['text_muted']} !important; width:60px;">{count} ({pct:.0f}%)</span>
            </div>
            ''', unsafe_allow_html=True)


# Export
def render():
    """Render function called by router."""
    render_documents_page()

__all__ = ['render_documents_page', 'render']
