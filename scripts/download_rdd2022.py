#!/usr/bin/env python3
"""
Utility script to download the Road Damage Dataset 2022 (RDD2022).

The dataset is hosted on Figshare. This script streams the archive to disk
with a progress bar and optionally extracts it into the project's data directory.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

import requests
from tqdm import tqdm
import zipfile
import json
import subprocess
import shutil

# Figshare download URL for RDD2022 dataset
# Source: https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547
FIGSHARE_DOWNLOAD_URL = "https://figshare.com/ndownloader/files/40163855"
ARCHIVE_NAME = "RDD2022.zip"


def configure_logger(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_figshare_download_url() -> str:
    """Get the Figshare download URL for RDD2022 by querying the article page."""
    article_url = "https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547"
    
    try:
        # Try to get the download link from the article page
        response = requests.get(article_url, timeout=30, allow_redirects=True)
        response.raise_for_status()
        
        # Look for download link in the page (common patterns)
        import re
        # Try to find file download URLs in the page
        patterns = [
            r'https://figshare\.com/ndownloader/files/(\d+)',
            r'ndownloader/files/(\d+)',
            r'file_id["\']?\s*:\s*["\']?(\d+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response.text)
            if matches:
                file_id = matches[0]
                download_url = f"https://figshare.com/ndownloader/files/{file_id}"
                logging.info("Found Figshare file ID: %s", file_id)
                return download_url
    except Exception as e:
        logging.warning("Failed to extract download URL from Figshare article: %s", e)
    
    # Fallback to direct URL (user may need to update this)
    logging.warning("Using fallback Figshare URL. If download fails, check the article page for the correct file ID.")
    return FIGSHARE_DOWNLOAD_URL


def get_zenodo_download_url(record_id: str, filename: str) -> str:
    """Query Zenodo API to get the correct download URL for a file."""
    api_url = f"https://zenodo.org/api/records/{record_id}"
    logging.info("Querying Zenodo API for record %s", record_id)
    
    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Look for the file in the files list
        files = data.get("files", [])
        logging.debug("Found %d files in record", len(files))
        
        # Try exact match first
        for file_info in files:
            file_key = file_info.get("key", "")
            file_size = file_info.get("size", 0)
            logging.debug("Checking file: %s (size: %d)", file_key, file_size)
            
            # Case-insensitive matching
            if file_key.lower() == filename.lower() or filename.lower() in file_key.lower():
                # Try multiple possible link keys
                links = file_info.get("links", {})
                download_url = (
                    links.get("self") or 
                    links.get("download") or 
                    links.get("content")
                )
                if download_url:
                    logging.info("Found download URL via API: %s", download_url)
                    return download_url
                else:
                    logging.debug("File matched but no download link found. Links: %s", links)
        
        # If no exact match, try to find any zip file
        for file_info in files:
            file_key = file_info.get("key", "")
            if file_key.endswith(".zip") and "rdd" in file_key.lower():
                links = file_info.get("links", {})
                download_url = (
                    links.get("self") or 
                    links.get("download") or 
                    links.get("content")
                )
                if download_url:
                    logging.info("Found ZIP file via API: %s -> %s", file_key, download_url)
                    return download_url
        
        # Fallback: try to construct URL from bucket (if available in first file)
        if files and len(files) > 0:
            bucket = files[0].get("bucket")
            if bucket:
                fallback_url = f"{bucket}/{filename}"
                logging.info("Using bucket URL: %s", fallback_url)
                return fallback_url
        else:
            logging.warning("No files found in API response")
            
    except Exception as e:
        logging.warning("Failed to query Zenodo API: %s", e)
        import traceback
        logging.debug(traceback.format_exc())
    
    # Final fallback: try zenodo_get if available
    if shutil.which("zenodo_get"):
        logging.info("zenodo_get found, will use it as fallback")
        return None  # Signal to use zenodo_get
    
    # Final fallback URLs to try
    logging.warning("Using fallback URL pattern")
    fallbacks = [
        f"https://zenodo.org/record/{record_id}/files/{filename}?download=1",
        f"https://zenodo.org/records/{record_id}/files/{filename}?download=1",
    ]
    return fallbacks[0]


def download_with_zenodo_get(record_id: str, destination: Path, filename: str) -> bool:
    """Use zenodo_get command-line tool to download the dataset."""
    logging.info("Attempting download using zenodo_get for record %s", record_id)
    try:
        result = subprocess.run(
            ["zenodo_get", record_id, "-o", str(destination.parent)],
            capture_output=True,
            text=True,
            timeout=3600,  # 1 hour timeout
        )
        if result.returncode == 0:
            # Check if the zip file was downloaded (zenodo_get downloads to current dir or specified dir)
            zip_path = destination.parent / filename
            if zip_path.exists():
                # Move it to the expected location if needed
                if zip_path != destination:
                    shutil.move(str(zip_path), str(destination))
                logging.info("Successfully downloaded using zenodo_get")
                return True
            else:
                # Check if any zip file was downloaded
                zip_files = list(destination.parent.glob("*.zip"))
                if zip_files:
                    logging.info("Found zip file: %s, moving to %s", zip_files[0], destination)
                    shutil.move(str(zip_files[0]), str(destination))
                    return True
        else:
            logging.error("zenodo_get failed: %s", result.stderr)
            return False
    except FileNotFoundError:
        logging.error("zenodo_get not found. Install with: pip install zenodo-get")
        return False
    except subprocess.TimeoutExpired:
        logging.error("zenodo_get timed out")
        return False
    except Exception as e:
        logging.error("zenodo_get error: %s", e)
        return False


def stream_download(url: str, destination: Path) -> None:
    logging.info("Starting download from %s", url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    with requests.get(url, stream=True, timeout=60, headers=headers, allow_redirects=True) as response:
        response.raise_for_status()
        total = int(response.headers.get("Content-Length", 0))
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "wb") as f, tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            desc=f"Downloading {destination.name}",
        ) as progress:
            for chunk in response.iter_content(chunk_size=1 << 20):
                if chunk:
                    f.write(chunk)
                    progress.update(len(chunk))
    logging.info("Saved archive to %s", destination)


def extract_archive(archive_path: Path, extract_to: Path, force: bool) -> None:
    if extract_to.exists():
        if force:
            logging.info("Removing existing directory %s", extract_to)
            for child in extract_to.iterdir():
                if child.is_file():
                    child.unlink()
                else:
                    import shutil

                    shutil.rmtree(child)
        else:
            logging.info("Directory %s already exists; skipping extraction", extract_to)
            return

    logging.info("Extracting %s to %s", archive_path, extract_to)
    with zipfile.ZipFile(archive_path, "r") as zf:
        zf.extractall(extract_to)
    logging.info("Extraction complete")


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    default_raw_dir = project_root / "data" / "raw"

    parser = argparse.ArgumentParser(description="Download the RDD2022 dataset archive.")
    parser.add_argument(
        "--url",
        default=None,
        help="Direct download URL for RDD2022.zip (if not provided, will use Figshare)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(default_raw_dir),
        help="Directory where the archive and extracted data will be stored.",
    )
    parser.add_argument(
        "--skip-extract",
        action="store_true",
        help="Only download the archive without extracting it.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files/directories.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    configure_logger(args.verbose)

    output_dir = Path(args.output_dir).expanduser().resolve()
    archive_path = output_dir / ARCHIVE_NAME
    extract_dir = output_dir / "RDD2022"

    if archive_path.exists() and not args.force:
        logging.info("Archive already exists at %s; skipping download", archive_path)
    else:
        # Get download URL - either from args or use Figshare
        if args.url:
            download_url = args.url
        else:
            download_url = get_figshare_download_url()
            logging.info("Using Figshare download URL for RDD2022 dataset")
        
        stream_download(download_url, archive_path)

    if not args.skip_extract:
        extract_archive(archive_path, extract_dir, args.force)

    logging.info("Dataset setup finished. Raw data located at %s", extract_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())

