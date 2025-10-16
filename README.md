# Real-ESRGAN.axera
Real-ESRGAN DEMO on Axera

- 目前支持  Python 语言 
- 预编译模型下载[models](https://github.com/wzf19947/PPOCR_v5/releases/download/v1.0.0/model.tar.gz)。如需自行转换请参考[模型转换](/model_convert/README.md)
- 支持任意分辨率的x2、x4放大

## 支持平台

- [x] AX650N
- [ ] AX630C

## 模型转换

[模型转换](./model_convert/README.md)

## 上板部署

- AX650N 的设备已预装 Ubuntu22.04
- 以 root 权限登陆 AX650N 的板卡设备
- 链接互联网，确保 AX650N 的设备能正常执行 `apt install`, `pip install` 等指令
- 已验证设备：AX650N DEMO Board

### Python API 运行

#### Requirements

```
cd python
pip3 install -r requirements.txt
``` 

#### 运行

##### 基于 ONNX Runtime 运行  
可在开发板或PC运行 

在开发板或PC上，运行以下命令  
```  
cd python
python3 run_onnx.py --input ./pics --outscale 2 --model_path ./realesrgan-x2.onnx
```
```
Testing 0 00003
Testing 1 00017_gray
Testing 2 0014
Testing 3 0030
Testing 4 ADE_val_00000114
Testing 5 OST_009
Testing 6 children-alpha
Testing 7 tree_alpha_16bit
	Input is a 16-bit image
Testing 8 video
Testing 9 wolf_gray
```
输出结果
![output](results/1.png)

##### 基于AXEngine运行  
在开发板上运行命令

```
cd python  
python3 run_axmodel.py --input ./pics --outscale 2 --model_path ./realesrgan-x2.axmodel
```
```
[INFO] Available providers:  ['AxEngineExecutionProvider']
Testing 0 00003
[INFO] Using provider: AxEngineExecutionProvider
[INFO] Chip type: ChipType.MC50
[INFO] VNPU type: VNPUType.DISABLED
[INFO] Engine version: 2.12.0s
[INFO] Model type: 2 (triple core)
[INFO] Compiler version: 4.2-dirty 5e72cf06-dirty
Testing 1 00017_gray
[INFO] Using provider: AxEngineExecutionProvider
[INFO] Model type: 2 (triple core)
[INFO] Compiler version: 4.2-dirty 5e72cf06-dirty
Testing 2 0014
[INFO] Using provider: AxEngineExecutionProvider
[INFO] Model type: 2 (triple core)
[INFO] Compiler version: 4.2-dirty 5e72cf06-dirty
Testing 3 0030
[INFO] Using provider: AxEngineExecutionProvider
[INFO] Model type: 2 (triple core)
[INFO] Compiler version: 4.2-dirty 5e72cf06-dirty
Testing 4 ADE_val_00000114
[INFO] Using provider: AxEngineExecutionProvider
[INFO] Model type: 2 (triple core)
[INFO] Compiler version: 4.2-dirty 5e72cf06-dirty
Testing 5 OST_009
[INFO] Using provider: AxEngineExecutionProvider
[INFO] Model type: 2 (triple core)
[INFO] Compiler version: 4.2-dirty 5e72cf06-dirty
Testing 6 children-alpha
[INFO] Using provider: AxEngineExecutionProvider
[INFO] Model type: 2 (triple core)
[INFO] Compiler version: 4.2-dirty 5e72cf06-dirty
Testing 7 tree_alpha_16bit
        Input is a 16-bit image
[INFO] Using provider: AxEngineExecutionProvider
[INFO] Model type: 2 (triple core)
[INFO] Compiler version: 4.2-dirty 5e72cf06-dirty
Testing 8 wolf_gray
[INFO] Using provider: AxEngineExecutionProvider
[INFO] Model type: 2 (triple core)
[INFO] Compiler version: 4.2-dirty 5e72cf06-dirty
```
输出结果
![output](results/2.png)


运行参数说明:  
| 参数名称 | 说明  |
| --- | --- | 
| --input | 输入图片目录 | 
| --output | 保存结果目录 | 
| --outscale | 超分尺度 | 
| --model_path | 模型路径 | 
| --tile | 分块大小，默认128 | 

### Latency

#### AX650N

| model | latency(ms) |
|---|---|
|realesrgan-x2|15.6|
|realesrgan-x4|62.1|



## 技术讨论

- Github issues
- QQ 群: 139953715
