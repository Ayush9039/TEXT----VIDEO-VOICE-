import requests
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip
import numpy as np
from io import BytesIO
import time
import os

def generate_video(user_text, output_path=None, width=720, height=480, duration=5, fps=24):
    total_frames = duration * fps

    # 🔹 Background image
    url = "https://t3.ftcdn.net/jpg/06/47/34/56/360_F_647345699_EvAsCpJuLSr1Tg2PoQA7Zz97zCBL4DUT.jpg"
    response = requests.get(url)
    bg = Image.open(BytesIO(response.content)).convert("RGB").resize((width, height))
    print("✅ Loaded Image Size:", bg.size)

    font = ImageFont.truetype("arial.ttf", 60)
    frames = []

    for i in range(total_frames):
        # ✅ Direct RGB copy, no RGBA
        img = bg.copy()
        draw = ImageDraw.Draw(img)

        # Text position
        bbox = draw.textbbox((0, 0), user_text, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pos = ((width - text_w) // 2, (height - text_h) // 2)

        # Fade-in / Fade-out
        if i < fps:
            alpha = int(255 * (i / fps))
        elif i > total_frames - fps:
            alpha = int(255 * ((total_frames - i) / fps))
        else:
            alpha = 255

        shadow_offset = 4
        # Draw shadow
        shadow_color = (0, 0, 0)
        draw.text((pos[0] + shadow_offset, pos[1] + shadow_offset), user_text, font=font, fill=shadow_color)
        # Draw text
        draw.text(pos, user_text, font=font, fill=(255, 255, 255))

        frames.append(np.array(img))  # ✅ RGB array, no conversion

    # 🔹 Unique filename
    if output_path is None:
        output_path = f"outputs/output_{int(time.time())}.mp4"
    else:
        # Delete old file if exists
        if os.path.exists(output_path):
            os.remove(output_path)

    # 🔹 Create video
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(output_path, fps=fps)

    return output_path
