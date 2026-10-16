import cv2

def instagram_crop(image, mode="portrait"):
    h, w = image.shape[:2]

    if mode == "portrait":      # 4:5
        target_ratio = 4 / 5
    elif mode == "square":      # 1:1
        target_ratio = 1
    else:                       # landscape
        target_ratio = 1.91

    current_ratio = w / h

    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        x1 = (w - new_w) // 2
        return image[:, x1:x1+new_w]
    else:
        new_h = int(w / target_ratio)
        y1 = (h - new_h) // 2
        return image[y1:y1+new_h, :]
