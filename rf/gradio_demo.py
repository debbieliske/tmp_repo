#!/usr/bin/env python
"""
Folium + Gradio demo (reduced flicker by throttling to every 5 pings)
--------------------------------------------------------------------
• Data   : stream_demo_close.csv
• Updates: map refreshed only when `step % THROTTLE == 0`
"""

import time
import pandas as pd
import gradio as gr
import folium
from branca.element import Template, MacroElement

# ------------------------------------------------------------------ #
# parameters
# ------------------------------------------------------------------ #
THROTTLE = 5            # refresh map every N pings (5 → about 2.5 s)

# ------------------------------------------------------------------ #
# load data & helper
# ------------------------------------------------------------------ #
DF = pd.read_csv("stream_demo_close.csv").sort_values("timestamp").reset_index(drop=True)

def mock_classifier(row):
    return int(row.true_vessel_id)

def alert(pred_id, claimed):
    if pd.isna(claimed) or claimed == "":
        return "dark"
    return "normal" if int(pred_id) == int(claimed) else "spoof"

COLOR = {"normal": "green", "spoof": "red", "dark": "orange"}
LABEL = {111111111: "V‑111", 222222222: "V‑222", 333333333: "V‑333"}

# ------------------------------------------------------------------ #
# Folium map init + legend
# ------------------------------------------------------------------ #
m      = folium.Map(location=[DF.lat.mean(), DF.lon.mean()], zoom_start=9)
layer  = folium.FeatureGroup(name="vessels").add_to(m)

legend = """
{% macro html(this, kwargs) %}
<div style="
     position: fixed; bottom: 20px; left: 20px; width: 150px;
     z-index: 900; font-size: 11px;
     background: rgba(255,255,255,0.9); padding:6px 8px;
     border:1px solid #999; border-radius:4px;">
<b>Legend</b><br>
<span style='color:green;'>●</span> normal<br>
<span style='color:red;'>●</span> spoof<br>
<span style='color:orange;'>●</span> dark<br><hr>
<b>Labels</b><br>
V‑111 First vessel<br>
V‑222 Second vessel<br>
V‑333 Third vessel
</div>
{% endmacro %}
"""
macro = MacroElement(); macro._template = Template(legend)
m.get_root().add_child(macro)

# handles
markers = {}
tracks  = {}

# ------------------------------------------------------------------ #
# playback generator
# ------------------------------------------------------------------ #
def playback(speed):
    step = 0
    layer._children.clear(); markers.clear(); tracks.clear()
    yield gr.update(value=m._repr_html_())      # first frame

    for _, row in DF.iterrows():
        vid   = mock_classifier(row)
        col   = COLOR[alert(vid, row.claimed_id)]

        # create / update marker
        if vid not in markers:
            markers[vid] = folium.CircleMarker(location=[row.lat, row.lon],
                                               radius=6,
                                               color=col, fill=True,
                                               fill_color=col, fill_opacity=0.9)
            layer.add_child(markers[vid])
            tracks[vid] = folium.PolyLine([[row.lat, row.lon]],
                                          color="#6c6cff", weight=2, opacity=0.6)
            layer.add_child(tracks[vid])
        else:
            markers[vid].location = [row.lat, row.lon]
            markers[vid].color = markers[vid].fill_color = col
            tracks[vid].locations.append([row.lat, row.lon])

        markers[vid].tooltip = f"{LABEL[vid]} | {col}"

        # refresh map only every THROTTLE steps
        if step % THROTTLE == 0:
            yield gr.update(value=m._repr_html_())
        step += 1
        time.sleep(1.0 / speed)

# ------------------------------------------------------------------ #
# Gradio UI
# ------------------------------------------------------------------ #
with gr.Blocks(title="RF‑Fingerprint Demo (Folium throttled)") as demo:
    gr.Markdown("## RF‑Fingerprint Demo – Folium (update every 5 pings)")
    speed = gr.Slider(1, 20, 10, label="Playback speed (× real‑time)")
    html  = gr.HTML()
    start = gr.Button("▶ Start")
    start.click(fn=playback, inputs=speed, outputs=html)

if __name__ == "__main__":
    demo.launch()