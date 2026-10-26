
import os
import asyncio
from flask import Flask, render_template_string, request, send_file
import edge_tts

app = Flask(__name__)

# মাইক্রোসফট এজ ন্যাচারাল ভয়েসসহ ফ্রন্টএন্ড ডিজাইন
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <title>Advanced Natural AI Voice Generator</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #0f172a; color: #f8fafc; text-align: center; margin: 0; padding: 50px; }
        .container { background: #1e293b; padding: 30px; border-radius: 12px; display: inline-block; box-shadow: 0 4px 20px rgba(0,0,0,0.5); width: 100%; max-width: 500px; }
        h1 { color: #38bdf8; font-size: 24px; margin-bottom: 20px; }
        textarea { width: 100%; height: 120px; padding: 12px; margin-bottom: 15px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 16px; box-sizing: border-box; resize: none; }
        select { width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 16px; box-sizing: border-box; }
        button { background: #2563eb; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-size: 16px; width: 100%; font-weight: bold; }
        button:hover { background: #1d4ed8; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Advanced Natural AI Voice</h1>
        <form method="POST" action="/generate">
            <textarea name="text" placeholder="মুভির স্ক্রিপ্ট এখানে লিখুন..." required></textarea><br>
            
            <select name="voice">
                <option value="bn-BD-PradeepNeural">বাংলা - পুরুষ কণ্ঠ (Natural)</option>
                <option value="bn-BD-NabanitaNeural">বাংলা - নারী কণ্ঠ (Natural)</option>
                <option value="en-US-AriaNeural">ইংরেজি - নারী কণ্ঠ (Natural)</option>
                <option value="en-US-GuyNeural">ইংরেজি - পুরুষ কণ্ঠ (Natural)</option>
            </select><br>

            <button type="submit">ন্যাচারাল ভয়েস জেনারেট ও ডাউনলোড করুন</button>
        </form>
    </div>
</body>
</html>
'''

async def generate_audio(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_voice():
    text = request.form.get('text')
    voice = request.form.get('voice', 'bn-BD-PradeepNeural')
    
    if not text:
        return "দয়া করে কিছু টেক্সট লিখুন!", 400
    
    audio_path = 'natural_voice.mp3'
    
    try:
        # এসিনক্রোনাস ফাংশন রেন্ডার সার্ভারে রান করানো
        asyncio.run(generate_audio(text, voice, audio_path))
        return send_file(audio_path, as_attachment=True)
    except Exception as e:
        return f"ভয়েস জেনারেট করতে সমস্যা হয়েছে: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
