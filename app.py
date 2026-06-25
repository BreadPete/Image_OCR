import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pytesseract
from PIL import Image
import numpy as np
import cv2
import io

st.set_page_config(
    page_title="kontAbil — Image OCR Scanner",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0f0f0f;
    color: #e8e8e8;
  }

  .stApp { background-color: #0f0f0f; }

  h1, h2, h3 { font-family: 'IBM Plex Mono', monospace; color: #e8e8e8; }

  .title-block {
    border-left: 3px solid #d3aee6;
    padding: 0.4rem 1rem;
    margin-bottom: 2rem;
  }
  .title-block h1 { font-size: 1.8rem; margin: 0; letter-spacing: -0.5px; }
  .title-block p  { margin: 0.2rem 0 0 0; color: #888; font-size: 0.85rem; }

  .tutorial-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.2rem;
  }
  .tutorial-card h4 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #d3aee6;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 0.8rem 0;
  }
  .step {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    margin-bottom: 0.6rem;
    font-size: 0.83rem;
    color: #bbb;
    line-height: 1.5;
  }
  .step-num {
    background: #d3aee6;
    color: #0f0f0f;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 0.7rem;
    border-radius: 2px;
    padding: 1px 6px;
    min-width: 20px;
    text-align: center;
    margin-top: 2px;
  }
  .kbd {
    background: #2a2a2a;
    border: 1px solid #444;
    border-radius: 3px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    padding: 1px 6px;
    color: #d3aee6;
  }

  .crop-item {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 0.8rem;
    margin-bottom: 0.6rem;
  }
  .crop-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #d3aee6;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.4rem;
  }

  .ocr-box {
    background: #111;
    border: 1px solid #d3aee6;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: #e8e8e8;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
  }

  .stButton > button {
    background: #d3aee6;
    color: #0f0f0f;
    border: none;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 0.8rem;
    padding: 0.5rem 1.2rem;
    width: 100%;
    cursor: pointer;
    transition: opacity 0.15s;
  }
  .stButton > button:hover { opacity: 0.85; }

  .stButton > button[kind="secondary"] {
    background: transparent;
    border: 1px solid #444;
    color: #aaa;
  }

  div[data-testid="stFileUploader"] {
    background: #1a1a1a;
    border: 1px dashed #333;
    border-radius: 6px;
    padding: 1rem;
  }

  .status-bar {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #666;
    padding: 0.4rem 0;
    border-top: 1px solid #1e1e1e;
    margin-top: 1rem;
  }
  .status-ok  { color: #7ec8a4; }
  .status-warn { color: #e6c46e; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────
if "crops" not in st.session_state:
    st.session_state.crops = []
if "ocr_results" not in st.session_state:
    st.session_state.ocr_results = {}

# ── Header ─────────────────────────────────────────────────────
st.markdown("""
<div class="title-block">
  <h1>kontAbil</h1>
  <p>Interactive image cropper &amp; OCR scanner</p>
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([2, 1])

# ── LEFT: canvas + upload ──────────────────────────────────────
with left_col:

    uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded:
        pil_img = Image.open(uploaded).convert("RGB")
        img_w, img_h = pil_img.size

        # Scale for display (max 800px wide)
        MAX_W = 800
        scale = min(1.0, MAX_W / img_w)
        disp_w = int(img_w * scale)
        disp_h = int(img_h * scale)

        st.markdown("**Draw a rectangle** over the region you want to crop, then click **Confirm Crop**.")

        canvas_result = st_canvas(
            fill_color="rgba(211, 174, 230, 0.15)",
            stroke_width=2,
            stroke_color="#d3aee6",
            background_image=pil_img,
            update_streamlit=True,
            width=disp_w,
            height=disp_h,
            drawing_mode="rect",
            key="canvas",
        )

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("✦ Confirm Crop"):
                if canvas_result.json_data and canvas_result.json_data["objects"]:
                    obj = canvas_result.json_data["objects"][-1]
                    x = int(obj["left"] / scale)
                    y = int(obj["top"] / scale)
                    w = int(obj["width"] / scale)
                    h = int(obj["height"] / scale)

                    if w > 5 and h > 5:
                        crop_img = pil_img.crop((x, y, x + w, y + h))
                        st.session_state.crops.append(crop_img)
                        st.success(f"Crop #{len(st.session_state.crops)} saved ({w}×{h}px)")
                    else:
                        st.warning("Selection too small — draw a larger rectangle.")
                else:
                    st.warning("No selection found — draw a rectangle on the image first.")

        with col_b:
            if st.button("↺ Reset All", type="secondary"):
                st.session_state.crops = []
                st.session_state.ocr_results = {}
                st.rerun()

        st.markdown(f'<div class="status-bar">Image: {img_w}×{img_h}px &nbsp;·&nbsp; '
                    f'Display scale: {scale:.0%} &nbsp;·&nbsp; '
                    f'<span class="status-ok">Crops saved: {len(st.session_state.crops)}</span></div>',
                    unsafe_allow_html=True)

    else:
        st.info("Upload an image above to get started.")

# ── RIGHT: tutorial + crops + OCR ─────────────────────────────
with right_col:

    # Tutorial
    st.markdown("""
    <div class="tutorial-card">
      <h4>How to use</h4>
      <div class="step"><span class="step-num">1</span>Upload a JPG or PNG image on the left.</div>
      <div class="step"><span class="step-num">2</span>Click and drag on the image to draw a crop rectangle.</div>
      <div class="step"><span class="step-num">3</span>Click <strong>Confirm Crop</strong> to save the selected region.</div>
      <div class="step"><span class="step-num">4</span>Repeat for as many regions as you need.</div>
      <div class="step"><span class="step-num">5</span>Click <strong>Run OCR</strong> on any saved crop to extract its text.</div>
      <div class="step"><span class="step-num">6</span>Click <strong>Reset All</strong> to start over.</div>
    </div>
    """, unsafe_allow_html=True)

    # Saved crops
    if st.session_state.crops:
        st.markdown("#### Saved Crops")

        for i, crop in enumerate(st.session_state.crops):
            st.markdown(f'<div class="crop-label">Crop #{i+1}</div>', unsafe_allow_html=True)
            st.image(crop, use_container_width=True)

            if st.button(f"🔍 Run OCR on Crop #{i+1}", key=f"ocr_{i}"):
                with st.spinner("Extracting text..."):
                    text = pytesseract.image_to_string(crop)
                    st.session_state.ocr_results[i] = text.strip() or "(no text detected)"

            if i in st.session_state.ocr_results:
                st.markdown(f'<div class="ocr-box">{st.session_state.ocr_results[i]}</div>',
                            unsafe_allow_html=True)

                # Download OCR text
                buf = io.BytesIO(st.session_state.ocr_results[i].encode())
                st.download_button(
                    label=f"⬇ Download text #{i+1}",
                    data=buf,
                    file_name=f"ocr_crop_{i+1}.txt",
                    mime="text/plain",
                    key=f"dl_{i}"
                )

            st.markdown("---")

        # Download all crops stacked
        if len(st.session_state.crops) > 0:
            st.markdown("#### Export")
            if st.button("⬇ Download All Crops (stacked PNG)"):
                lilac = (238, 174, 211)  # PIL is RGB
                total_h = sum(c.size[1] for c in st.session_state.crops) + 10 * (len(st.session_state.crops) - 1)
                max_w   = max(c.size[0] for c in st.session_state.crops)
                final   = Image.new("RGB", (max_w, total_h), lilac)
                y_off   = 0
                for crop in st.session_state.crops:
                    final.paste(crop, (0, y_off))
                    y_off += crop.size[1] + 10

                buf = io.BytesIO()
                final.save(buf, format="PNG")
                buf.seek(0)
                st.download_button(
                    label="Save stacked PNG",
                    data=buf,
                    file_name="all_crops_stacked.png",
                    mime="image/png"
                )
