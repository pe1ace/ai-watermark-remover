import os
import torch
import torch.nn.functional as F
from PIL import Image
import numpy as np
from typing import Optional
import requests
from tqdm import tqdm


class LaMaModel:
    """LaMa模型单例类，直接加载TorchScript格式模型，完全绕过HuggingFace"""
    _instance: Optional["LaMaModel"] = None
    _model: Optional[torch.jit.ScriptModule] = None
    _device: str = "cuda" if torch.cuda.is_available() else "cpu"

    # 模型下载地址（GitHub官方发布，永久可用）
    MODEL_URL = "https://github.com/enesmsahin/simple-lama-inpainting/releases/download/v0.1.0/big-lama.pt"
    # 本地缓存路径
    CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "torch", "hub", "checkpoints")
    MODEL_FILENAME = "big-lama.pt"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _download_model(self):
        """从GitHub下载模型文件，带进度条"""
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        model_path = os.path.join(self.CACHE_DIR, self.MODEL_FILENAME)

        if os.path.exists(model_path):
            print(f"模型已存在于本地缓存：{model_path}")
            return model_path

        print(f"正在从GitHub下载LaMa模型（约196MB）...")
        response = requests.get(self.MODEL_URL, stream=True)
        total_size = int(response.headers.get("content-length", 0))

        with open(model_path, "wb") as f, tqdm(
                desc="下载进度",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)

        print(f"模型下载完成，已保存到：{model_path}")
        return model_path

    def _load_model(self):
        """加载TorchScript格式的LaMa模型"""
        print(f"正在加载LaMa模型到 {self._device}...")

        # 下载或获取本地模型路径
        model_path = self._download_model()

        # 加载模型
        self._model = torch.jit.load(model_path, map_location=self._device)
        self._model.eval()

        print("模型加载完成！")

    def inpaint(self, image: Image.Image, mask: Image.Image) -> Image.Image:
        """
        执行图像修复
        :param image: 原始图片（RGB）
        :param mask: 掩码图片（L模式，白色为需要修复的区域）
        :return: 修复后的图片
        """
        if self._model is None:
            raise RuntimeError("模型未加载")

        # 保存原始尺寸
        original_size = image.size

        # LaMa要求尺寸为8的倍数
        width, height = image.size
        new_width = (width // 8) * 8
        new_height = (height // 8) * 8

        if new_width != width or new_height != height:
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            mask = mask.resize((new_width, new_height), Image.Resampling.NEAREST)

        # 转换为张量
        img_tensor = torch.from_numpy(np.array(image)).permute(2, 0, 1).float() / 255.0
        mask_tensor = torch.from_numpy(np.array(mask)).float() / 255.0
        mask_tensor = mask_tensor.unsqueeze(0)

        # 扩展批次维度
        img_tensor = img_tensor.unsqueeze(0).to(self._device)
        mask_tensor = mask_tensor.unsqueeze(0).to(self._device)

        # 执行推理
        with torch.no_grad():
            result = self._model(img_tensor, mask_tensor)

        # 后处理
        result = torch.clamp(result, 0, 1)
        result = result.squeeze(0).permute(1, 2, 0).cpu().numpy()
        result = (result * 255).astype(np.uint8)

        # 转换为PIL图像并恢复原始尺寸
        result_image = Image.fromarray(result)
        result_image = result_image.resize(original_size, Image.Resampling.LANCZOS)

        return result_image