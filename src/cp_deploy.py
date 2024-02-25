# 引入fastapi及对应CORS跨域库
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io

import torch
from albumentations.pytorch import ToTensorV2

import runner.config as config
from src.modeling import glam
# import cv2
import albumentations as A

app = FastAPI()
# 允许本地地址实现跨域,日后按需求更改
origins = [
    "http://localhost",
    "http://localhost:8080",  # 本地应用运行的地址
]
# 日后按需求限制访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

parameters = {
    "device_type": "cuda",
    "cam_size": (184, 120),
    "top_k_per_class": 1,
    "crop_shape": (512, 512),
    "percent_k": 0.03,
    "detection_pooling_percent_k": 0.3,
    "fusion": True
}
model = glam.MILSingleImageModel(parameters).to(config.device)

x = torch.load(r"E:\code\GLAM-main\models\model_joint.ckpt", map_location="cuda")
model.load_state_dict(x, strict=False)

if __name__ == '__main__':
    # 定义推理流程
    model.eval()

    @app.post("/recognition")
    async def canser_recognition(image:UploadFile=File(...)):
        img=await image.read()
        # img = cv2.imread(r'E:\code\GLAM-main\sample_data\images\0_L-CC.png', cv2.IMREAD_GRAYSCALE)
        transform = A.Compose([
            A.Resize(width=2944, height=1920),  # 调整大小
            A.Normalize(mean=0.456, std=0.224),  # 标准化
            ToTensorV2(), ]  # 转换为张量
        )
        img = transform(image=img)['image']
        img = img.unsqueeze(0).to(config.device)
        output = model(img)
        ####
        # sanyin:0
        # no_sanyin:1
        # 判断是否是sanyin
        # 并输出置信度
        # print(output)
        # Assuming you have two classes: 'sanyin' and 'no_sanyin'
        class_names = ['sanyin', 'no_sanyin']
        # Apply softmax to get probabilities
        probs = torch.nn.functional.softmax(output, dim=1)[0] * 100

        # Get the predicted class index
        _, predicted = torch.max(output, 1)
        predicted = predicted.item()
        # print the result
        print(f'Predicted: {class_names[predicted]}, Confidence: {probs[predicted]:.2f}%')
        # print(f'Predicted: {class_names[predicted]}, Confidence: {probs[predicted]:.2f}%')

        # 用键值对JSON格式返回
        return{
            "Output":StreamingResponse(io.BytesIO(output), media_type="image/png"),
            "Predicted":class_names[predicted],
            "Confidence":f'{probs[predicted]:.2f}%'
        }
