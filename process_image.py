import cv2

def detect_deforestation(image_path):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = (35, 40, 40)
    upper_green = (85, 255, 255)

    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_pixels = cv2.countNonZero(mask)

    total_pixels = img.shape[0] * img.shape[1]
    green_percent = (green_pixels / total_pixels) * 100

    deforested_percent = 100 - green_percent
    deforested_area = round((deforested_percent / 100) * 1000, 2)  # Assume 1000 sq.km base area

    return round(deforested_area, 2), round(deforested_percent, 2)

# ✅ This block should be OUTSIDE the function
if __name__ == "__main__":
    test_image = "static/uploads/sample.jpg"  # Make sure this path exists
    area, percent = detect_deforestation(test_image)
    print(f"Deforested Area: {area} sq.km")
    print(f"Deforested Percentage: {percent}%")
