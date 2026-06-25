# 🖼️ kontAbil — Interactive Image Cropper & OCR Scanner

A desktop tool for manually selecting regions from an image, stacking them, and extracting text via OCR. Built for scanning receipts and documents.

---

## ✨ Features

- Interactive crop selection with mouse drag
- Resize crop box by dragging edges or corners
- Confirm and "cut" multiple regions from the image
- Stack all crops into a single output image (lilac background)
- OCR text extraction via Tesseract

---

## 📋 Requirements

- Python 3.10+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed on your system

### Python dependencies

```
opencv-python
numpy
pytesseract
```

Install with:

```bash
pip install opencv-python numpy pytesseract
```

---

## ⚙️ Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-username/kontAbil.git
cd kontAbil
```

2. **Install dependencies**

```bash
pip install opencv-python numpy pytesseract
```

3. **Install Tesseract OCR**

Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

Then add this line to the script (after `import pytesseract`), pointing to your install path:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

4. **Set your image path**

In `NEW IMAGE EDIT APLICATIE.py`, update line 8:

```python
image = cv2.imread(r"path\to\your\image.jpg")
```

---

## ▶️ Usage

Run the script:

```bash
python "NEW IMAGE EDIT APLICATIE.py"
```

### Controls

| Key / Action | Description |
|---|---|
| **Drag** mouse | Draw a crop rectangle |
| **Drag edges/corners** | Resize the crop rectangle |
| `C` | Confirm crop — cuts it from the image and adds to stack |
| `R` | Reset — clears all crops and starts over |
| `Q` | Quit the cropper window |
| `T` (in preview) | Run OCR and print extracted text to console |
| `Q` (in preview) | Close the preview window |

### Workflow

1. A window opens with your image
2. Drag to select a region
3. Fine-tune by dragging the edges or corners of the box
4. Press `C` to confirm — the region is cut and saved
5. Repeat for all regions you want
6. Press `Q` to finish — all crops are stacked and saved as `all_crops_stacked.png`
7. A preview window opens — press `T` to extract text via OCR

---

## 📁 Output

- `all_crops_stacked.png` — all confirmed crops stacked vertically on a lilac background, saved in the working directory

---

## 🗂️ Project Structure

```
kontAbil/
├── NEW IMAGE EDIT APLICATIE.py   # Main script
├── all_crops_stacked.png         # Output (generated after use)
└── README.md
```

---

## 🌐 Live Demo

Try it directly in your browser — no installation needed:

👉 **[https://image-ocr-ycen.onrender.com](https://image-ocr-ycen.onrender.com)**

> Note: The app may take ~30 seconds to wake up if it has not been used recently (free tier).

---

## 🔧 Known Issues

- The image path is currently hardcoded — update it before running
- `cv2.imshow()` does not work in Jupyter Notebook; run as a regular Python script
- Tesseract path must be configured manually on Windows

---

## 📄 License

MIT License — free to use and modify.
