#!/bin/bash
echo Have you updated package version?
read
./setup.py sdist --formats=gztar upload
echo "Generating docs"
./setup.py build_sphinx
echo "Uploading docs to pypi"
./setup.py upload_docs --upload-dir build/sphinx/html/

