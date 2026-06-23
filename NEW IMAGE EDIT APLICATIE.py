import cv2
import numpy as np
import os
import platform
import subprocess


image = cv2.imread(r"F:\wrk\IMAGE SCANNER\bonScan\4.JPEG")
clone = image.copy()
display = image.copy()

cropping = False
resizing = False
resize_edge = None  # "left", "right", "top", "bottom"
start_point = None
temp_crop = None

stacked_crops = []
total_height = 0
max_width = 0

# Sensitivity radius for grabbing edges
EDGE_SENSITIVITY = 10

def is_near(val1, val2):
    return abs(val1 - val2) < EDGE_SENSITIVITY

def get_edge(x, y, crop):
    cx, cy, cw, ch = crop
    right = cx + cw
    bottom = cy + ch

    # Prioritize corners
    if is_near(x, cx) and is_near(y, cy): return "top-left"
    if is_near(x, right) and is_near(y, cy): return "top-right"
    if is_near(x, cx) and is_near(y, bottom): return "bottom-left"
    if is_near(x, right) and is_near(y, bottom): return "bottom-right"

    # Then allow edge resizing
    if is_near(x, cx): return "left"
    if is_near(x, right): return "right"
    if is_near(y, cy): return "top"
    if is_near(y, bottom): return "bottom"
    return None

def adjust_crop(x, y):
    global temp_crop
    cx, cy, cw, ch = temp_crop
    right = cx + cw
    bottom = cy + ch

    if resize_edge == "left":
        new_x = min(x, right - 1)
        temp_crop = (new_x, cy, right - new_x, ch)
    elif resize_edge == "right":
        temp_crop = (cx, cy, max(1, x - cx), ch)
    elif resize_edge == "top":
        new_y = min(y, bottom - 1)
        temp_crop = (cx, new_y, cw, bottom - new_y)
    elif resize_edge == "bottom":
        temp_crop = (cx, cy, cw, max(1, y - cy))

    elif resize_edge == "top-left":
        new_x = min(x, right - 1)
        new_y = min(y, bottom - 1)
        temp_crop = (new_x, new_y, right - new_x, bottom - new_y)

    elif resize_edge == "top-right":
        new_y = min(y, bottom - 1)
        temp_crop = (cx, new_y, max(1, x - cx), bottom - new_y)

    elif resize_edge == "bottom-left":
        new_x = min(x, right - 1)
        temp_crop = (new_x, cy, right - new_x, max(1, y - cy))

    elif resize_edge == "bottom-right":
        temp_crop = (cx, cy, max(1, x - cx), max(1, y - cy))

def draw_temp_crop():
    global display, temp_crop
    display = clone.copy()
    if temp_crop:
        x, y, w, h = temp_crop
        cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)

def mouse_crop(event, x, y, flags, param):
    global cropping, start_point, temp_crop, resizing, resize_edge

    if event == cv2.EVENT_LBUTTONDOWN:
        if temp_crop:
            edge = get_edge(x, y, temp_crop)
            if edge:
                resizing = True
                resize_edge = edge
                return
        start_point = (x, y)
        cropping = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            x0, y0 = start_point
            x_min, y_min = min(x0, x), min(y0, y)
            x_max, y_max = max(x0, x), max(y0, y)
            temp_crop = (x_min, y_min, x_max - x_min, y_max - y_min)
            draw_temp_crop()
        elif resizing and temp_crop:
            adjust_crop(x, y)
            draw_temp_crop()

    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False
        resizing = False
        resize_edge = None

cv2.namedWindow("Select Crops (drag box, c=confirm, r=reset, q=quit)")
cv2.setMouseCallback("Select Crops (drag box, c=confirm, r=reset, q=quit)", mouse_crop)

while True:
    cv2.imshow("Select Crops (drag box, c=confirm, r=reset, q=quit)", display)
    key = cv2.waitKey(1)

    if key == ord("r"):
        clone = image.copy()
        display = clone.copy()
        stacked_crops.clear()
        total_height = 0
        max_width = 0
        temp_crop = None

    elif key == ord("c") and temp_crop:
        x, y, w, h = temp_crop
        crop = clone[y:y+h, x:x+w].copy()
        clone[y:y+h, x:x+w] = 255  # white-out cut
        stacked_crops.append(crop)
        total_height += h + 10
        max_width = max(max_width, w)
        temp_crop = None
        draw_temp_crop()

    elif key == ord("q"):
        break

cv2.destroyAllWindows()

if stacked_crops:
    lilac_color = (211, 174, 238)
    final = np.full((total_height - 10, max_width, 3), lilac_color, dtype=np.uint8)
    y_offset = 0
    for crop in stacked_crops:
        h, w = crop.shape[:2]
        final[y_offset:y_offset+h, 0:w] = crop
        y_offset += h + 10

    output_path = "all_crops_stacked.png"
    cv2.imwrite(output_path, final)
    print(f"Saved: {output_path}")

    # === OCR viewer section ===
    preview = cv2.imread(output_path)
cv2.imshow("Final Cropped Output (press 't' to OCR, 'q' to quit)", preview)

import pytesseract
while True:
    key = cv2.waitKey(0)
    if key == ord('t'):
        text = pytesseract.image_to_string(preview)
        print("\n🔍 OCR Text Extracted from Final Image:\n")
        print(text.strip())
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
