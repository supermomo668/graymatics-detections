echo "Running Label Studio in the background"
docker run -it --user root --name labelstudio -p 5000:8080 -v $(pwd)/labelstudio-data:/label-studio/data heartexlabs/label-studio:latest 
# chown -R 1001:root /label-studio/data/