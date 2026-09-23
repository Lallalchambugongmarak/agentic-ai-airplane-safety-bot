!pip install -q --upgrade gradio gTTS

import gradio as gr
import random, pandas as pd
from datetime import datetime
from gtts import gTTS

history = []

def update_airplane():
    ts = datetime.now().strftime("%H:%M:%S")
    systems = []
    def add(name, val, y, r, low=False):
        if low:
            if val < r: st,bg,col = "🔴 WARNING","#f8d7da","#721c24"
            elif val < y: st,bg,col = "🟡 CAUTION","#fff3cd","#856404"
            else: st,bg,col = "🟢 HEALTHY","#d4edda","#155724"
        else:
            if val >= r: st,bg,col = "🔴 WARNING","#f8d7da","#721c24"
            elif val >= y: st,bg,col = "🟡 CAUTION","#fff3cd","#856404"
            else: st,bg,col = "🟢 HEALTHY","#d4edda","#155724"
        systems.append({"name":name,"value":val,"status":st,"bg":bg,"color":col})

    add("ENG-1 TEMP", random.randint(550,950),700,850)
    add("ENG-2 TEMP", random.randint(540,940),700,850)
    add("OIL PRESS", random.randint(35,95),60,45,low=True)
    add("FUEL", random.randint(500,5000),2000,1000,low=True)
    add("HYDRAULIC", random.randint(2000,3500),2800,2500,low=True)
    add("VIBRATION", round(random.uniform(1.0,5.5),2),3.0,4.5)

    red = sum(1 for s in systems if "WARNING" in s["status"])
    yellow = sum(1 for s in systems if "CAUTION" in s["status"])

    if red > 0:
        banner_color = "#f8d7da"; border="red"; title="⛔ PULL UP! AGENTIC AI GROUNDED - ACCIDENT PREVENTED BEFORE INCIDENT"
        voice_text = "Master Warning! Pull up! Pull up! Critical failure! Flight grounded! Accident prevented!"
    elif yellow > 0:
        banner_color = "#fff3cd"; border="orange"; title=f"⚠️ CAUTION - Predictive Failure in 15 minutes - {yellow} issues"
        voice_text = "Master Caution! Predictive failure in fifteen minutes!"
    else:
        banner_color = "#d4edda"; border="green"; title="✅ ALL SYSTEMS GREEN - AI CLEARED FOR FLIGHT"
        voice_text = "All green! Safe to fly!"

    # Create voice mp3
    try:
        tts = gTTS(text=voice_text, lang='en', slow=False)
        tts.save("/tmp/alert.mp3")
        audio_path = "/tmp/alert.mp3"
    except:
        audio_path = None

    sys_html = "".join([f"<div style='background:{s['bg']};border-left:8px solid {s['color']};padding:10px;margin:6px;border-radius:5px;'><b>{s['status']} | {s['name']}: {s['value']}</b></div>" for s in systems])

    full_html = f"""
    <div style='font-family:Arial;'>
        <div style='display:flex; justify-content:space-between;'>
            <h2>✈️ AI-101 | {ts}</h2>
            <h3 style='background:black;color:#00ff00;padding:5px 15px;border-radius:20px;'>● LIVE AUTO MONITORING EVERY 3 SEC</h3>
        </div>
        <div style='background:{banner_color};border:3px solid {border};padding:15px;text-align:center;border-radius:10px;'>
            <h1 style='margin:0;'>{title}</h1>
            <p>🤖 AGENTIC AI is Thinking... Observing {len(systems)} sensors -> Acting by itself</p>
        </div>
        <div style='margin-top:15px;'>{sys_html}</div>
    </div>
    """

    for s in systems:
        history.append({"time":ts,"system":s["name"],"value":s["value"],"status":s["status"]})
    if len(history)>30: history[:] = history[-30:]

    return full_html, pd.DataFrame(history), audio_path

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 AGENTIC AI - AUTO MONITORING EVERY 3 SEC - BEFORE FLIGHT SAFETY BOT")
    gr.Markdown("### 🔴 This bot runs by itself - Thinks and Acts - No human needed - Accident prevented BEFORE incident")
    live = gr.HTML()
    table = gr.Dataframe(label="Black Box - Flight History Log")
    audio = gr.Audio(label="🔊 LIVE PILOT VOICE ALERT - Auto Speaks", autoplay=True)

    # THIS IS THE AUTO BOT - Runs every 3 seconds!
    timer = gr.Timer(3)  # <--- AUTO MONITORING
    timer.tick(fn=update_airplane, outputs=[live, table, audio])

    # Also manual button
    btn = gr.Button("🔄 Manual Check + Hear Voice Now")
    btn.click(fn=update_airplane, outputs=[live, table, audio])

    demo.load(fn=update_airplane, outputs=[live, table, audio])

demo.launch(share=True, debug=True)
