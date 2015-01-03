REMOTE_HOST=dedi.nexisonline.net
ROOT_DIR=/host/media.nexisonline.net
POOL_DIR=${ROOT_DIR}/files
TMP_POOL_DIR=${ROOT_DIR}/files-upl
CACHE_DIR=${ROOT_DIR}/cache
rsync -Rrhavvp --chmod=ugo=rw --delete --progress files-upl/ root@$REMOTE_HOST:$ROOT_DIR/
REMOTE_COMMAND="rm -rf ${POOL_DIR}/*"
REMOTE_COMMAND="${REMOTE_COMMAND} && cp -rv ${TMP_POOL_DIR}/* ${POOL_DIR}"
REMOTE_COMMAND="${REMOTE_COMMAND} && rm -rfv ${CACHE_DIR}/*"
REMOTE_COMMAND="${REMOTE_COMMAND} && chmod -R 755 ${POOL_DIR}"
REMOTE_COMMAND="${REMOTE_COMMAND} && chown -R www-data:www-data ${POOL_DIR}"
ssh root@$REMOTE_HOST $REMOTE_COMMAND
echo DONE.
