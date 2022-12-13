docker run \
   -p 9000:9000 \
   -p 9090:9090 \
   --name minio \
   -v ~/dev/minio/data:/data \
   -e "MINIO_ROOT_USER=minio" \
   -e "MINIO_ROOT_PASSWORD=minio123" \
   quay.io/minio/minio server /data --console-address ":9090"
