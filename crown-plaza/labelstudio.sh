echo "Running Label Studio in the background"
docker run -dit --user root --name labelstudio -p 5000:8080 -v $(pwd)/data:/label-studio/data -e LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true -e LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/label-studio/data heartexlabs/label-studio:latest 
# chown -R 1001:root /label-studio/data/