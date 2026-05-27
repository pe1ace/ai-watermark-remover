let canvas, ctx;
let originalImage = null;
let maskCanvas = null;
let isDrawing = false;
let lastX = 0;
let lastY = 0;
let history = [];

document.addEventListener('DOMContentLoaded', () => {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    // 初始化掩码画布
    maskCanvas = document.createElement('canvas');

    // 事件监听
    document.getElementById('imageInput').addEventListener('change', handleImageUpload);
    document.getElementById('imageUpload').addEventListener('click', () => {
        document.getElementById('imageInput').click();
    });

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    document.getElementById('clearBtn').addEventListener('click', clearMask);
    document.getElementById('undoBtn').addEventListener('click', undo);
    document.getElementById('processBtn').addEventListener('click', processImage);
});

function handleImageUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
        const img = new Image();
        img.onload = () => {
            // 设置画布尺寸
            canvas.width = img.width;
            canvas.height = img.height;
            maskCanvas.width = img.width;
            maskCanvas.height = img.height;

            // 绘制原图
            ctx.drawImage(img, 0, 0);
            originalImage = img;

            // 初始化掩码
            const maskCtx = maskCanvas.getContext('2d');
            maskCtx.fillStyle = 'black';
            maskCtx.fillRect(0, 0, maskCanvas.width, maskCanvas.height);

            // 保存初始状态
            history = [maskCtx.getImageData(0, 0, maskCanvas.width, maskCanvas.height)];

            document.getElementById('processBtn').disabled = false;
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
}

function startDrawing(e) {
    isDrawing = true;
    [lastX, lastY] = getCanvasCoordinates(e);
}

function draw(e) {
    if (!isDrawing || !originalImage) return;

    const [x, y] = getCanvasCoordinates(e);

    // 在画布上绘制红色半透明线条
    ctx.strokeStyle = 'rgba(255, 0, 0, 0.5)';
    ctx.lineWidth = 20;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.stroke();

    // 在掩码画布上绘制白色线条
    const maskCtx = maskCanvas.getContext('2d');
    maskCtx.strokeStyle = 'white';
    maskCtx.lineWidth = 20;
    maskCtx.lineCap = 'round';
    maskCtx.lineJoin = 'round';
    maskCtx.beginPath();
    maskCtx.moveTo(lastX, lastY);
    maskCtx.lineTo(x, y);
    maskCtx.stroke();

    [lastX, lastY] = [x, y];
}

function stopDrawing() {
    if (isDrawing) {
        isDrawing = false;
        // 保存历史记录
        const maskCtx = maskCanvas.getContext('2d');
        history.push(maskCtx.getImageData(0, 0, maskCanvas.width, maskCanvas.height));
    }
}

function getCanvasCoordinates(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    return [
        (e.clientX - rect.left) * scaleX,
        (e.clientY - rect.top) * scaleY
    ];
}

function clearMask() {
    if (!originalImage) return;

    // 重绘原图
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(originalImage, 0, 0);

    // 清空掩码
    const maskCtx = maskCanvas.getContext('2d');
    maskCtx.fillStyle = 'black';
    maskCtx.fillRect(0, 0, maskCanvas.width, maskCanvas.height);

    history = [maskCtx.getImageData(0, 0, maskCanvas.width, maskCanvas.height)];
}

function undo() {
    if (history.length <= 1) return;

    history.pop();
    const lastState = history[history.length - 1];

    // 重绘原图
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(originalImage, 0, 0);

    // 重绘掩码
    const maskCtx = maskCanvas.getContext('2d');
    maskCtx.putImageData(lastState, 0, 0);

    // 在画布上绘制红色半透明掩码
    ctx.globalAlpha = 0.5;
    ctx.drawImage(maskCanvas, 0, 0);
    ctx.globalAlpha = 1;
}

async function processImage() {
    if (!originalImage) return;

    const processBtn = document.getElementById('processBtn');
    processBtn.disabled = true;
    processBtn.textContent = '处理中...';

    try {
        // 将原图和掩码转换为Blob
        const imageBlob = await canvasToBlob(originalImage);
        const maskBlob = await canvasToBlob(maskCanvas);

        // 创建FormData
        const formData = new FormData();
        formData.append('image', imageBlob, 'image.png');
        formData.append('mask', maskBlob, 'mask.png');

        // 发送请求
        const response = await fetch('/api/inpaint', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('处理失败');
        }

        const resultBlob = await response.blob();
        const resultUrl = URL.createObjectURL(resultBlob);

        // 显示结果
        document.getElementById('originalImage').src = URL.createObjectURL(imageBlob);
        document.getElementById('resultImage').src = resultUrl;
        document.getElementById('downloadBtn').href = resultUrl;
        document.getElementById('resultSection').style.display = 'block';

    } catch (error) {
        alert('处理失败：' + error.message);
    } finally {
        processBtn.disabled = false;
        processBtn.textContent = '开始去除水印';
    }
}

function canvasToBlob(canvas) {
    return new Promise((resolve) => {
        if (canvas instanceof HTMLImageElement) {
            // 如果是图片，先绘制到临时画布
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = canvas.width;
            tempCanvas.height = canvas.height;
            const tempCtx = tempCanvas.getContext('2d');
            tempCtx.drawImage(canvas, 0, 0);
            tempCanvas.toBlob(resolve, 'image/png');
        } else {
            canvas.toBlob(resolve, 'image/png');
        }
    });
}