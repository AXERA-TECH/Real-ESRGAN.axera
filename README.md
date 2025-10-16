# Real-ESRGAN.axera
Real-ESRGAN DEMO on Axera

- 目前支持  Python 语言 
- 预编译模型下载[models](https://github.com/wzf19947/PPOCR_v5/releases/download/v1.0.0/model.tar.gz)。如需自行转换请参考[模型转换](/model_convert/README.md)

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
输出结果
![output](asserts/res_onnx.jpg)

##### 基于AXEngine运行  
在开发板上运行命令

```
cd python  
python3 run_axmodel.py --input ./pics --outscale 2 --model_path ./realesrgan-x2.axmodel
```  
输出结果
![output](asserts/res_ax.jpg)


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
