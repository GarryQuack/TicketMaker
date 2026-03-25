import os
import io
import requests
from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# --- CONFIGURATION ---
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
# On Render, paths are relative to the root of your repo
FONT_PATH = "consola.ttf" 
TEMPLATE_PATH = "Test Order.png"

def get_fonts():
    return {
        "small": ImageFont.truetype(FONT_PATH, 30),
        "medium": ImageFont.truetype(FONT_PATH, 40),
        "big": ImageFont.truetype(FONT_PATH, 60)
    }

@app.route('/generate', methods=['GET'])
def generate_and_send():
    location = request.args.get('location', 'Standing')
    seatnum = request.args.get('seatnum', 'N/A')
    
    try:
        fonts = get_fonts()
        im = Image.open(TEMPLATE_PATH)
        d = ImageDraw.Draw(im)

        # Drawing Logic
        if location == "Seated":
            d.text((97,45), "You are in the...", fill='#000', font=fonts["small"])
            d.text((97,85), "Seated Area", fill="#000", font=fonts["medium"])
            d.text((97,130), "You are seated at:", fill="#000", font=fonts["small"])
            d.text((97,165), seatnum, fill="#000", font=fonts["big"])
        elif location == "Backstage":
            d.text((97,45), "You gain access to \nthe...", fill="#000", font=fonts["small"])
            d.text((97,105), location + " \nPass!", fill="#AA00DD", font=fonts["big"])
        else:
            d.text((97,45), "You are in the...", fill='#000', font=fonts["small"])
            d.text((97,105), location + " \nArea", fill="#000", font=fonts["big"])

        # Save to memory
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Send to Discord
        files = {'file': ('ticket.png', img_byte_arr, 'image/png')}
        payload = {"content": f"New ticket generated for **{location}**!"}
        response = requests.post(WEBHOOK_URL, data=payload, files=files)

        return jsonify({"status": "success", "discord_response": response.status_code}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
