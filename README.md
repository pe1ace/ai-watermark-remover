
```markdown
# AI图片去水印工具 🚀

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/pytorch-2.0+-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/pe1ace/ai-watermark-remover.svg)](https://github.com/pe1ace/ai-watermark-remover/stargazers)

一个**生产级、开箱即用**的AI图片去水印工具，基于LaMa深度学习模型，提供**Web界面、命令行、Python API**三种使用方式。**完全绕过HuggingFace**，直接从GitHub下载模型，解决国内用户无法访问HuggingFace的痛点。

## ⚠️ 重要法律声明
**本工具仅可用于处理您自己拥有版权或已获得明确授权的图片**。未经许可去除他人版权图片的水印并用于商业用途或二次分发，可能违反《著作权法》及相关国际公约，需承担相应的法律责任。

## ✨ 核心特性
- 🎯 **效果出色**：使用LaMa深度学习模型，修复效果自然，几乎无痕迹
- 🌐 **国内友好**：完全绕过HuggingFace，模型直接从GitHub下载
- 🖥️ **多种接口**：Web界面、命令行、Python API全覆盖
- 📦 **批量处理**：支持批量去除固定位置水印
- 🎨 **自动检测**：自动检测白色半透明水印
- ⚡ **GPU加速**：支持CUDA加速，处理速度提升10倍以上
- 📱 **响应式UI**：美观的Web界面，支持画笔涂抹、撤销、清除
- 🔒 **隐私安全**：所有处理都在本地完成，图片不会上传到任何服务器

## 🚀 快速开始

### 安装
```bash
# 克隆仓库
git clone https://github.com/pe1ace/ai-watermark-remover.git
cd ai-watermark-remover

# 安装依赖
pip install -e .
```

### 使用Web界面（推荐）
```bash
watermark-remover web --port 8080
```
然后打开浏览器访问 `http://localhost:8080`

### 使用命令行
```bash
# 单张图片处理（使用掩码）
watermark-remover single input.jpg output.jpg --mask mask.png

# 单张图片处理（自动检测白色水印）
watermark-remover single input.jpg output.jpg --auto-white

# 批量处理固定位置水印
watermark-remover batch ./input_dir ./output_dir ./mask.png
```

### 使用Python API
```python
from watermark_remover import WatermarkRemover

# 初始化处理器
remover = WatermarkRemover()

# 单张图片处理
remover.remove_watermark("input.jpg", "output.jpg", mask_path="mask.png")

# 批量处理
remover.batch_remove("./input_dir", "./output_dir", "./mask.png")
```

## 🛠️ 技术栈
| 模块 | 技术选择 | 说明 |
|------|----------|------|
| 核心模型 | LaMa (Large Mask Inpainting) | 效果远超传统算法，开源且商业友好 |
| 深度学习框架 | PyTorch | 模型加载与推理 |
| 图像处理 | OpenCV + Pillow | 图像读写、预处理、掩码生成 |
| Web后端 | FastAPI | 高性能异步API，自动生成接口文档 |
| Web前端 | 原生HTML/CSS/JS | 轻量无依赖，无需额外构建工具 |
| 命令行 | Click | 优雅的命令行参数解析 |
| 进度显示 | tqdm | 批量处理进度条 |



## 📁 项目结构
```
ai-watermark-remover/
├── README.md               # 项目主文档
├── requirements.txt        # 依赖列表
├── setup.py                # 项目安装配置
├── .gitignore              # Git忽略文件
├── LICENSE                 # 许可证文件
├── watermark_remover/      # 核心代码包
│   ├── __init__.py
│   ├── model.py            # 模型加载与推理（TorchScript版本）
│   ├── processor.py        # 图像处理逻辑
│   ├── cli.py              # 命令行接口
│   └── api.py              # FastAPI接口
├── web/                    # Web前端文件
│   ├── index.html
│   ├── style.css
│   └── script.js
├── examples/               # 示例图片
│   ├── watermarked.jpg
│   └── mask.png
└── tests/                  # 测试用例
    └── test_processor.py
```

## 🤝 贡献
欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个Pull Request

## 📄 许可证
MIT License - 详情请见 [LICENSE](LICENSE) 文件
```

---

# 如何上传README到GitHub
## 第一步：修改个人信息
在上面的README中，把以下内容换成你自己的：
1. 第3行的GitHub仓库地址：`https://github.com/pe1ace/ai-watermark-remover`
2. 作者信息（如果需要的话）

## 第二步：添加示例图片（可选但推荐）
1. 找一张带水印的图片，命名为`watermarked.jpg`，放到`examples`文件夹
2. 用你的工具处理这张图片，得到`cleaned.jpg`，也放到`examples`文件夹
3. 这样别人打开你的GitHub就能直接看到效果了

## 第三步：提交并推送
在Git Bash终端（就是你之前用的那个MINGW64窗口），依次执行以下命令：

```bash
# 确保你在项目根目录
cd C:\Users\pe1ace\PyCharmMiscProject\ai-watermark-remover

# 添加所有修改
git add .

# 提交
git commit -m "添加完整的README文档和示例图片"

# 推送到GitHub（你已经配置了SSH，直接推送即可）
git push origin main
```

## 第四步：验证是否成功
打开你的GitHub仓库页面：https://github.com/pe1ace/ai-watermark-remover

刷新一下，你会看到页面底部已经显示出了完整的README文档，包括标题、徽章、特性、使用方法和效果展示。

---