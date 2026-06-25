# 🖼️ kontAbil — Interactive Image Cropper & OCR Scanner

A web tool for manually selecting regions from an image and extracting text via OCR. Built for scanning receipts and documents.

---

## 🌐 Live Demo

Try it directly in your browser — no installation needed:

👉 **[https://imageocr-vcp4etrywnxtivdua8bt3r.streamlit.app/](https://imageocr-vcp4etrywnxtivdua8bt3r.streamlit.app/)**

---

## ✨ Features

- Upload any JPG or PNG image
- Interactive crop selection with draggable handles
- Save multiple crops in one session
- OCR text extraction via Tesseract
- Download extracted text or all crops as a stacked PNG

---

## 📋 How to Use

1. Upload a JPG or PNG image
2. Drag the handles on the image to select a region
3. Click **Confirm Crop** to save the selected region
4. Repeat for as many regions as you need
5. Click **Run OCR** on any saved crop to extract its text
6. Click **Reset All** to start over

---

## 🗂️ Project Structure

```
Image_OCR/
├── app.py               # Streamlit web app
├── requirements.txt     # Python dependencies
├── packages.txt         # System dependencies (Tesseract)
├── runtime.txt          # Python version
└── README.md
```

---

## ⚙️ Run Locally

1. **Clone the repository**

```bash
git clone https://github.com/BreadPete/Image_OCR.git
cd Image_OCR
```

2. **Install Tesseract OCR**

Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

Then add this line to `app.py` after `import pytesseract`:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

3. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the app**

```bash
streamlit run app.py
```

---

## 📁 Output

- **Stacked PNG** — all confirmed crops stacked vertically on a lilac background
- **OCR text** — extracted text from each crop, downloadable as `.txt`

---

## 📄 License

MIT License — free to use and modify.
