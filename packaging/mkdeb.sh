#!/bin/bash

set -eux -o pipefail

project_dir="$(cd $(dirname "${BASH_SOURCE[0]}")/.. && pwd)"
version="$(git describe --tags --always --dirty)"

echo "project root: $project_dir"
echo "project version: $version"

cd "$project_dir"
ln -sf packaging/debian debian
debuild "-$version"

mkdir -p out
mv ../azure-nvme-utils_99.99.99* out/
rm debian
