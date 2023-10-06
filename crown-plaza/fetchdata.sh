apt install python-pip
pip install gdown
url="https://drive.google.com/drive/folders/1sefSUgEwx_5pYImNcuAlXbgT6CCYlwHC?usp=drive_link"
url="https://drive.google.com/drive/u/1/folders/1ZcUdNPlxmOMWwnlZlZ-91hesEvfbcn_m"
mkdir -p ./data
gdown $url -O ./data/crown-plaza/data/video-processed --folder
