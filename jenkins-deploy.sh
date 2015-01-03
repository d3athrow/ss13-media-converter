#!/bin/bash
# This is run locally by Jenkins CI after each push.
#
ROOT_DIR=/host/media.nexisonline.net
POOL_DIR=${ROOT_DIR}/files
TMP_POOL_DIR=${ROOT_DIR}/files-upl
CACHE_DIR=${ROOT_DIR}/cache

set -x
rsync -Rrhavvp --chmod=ugo=rw --delete --progress files-upl/ $ROOT_DIR/
rm -rf $POOL_DIR/*
cp -r ${TMP_POOL_DIR}/* ${POOL_DIR}
rm -rf ${CACHE_DIR}/*
chmod -R 755 ${POOL_DIR} 
