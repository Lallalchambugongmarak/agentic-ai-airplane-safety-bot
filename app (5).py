
import gradio as gr
import random
from gtts import gTTS
import os

def get_status():
    systems = []
    def add(name, val, y, r, low=False):
        if low:
            if val <= r: st="🔴 WARNING"
            elif val <= y: st="🟡 CAUTION"
            else: st="🟢 HEALTHY"
        else:
            if val >= r: st="🔴 WARNING"
            elif val >= y: st="🟡 CAUTION"
            else: st="🟢 HEALTHY"
        systems.append(f"{name}: {val} - {st}")
    
    add("ENG-1 TEMP", random.randint(550,950),700,850)
    add("ENG-2 TEMP", random.randint(540,940),700,850)
    add("OIL PRESS", random.randint(35,95),60,45,low=True)
    add("FUEL", random.randint(500,5000),2000,1000,low=True)
    add("HYDRAULIC", random.randint(2000,3500),2800,2500,low=True)
    add("VIBRATION", round(random.uniform(1.0,5.5),2),3.0,4.5)
    return "\n".join(systems)

with gr.Blocks() as demo:
    gr.Markdown("# ✈️ Agentic AI Airplane Safety Bot - Before Incident Prevention")
    out = gr.Textbox(label="Live Monitoring", lines=10)
    btn = gr.Button("Check Now")
    btn.click(get_status, outputs=out)
    gr.Timer(3).tick(get_status, outputs=out)

demo.launch()
