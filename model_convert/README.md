# 模型转换

## 导出模型（ONNX）
导出real-esrgan onnx可以参考：https://github.com/xinntao/Real-ESRGAN/blob/master/scripts/pytorch2onnx.py

这里固定onnx输入尺寸为：1x3x128x128

## 动态onnx转静态
```
onnxsim realesrgan-x2.onnx  realesrgan-x2_sim.onnx --overwrite-input-shape=1,3,128,128
```

## 转换模型（ONNX -> Axera）
使用模型转换工具 `Pulsar2` 将 ONNX 模型转换成适用于 Axera 的 NPU 运行的模型文件格式 `.axmodel`，通常情况下需要经过以下两个步骤：

- 生成适用于该模型的 PTQ 量化校准数据集
- 使用 `Pulsar2 build` 命令集进行模型转换（PTQ 量化、编译），更详细的使用说明请参考 [AXera Pulsar2 工具链指导手册](https://pulsar2-docs.readthedocs.io/zh-cn/latest/index.html)

### 量化数据集
准备量化图片若张，打包成Image.zip或准备量化npy文件

### 模型转换

#### 修改配置文件
 
检查`config.json` 中 `calibration_dataset` 字段，将该字段配置的路径改为上一步下载的量化数据集存放路径  

#### Pulsar2 build

参考命令如下：

```
pulsar2 build --input realesrgan-x2.onnx --config ./build_config.json --output_dir ./output --output_name realesrgan-x2.axmodel  --target_hardware AX650 --compiler.check 0

也可将参数写进json中，直接执行：
pulsar2 build --config ./build_config.json
```
