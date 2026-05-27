import cv2
import numpy as np
from PIL import Image
import os
from typing import Optional, Tuple
from .model import LaMaModel


class WatermarkRemover:
    def __init__(self):
        self.model = LaMaModel()

    def remove_watermark(
            self,
            input_path: str,
            output_path: str,
            mask_path: Optional[str] = None,
            roi: Optional[Tuple[int, int, int, int]] = None,
            auto_detect_white: bool = False,
            white_threshold: int = 220
    ) -> None:
        """
        去除图片水印
        :param input_path: 输入图片路径
        :param output_path: 输出图片路径
        :param mask_path: 掩码图片路径（黑白图，白色为水印）
        :param roi: 手动框选的区域 (x, y, w, h)
        :param auto_detect_white: 是否自动检测白色水印
        :param white_threshold: 白色水印检测阈值（0-255）
        """
        # 读取图片
        img = Image.open(input_path).convert("RGB")

        # 生成掩码
        if mask_path is not None:
            mask = Image.open(mask_path).convert("L")
        elif roi is not None:
            mask = self._create_mask_from_roi(img.size, roi)
        elif auto_detect_white:
            mask = self._detect_white_watermark(input_path, white_threshold)
        else:
            raise ValueError("必须提供mask_path、roi或启用auto_detect_white")

        # 执行修复
        result = self.model.inpaint(img, mask)

        # 保存结果
        result.save(output_path, quality=95)
        print(f"处理完成：{output_path}")

    def _create_mask_from_roi(self, size: Tuple[int, int], roi: Tuple[int, int, int, int]) -> Image.Image:
        """从ROI区域创建掩码"""
        width, height = size
        x, y, w, h = roi

        mask = np.zeros((height, width), dtype=np.uint8)
        mask[y:y + h, x:x + w] = 255

        # 膨胀掩码，覆盖水印边缘
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)

        return Image.fromarray(mask)

    def _detect_white_watermark(self, image_path: str, threshold: int) -> Image.Image:
        """自动检测白色半透明水印"""
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 二值化检测白色区域
        _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

        # 形态学操作去除小噪点
        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return Image.fromarray(mask)

    def batch_remove(
            self,
            input_dir: str,
            output_dir: str,
            mask_path: str,
            extensions: list = ["jpg", "jpeg", "png"]
    ) -> None:
        """
        批量去除固定位置水印
        :param input_dir: 输入文件夹
        :param output_dir: 输出文件夹
        :param mask_path: 统一的掩码图片路径
        """
        from tqdm import tqdm

        os.makedirs(output_dir, exist_ok=True)

        # 获取所有图片文件
        image_files = []
        for ext in extensions:
            image_files.extend([f for f in os.listdir(input_dir) if f.lower().endswith(f".{ext}")])

        if not image_files:
            print("未找到任何图片文件")
            return

        print(f"找到 {len(image_files)} 张图片，开始批量处理...")

        # 加载掩码
        mask = Image.open(mask_path).convert("L")

        for filename in tqdm(image_files):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            try:
                img = Image.open(input_path).convert("RGB")
                result = self.model.inpaint(img, mask)
                result.save(output_path, quality=95)
            except Exception as e:
                print(f"处理失败 {filename}: {str(e)}")