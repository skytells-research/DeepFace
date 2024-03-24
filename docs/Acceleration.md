
# Acceleration
## CUDA (Nvidia)
Install CUDA Toolkit 11.8 and cuDNN for Cuda 11.x
Install dependencies:
```sh
pip uninstall onnxruntime onnxruntime-gpu
pip install onnxruntime-gpu==1.15.1
```
Usage in case the provider is available:
```sh
python run.py --execution-provider cuda
```


## CoreML (Apple)
#### Apple Silicon
Install dependencies:

```sh
pip uninstall onnxruntime onnxruntime-silicon
pip install onnxruntime-silicon==1.13.1
```
Usage in case the provider is available:
```sh
python run.py --execution-provider coreml
```

## Apple Legacy

Install dependencies:
```sh
pip uninstall onnxruntime onnxruntime-coreml
pip install onnxruntime-coreml==1.13.1
```
Usage in case the provider is available:
```sh
python run.py --execution-provider coreml
```

## DirectML (Windows)
Install dependencies:
```sh
pip uninstall onnxruntime onnxruntime-directml
pip install onnxruntime-directml==1.15.1
```
Usage in case the provider is available:
```sh
python run.py --execution-provider dml
```

## OpenVINO (Intel)
Install dependencies:
```sh
pip uninstall onnxruntime onnxruntime-openvino
pip install onnxruntime-openvino==1.15.0
```
Usage in case the provider is available:
```sh
python run.py --execution-provider openvino
```

