"""
Supabase storage client for file uploads
"""
from typing import Optional
import uuid
from supabase import create_client, Client
from app.config.settings import settings
from app.core.logging import get_logger
from app.core.exceptions import StorageException

logger = get_logger(__name__)


class SupabaseStorage:
    """Supabase storage client"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.bucket = settings.SUPABASE_STORAGE_BUCKET
    
    def connect(self) -> None:
        """Initialize Supabase client"""
        try:
            self.client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_KEY
            )
            logger.info("supabase_storage_connected")
        except Exception as e:
            logger.error("supabase_storage_connection_failed", error=str(e))
            raise StorageException(f"Failed to connect to Supabase: {str(e)}")
    
    async def upload_file(
        self,
        file_content: bytes,
        file_name: str,
        content_type: str = "image/jpeg"
    ) -> str:
        """
        Upload file to Supabase storage
        
        Args:
            file_content: File bytes
            file_name: Name of the file
            content_type: MIME type of the file
            
        Returns:
            Public URL of uploaded file
        """
        if not self.client:
            self.connect()
        
        try:
            # Generate unique file name
            unique_name = f"{uuid.uuid4()}_{file_name}"
            
            # Upload file
            self.client.storage.from_(self.bucket).upload(
                path=unique_name,
                file=file_content,
                file_options={"content-type": content_type}
            )
            
            # Get public URL
            url = self.client.storage.from_(self.bucket).get_public_url(unique_name)
            
            logger.info("file_uploaded", file_name=unique_name, url=url)
            return url
            
        except Exception as e:
            logger.error("file_upload_failed", file_name=file_name, error=str(e))
            raise StorageException(f"Failed to upload file: {str(e)}")
    
    async def delete_file(self, file_url: str) -> bool:
        """
        Delete file from Supabase storage
        
        Args:
            file_url: URL of the file to delete
            
        Returns:
            True if successful
        """
        if not self.client:
            self.connect()
        
        try:
            # Extract file path from URL
            # URL format: https://xxx.supabase.co/storage/v1/object/public/bucket-name/file-path
            parts = file_url.split(f"/{self.bucket}/")
            if len(parts) != 2:
                raise ValueError("Invalid file URL format")
            
            file_path = parts[1]
            
            # Delete file
            self.client.storage.from_(self.bucket).remove([file_path])
            
            logger.info("file_deleted", file_path=file_path)
            return True
            
        except Exception as e:
            logger.error("file_delete_failed", file_url=file_url, error=str(e))
            return False
    
    async def download_file(self, file_url: str) -> bytes:
        """
        Download file from URL
        
        Args:
            file_url: URL of the file to download
            
        Returns:
            File bytes
        """
        import httpx
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(file_url)
                response.raise_for_status()
                return response.content
        except Exception as e:
            logger.error("file_download_failed", file_url=file_url, error=str(e))
            raise StorageException(f"Failed to download file: {str(e)}")


# Global storage instance
supabase_storage = SupabaseStorage()


def get_storage() -> SupabaseStorage:
    """Dependency to get storage client"""
    return supabase_storage
