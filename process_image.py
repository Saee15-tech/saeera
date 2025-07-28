import cv2

def detect_deforestation(image_path):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = (35, 40, 40)
    upper_green = (85, 255, 255)

    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_pixels = cv2.countNonZero(mask)

    total_pixels = img.shape[0] * img.shape[1]
    non_green_pixels = total_pixels - green_pixels

    deforested_area = round((non_green_pixels / total_pixels) * 100, 2)
    percentage = round(deforested_area, 2)

    return deforested_area, percentage
