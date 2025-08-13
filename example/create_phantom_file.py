from os.path import getsize as _get_file_size
from os import remove as _delete_file
from tqdm import tqdm
from pathlib import Path as _Path
from struct import pack as _struct_pack
from aiofiles import open as _aio_open
from asyncio import gather, run as _aio_run, get_running_loop
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileCreationError(Exception):
    """Custom exception for file creation errors"""
    pass

async def create_file(
    size_mb: int,
    path: _Path = _Path(".zip"),
    *,
    chunk_size: int = 1024 * 1024,
    progress_bar: Optional[tqdm] = None
) -> None:
    """
    Create a phantom file of specified size.
    
    Args:
        size_mb: Size of the file in megabytes
        path: Path where the file should be created
        chunk_size: Size of chunks to write (default: 1MB)
        progress_bar: Optional progress bar instance
    """
    if size_mb <= 0:
        raise ValueError("File size must be a positive number")

    target_size = size_mb * 1024 * 1024
    local_progress = progress_bar or tqdm(
        total=target_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        desc=f"Creating file: {path.name}",
    )

    try:
        async with _aio_open(path, "wb") as file:
            # Write minimal valid ZIP header
            await file.write(b"PK\x03\x04\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            await file.write(_struct_pack("<I", 0xFFFFFFFF))  # CRC
            await file.write(_struct_pack("<I", target_size - 30))  # File size
            await file.write(b"phantom_file.bin")

            await file.flush()
            bytes_written = await file.tell()
            local_progress.update(bytes_written)
            
            remaining_size = target_size - bytes_written
            chunk_count = remaining_size // chunk_size
            last_chunk_size = remaining_size % chunk_size

            # Pre-allocate the chunk buffer
            chunk = b"\0" * chunk_size
            
            # Write full chunks
            for _ in range(chunk_count):
                await file.write(chunk)
                await file.flush()
                local_progress.update(chunk_size)

            # Write remaining bytes
            if last_chunk_size > 0:
                await file.write(b"\0" * last_chunk_size)
                local_progress.update(last_chunk_size)

        if progress_bar is None:
            local_progress.close()

        actual_size = _get_file_size(path)
        if actual_size < target_size * 0.99:
            _delete_file(path)
            raise FileCreationError(
                f"File size mismatch. Expected: {size_mb}MB, Got: {actual_size//1024//1024}MB"
            )

    except Exception as e:
        if progress_bar is None:
            local_progress.close()
        raise FileCreationError(f"Failed to create file: {str(e)}")

async def main():
    """Main function to create multiple files concurrently"""
    try:
        loop = get_running_loop()
        output_dir = _Path("d:/")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a single progress bar for all files
        total_size = 1024 * 10  # 10GB total
        progress = tqdm(
            total=total_size * 1024 * 1024,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc="Total progress"
        )
        
        tasks = [
            loop.create_task(
                create_file(
                    1024,
                    output_dir / f"1GB_{index+1}.zip",
                    chunk_size=5 * 1024 * 1024,
                    progress_bar=progress
                )
            )
            for index in range(10)
        ]
        
        results = await gather(*tasks, return_exceptions=True)
        
        # Check for any errors
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error creating file {i+1}: {str(result)}")
        
        progress.close()
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    _aio_run(main())
