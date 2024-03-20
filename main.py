import streamlit as st
import requests
import os
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime
import random
# Streamlit 应用设置
st.set_page_config(page_title="AI Image Generator", layout="wide")
# NovelAI API URL 和 API 请求头部
API_URL = 'https://api.novelai.net/ai/generate-image'
HEADERS = {
    'accept': 'application/json',
    'Authorization': f'Bearer {st.secrets["api_key"]}',
    'Content-Type': 'application/json'
}
IMAGES_FILE = 'generated_images.txt'
# Streamlit 应用主体
def main():
    st.title("AI Image Generator")
    col1, col2, col3 = st.columns([10, 80, 10])
    # 用户输入
    with col2:
        input_text = st.text_input("输入关键词", value="")
        num_images = st.number_input("连续生成图片数", min_value=1, max_value=100, value=1, step=1)
    # 生成按钮
        if st.button("Generate"):
        # 构建请求的JSON数据
            for _ in range(num_images):
                seed = random.randint(0, 9999999999)
                data = {
                    "input": f"{input_text}, best quality, amazing quality, very aesthetic, absurdres",
                    "model": "nai-diffusion-3",
                    "action": "generate",
                    "parameters": {
                    "params_version": 1,
                    "width": 832,
                    "height": 1216,
                    "scale": 5,
                    "sampler": "k_euler",
                    "steps": 28,
                    "n_samples": 1,
                    "ucPreset": 0,
                    "qualityToggle": True,
                    "sm": False,
                    "sm_dyn": False,
                    "dynamic_thresholding": False,
                    "controlnet_strength": 1,
                    "legacy": False,
                    "add_original_image": True,
                    "uncond_scale": 1,
                    "cfg_rescale": 0,
                    "noise_schedule": "native",
                    "legacy_v3_extend": False,
                    "reference_information_extracted": 1,
                    "reference_strength": 0.6,
                    "seed": seed,
                    "negative_prompt": "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract]"
                    }
                }
        # 发送请求并处理响应
                response = requests.post(API_URL, headers=HEADERS, json=data)
                if response.status_code == 200:
            # 解压zip文件并保存图片
                    zip_file = ZipFile(BytesIO(response.content))
                    file_name = zip_file.namelist()[0]
                    extracted_file = zip_file.open(file_name)
                    new_file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
                    with open(new_file_name, "wb") as f:
                        f.write(extracted_file.read())
                    with open(IMAGES_FILE,'a')as f:
                        f.write(new_file_name + '\n')
                    st.session_state.current_image = new_file_name
            # 显示生成的图片
    # 从文件中读取历史生成的图片路径
    if os.path.exists(IMAGES_FILE):
        with open(IMAGES_FILE, 'r') as f:
            st.session_state.generated_images = [line.strip() for line in f.readlines() if line.strip()]
    # 展示当前生成的图片
    if 'current_image' in st.session_state:
        with col2:
            st.subheader("当前图片")
            st.image(st.session_state.current_image, width=300)
    # 展示历史生成的图片
    if 'generated_images' in st.session_state:
        with col2:
            st.subheader("历史记录")
            for image_file in reversed(st.session_state.generated_images):
                st.image(image_file, use_column_width=True)
# 运行Streamlit应用
if __name__ == "__main__":
    main()
