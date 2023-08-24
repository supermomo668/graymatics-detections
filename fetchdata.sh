apt install python-pip
pip install gdown
url="https://drive.google.com/drive/folders/1sefSUgEwx_5pYImNcuAlXbgT6CCYlwHC?usp=drive_link"
mkdir -p ./data
gdown $url -O ./data/crown-plaza --folder
