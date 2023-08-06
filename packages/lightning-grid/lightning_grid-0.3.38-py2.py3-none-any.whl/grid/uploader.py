"""
Uploader that uploads files into Cloud storage
"""
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
import os
from typing import Dict, IO, List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class UploadProgressCallback:
    """
    This class provides a interface for notifying upload progress
    """
    def upload_part_completed(self, part: int, etag: str):
        pass


class S3Uploader:
    """
    This class uploads a source file with presigned urls to S3

    Attributes
    ----------
    source_file_prefix: str
        Source file prefix to upload, assuming file was splitted using Unix split
    presigned_urls: Dict[int, str]
        Presigned urls dictionary, with key as part number and values as urls
    workers: int
        Amount of workers to upload parts
    retries: int
        Amount of retries when requests encounters an error
    progress_callback: UploadProgressCallback
        Callback for notifying upload progress
    """
    workers: int = 8
    retries: int = 10

    def __init__(self,
                 presigned_urls: Dict[int, str],
                 source_file_prefix: str,
                 progress_callback: UploadProgressCallback = None):
        self.presigned_urls = presigned_urls
        self.source_file_prefix = source_file_prefix
        self.upload_etags = None
        self.progress_callback = progress_callback

    @staticmethod
    def upload_s3_data(url: str, part_file: IO, retries: int) -> str:
        """
        Send data to s3 url

        Parameters
        ----------
        url: str
            S3 url string to send data to
        part_file: IO
            IO file to stream to s3
        retries: int
            Amount of retries

        Returns
        -------
        str
            ETag from response
        """
        s = requests.Session()
        retries = Retry(total=retries, status_forcelist=[500, 502, 503, 504])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        response = s.put(url, data=part_file)
        if 'ETag' not in response.headers:
            raise ValueError("Unexpected response from S3, headers: " +
                             f"{response.headers}")

        return response.headers['ETag']

    def _upload_part(self, url: str, part_path: str, part: int) -> None:
        """
        Upload part of the data file with presigned url

        Parameters
        ----------
        url: str
            Presigned url to upload to S3
        part_path: str
            Path to part file
        part: int
            Part number
        """
        with open(part_path, 'rb') as f:
            etag = self.upload_s3_data(url, f, self.retries)
            if self.progress_callback:
                self.progress_callback.upload_part_completed(part=part,
                                                             etag=etag)

    @staticmethod
    def get_split_files(file_prefix: str) -> List[str]:
        """
        Get all the split files in the source directory
        based on the file_prefix.

        Paramters
        ---------
        file_prefix: str
          Path to split files and prefix

        Returns
        -------
        List[str]
          List of files to upload
        """
        parts = []
        source_dir = os.path.dirname(file_prefix)
        prefix = os.path.basename(file_prefix)
        for root, _, files in os.walk(source_dir, topdown=True):
            for f in files:
                if f.startswith(prefix):
                    full_path = os.path.join(root, f)
                    parts.append(full_path)

        # Sort the files so it keeps the existing order
        parts.sort()

        return parts

    def upload(self) -> Dict[int, str]:
        """
        Upload files from source dir into target path in S3
        """
        parts = self.get_split_files(self.source_file_prefix)
        if len(parts) == 0:
            raise ValueError("Unable to find files to upload")

        if len(parts) != len(self.presigned_urls):
            parts_len = len(parts)
            presigned_len = len(self.presigned_urls)
            raise ValueError(
                f"Invalid part counts, detected {parts_len} but " +
                f"configured {presigned_len}")

        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            futures = []
            for part, url in self.presigned_urls.items():
                part_file = parts[part - 1]
                f = pool.submit(self._upload_part, url, part_file, part)
                futures.append(f)

            for future in as_completed(futures):
                future.result()

        return self.upload_etags
