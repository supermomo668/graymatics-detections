import torch, numpy as np, cv2, subprocess
from PIL import Image

def export_onnx(model_name='yolov5n'):
  # load & download .pt model
  model = torch.hub.load(
    'ultralytics/yolov5', 'custom', f'{model_name}.pt', force_reload=True)  
    # yolov5n - yolov5x6 or custom
  subprocess.check_call(
    f"python export.py --weights {model_name} --include onnx --dynamic".split(' ')
  )
  model_onnx = torch.hub.load(
    './', 
    'custom', 
    path=f"{model_name}.onnx",
    source='local', 
    force_reload = True
  )
  return model_onnx

if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('model_name', nargs='?', type=str, default='yolov5n',
                    help='name of model to export')
    args = ap.parse_args()
    export_onnx(args.model_name)