from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import os
import tempfile
from PIL import Image
from .processor import WatermarkRemover

app = FastAPI(title="AI Watermark Remover API", version="1.0.0")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="web"), name="static")

# 初始化处理器
remover = WatermarkRemover()


@app.get("/", response_class=HTMLResponse)
async def root():
    """返回Web界面"""
    return FileResponse("web/index.html")


@app.post("/api/inpaint")
async def inpaint(
        image: UploadFile = File(...),
        mask: UploadFile = File(...)
):
    """
    图片修复API
    上传原始图片和掩码图片，返回修复后的图片
    """
    try:
        # 保存临时文件
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as img_tmp:
            img_tmp.write(await image.read())
            img_path = img_tmp.name

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as mask_tmp:
            mask_tmp.write(await mask.read())
            mask_path = mask_tmp.name

        # 执行修复
        output_path = tempfile.mktemp(suffix=".png")
        remover.remove_watermark(img_path, output_path, mask_path)

        # 清理临时文件
        os.unlink(img_path)
        os.unlink(mask_path)

        return FileResponse(output_path, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok", "device": remover.model._device}