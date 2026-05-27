import click
import os
from .processor import WatermarkRemover


@click.group()
def cli():
    """AI图片去水印工具 - 基于LaMa深度学习模型"""
    pass


@cli.command()
@click.argument("input_path")
@click.argument("output_path")
@click.option("--mask", "-m", help="掩码图片路径")
@click.option("--roi", "-r", nargs=4, type=int, help="ROI区域 x y w h")
@click.option("--auto-white", "-a", is_flag=True, help="自动检测白色水印")
@click.option("--threshold", "-t", default=220, type=int, help="白色水印检测阈值")
def single(input_path, output_path, mask, roi, auto_white, threshold):
    """处理单张图片"""
    remover = WatermarkRemover()
    remover.remove_watermark(
        input_path=input_path,
        output_path=output_path,
        mask_path=mask,
        roi=roi,
        auto_detect_white=auto_white,
        white_threshold=threshold
    )


@cli.command()
@click.argument("input_dir")
@click.argument("output_dir")
@click.argument("mask_path")
def batch(input_dir, output_dir, mask_path):
    """批量处理固定位置水印"""
    remover = WatermarkRemover()
    remover.batch_remove(input_dir, output_dir, mask_path)


@cli.command()
@click.option("--host", default="0.0.0.0", help="服务器地址")
@click.option("--port", default=8080, type=int, help="服务器端口")
def web(host, port):
    """启动Web服务"""
    import uvicorn
    from .api import app

    print(f"Web服务已启动，访问地址：http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    cli()