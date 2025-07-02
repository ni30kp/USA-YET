import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class DocumentManager:
    def __init__(self, docs_path: str = "data", metadata_file: str = "document_metadata.json"):
        self.docs_path = Path(docs_path)
        self.metadata_file = Path(docs_path) / metadata_file
        self.docs_path.mkdir(exist_ok=True)
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Load document metadata from JSON file"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_metadata(self):
        """Save document metadata to JSON file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2, default=str)
    
    def _calculate_file_hash(self, file_content: bytes) -> str:
        """Calculate SHA-256 hash of file content"""
        return hashlib.sha256(file_content).hexdigest()
    
    def _get_file_info(self, filename: str) -> Dict:
        """Get file information including size and modification time"""
        file_path = self.docs_path / filename
        if file_path.exists():
            stat = file_path.stat()
            return {
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'exists': True
            }
        return {'exists': False}
    
    def check_duplicate(self, filename: str, file_content: bytes) -> Optional[Dict]:
        """Check if file is a duplicate based on content hash"""
        file_hash = self._calculate_file_hash(file_content)
        
        # Check if hash exists in metadata
        for existing_file, metadata in self.metadata.items():
            if metadata.get('hash') == file_hash:
                return {
                    'is_duplicate': True,
                    'existing_file': existing_file,
                    'upload_date': metadata.get('upload_date'),
                    'file_size': metadata.get('file_size')
                }
        
        # Check if same filename exists
        if filename in self.metadata:
            existing_hash = self.metadata[filename].get('hash')
            if existing_hash == file_hash:
                return {
                    'is_duplicate': True,
                    'existing_file': filename,
                    'upload_date': self.metadata[filename].get('upload_date'),
                    'file_size': self.metadata[filename].get('file_size'),
                    'same_name': True
                }
        
        return {'is_duplicate': False}
    
    def add_document(self, filename: str, file_content: bytes, force_overwrite: bool = False) -> Dict:
        """Add a new document to the system"""
        # Check for duplicates
        duplicate_check = self.check_duplicate(filename, file_content)
        
        if duplicate_check['is_duplicate'] and not force_overwrite:
            return {
                'success': False,
                'message': 'Duplicate file detected',
                'duplicate_info': duplicate_check
            }
        
        # Save file
        file_path = self.docs_path / filename
        try:
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Update metadata
            file_hash = self._calculate_file_hash(file_content)
            self.metadata[filename] = {
                'hash': file_hash,
                'upload_date': datetime.now().isoformat(),
                'file_size': len(file_content),
                'file_path': str(file_path),
                'status': 'active'
            }
            
            self._save_metadata()
            
            return {
                'success': True,
                'message': f'Document "{filename}" uploaded successfully',
                'file_info': self.metadata[filename]
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error saving file: {str(e)}'
            }
    
    def remove_document(self, filename: str) -> Dict:
        """Remove a document from the system"""
        file_path = self.docs_path / filename
        
        try:
            # Remove physical file
            if file_path.exists():
                file_path.unlink()
            
            # Remove from metadata
            if filename in self.metadata:
                del self.metadata[filename]
                self._save_metadata()
            
            return {
                'success': True,
                'message': f'Document "{filename}" removed successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error removing file: {str(e)}'
            }
    
    def get_all_documents(self) -> List[Dict]:
        """Get list of all documents with their metadata"""
        documents = []
        
        for filename, metadata in self.metadata.items():
            file_info = self._get_file_info(filename)
            doc_info = {
                'filename': filename,
                'upload_date': metadata.get('upload_date'),
                'file_size': metadata.get('file_size'),
                'status': metadata.get('status', 'unknown'),
                'exists': file_info['exists']
            }
            
            if file_info['exists']:
                doc_info['modified'] = file_info['modified']
                doc_info['current_size'] = file_info['size']
            
            documents.append(doc_info)
        
        # Sort by upload date (newest first)
        documents.sort(key=lambda x: x.get('upload_date', ''), reverse=True)
        return documents
    
    def get_document_count(self) -> int:
        """Get total number of active documents"""
        return len([f for f in self.metadata.keys() 
                   if self.metadata[f].get('status') == 'active'])
    
    def cleanup_orphaned_files(self) -> Dict:
        """Remove files that exist in filesystem but not in metadata"""
        orphaned_files = []
        
        # Check for files in directory that aren't in metadata
        for file_path in self.docs_path.glob('*'):
            if file_path.is_file() and file_path.name not in self.metadata:
                if file_path.suffix.lower() in ['.pdf', '.txt', '.docx']:
                    orphaned_files.append(file_path.name)
        
        # Remove orphaned files
        removed_count = 0
        for filename in orphaned_files:
            try:
                (self.docs_path / filename).unlink()
                removed_count += 1
            except Exception:
                pass
        
        return {
            'removed_count': removed_count,
            'orphaned_files': orphaned_files
        }
    
    def sync_with_filesystem(self) -> Dict:
        """Sync metadata with files actually present in the filesystem"""
        synced_files = []
        new_files = []
        
        # Get all document files in the directory
        for file_path in self.docs_path.glob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt', '.docx']:
                filename = file_path.name
                
                # Skip metadata file
                if filename.endswith('_metadata.json'):
                    continue
                
                # If file not in metadata, add it
                if filename not in self.metadata:
                    try:
                        # Read file to get hash and size
                        with open(file_path, 'rb') as f:
                            file_content = f.read()
                        
                        file_hash = self._calculate_file_hash(file_content)
                        file_stat = file_path.stat()
                        
                        self.metadata[filename] = {
                            'hash': file_hash,
                            'upload_date': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                            'file_size': len(file_content),
                            'file_path': str(file_path),
                            'status': 'active',
                            'synced': True  # Mark as synced from filesystem
                        }
                        new_files.append(filename)
                    except Exception as e:
                        print(f"Error syncing {filename}: {e}")
                        continue
                
                synced_files.append(filename)
        
        # Remove metadata for files that no longer exist
        files_to_remove = []
        for filename in self.metadata.keys():
            file_path = self.docs_path / filename
            if not file_path.exists():
                files_to_remove.append(filename)
        
        for filename in files_to_remove:
            del self.metadata[filename]
        
        # Save updated metadata
        self._save_metadata()
        
        return {
            'synced_files': len(synced_files),
            'new_files': len(new_files),
            'removed_files': len(files_to_remove),
            'new_file_names': new_files
        }
    
    def get_storage_stats(self) -> Dict:
        """Get storage statistics"""
        # Sync with filesystem first to ensure accurate counts
        self.sync_with_filesystem()
        
        total_size = 0
        file_count = 0
        
        for filename, metadata in self.metadata.items():
            if metadata.get('status') == 'active':
                total_size += metadata.get('file_size', 0)
                file_count += 1
        
        return {
            'total_files': file_count,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'average_file_size_mb': round((total_size / file_count) / (1024 * 1024), 2) if file_count > 0 else 0
        } 