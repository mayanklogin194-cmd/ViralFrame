import cv2

def draw_text_safe_zone(image):
    h, w = image.shape[:2]

    top = int(0.15 * h)
    bottom = int(0.85 * h)
    left = int(0.1 * w)
    right = int(0.9 * w)

    overlay = image.copy()

    cv2.rectangle(
        overlay,
        (left, top),
        (right, bottom),
        (0, 255, 0),
        3
    )

    return overlay
