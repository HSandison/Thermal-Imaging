import cv2
import numpy as np

# Constants
RECT_WIDTH = 501
RECT_HEIGHT = 378
RECT_STEP = 10

# Global variables
drawing = False
top_left_pt = None

# Callback function for mouse events
def mouse_callback(event, x, y, flags, param):
    global top_left_pt, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        top_left_pt = (x, y)
        drawing = True

def draw_rectangle(image, top_left_pt):
    cv2.rectangle(image, top_left_pt, (top_left_pt[0] + RECT_WIDTH, top_left_pt[1] + RECT_HEIGHT), (0, 255, 0), 2)

# Load the visible image
visible_image = cv2.imread('C:/PETRAS/Overlay/visible_image.jpg')

# Load the thermal image
thermal_image = cv2.imread('C:/PETRAS/Overlay/thermal_image.jpg')

# Create windows to display the images
cv2.namedWindow('Visible Image')
cv2.namedWindow('Thermal Image')
cv2.setMouseCallback('Visible Image', mouse_callback)

while True:
    # Display the visible image
    display_visible_image = visible_image.copy()

    # Draw the rectangle if top left point is selected
    if drawing:
        draw_rectangle(display_visible_image, top_left_pt)

    cv2.imshow('Visible Image', display_visible_image)
    cv2.imshow('Thermal Image', thermal_image)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # Exit the loop if 'q' is pressed
    if key == ord('q'):
        break

    # Crop the image and display it in a separate window if rectangle selection is complete
    if drawing and key == ord('c'):
        cropped_image = visible_image[top_left_pt[1]:top_left_pt[1] + RECT_HEIGHT, top_left_pt[0]:top_left_pt[0] + RECT_WIDTH]

        # Resize the cropped image to match the size of the thermal image
        resized_cropped_image = cv2.resize(cropped_image, (thermal_image.shape[1], thermal_image.shape[0]))
        cv2.imshow('Resized cropped image', resized_cropped_image)

        # Overlay the resized cropped image onto the thermal image
        overlay_image = cv2.addWeighted(thermal_image, 0.5, resized_cropped_image, 0.5, 0)

        cv2.imshow('Overlay Image', overlay_image)
        cv2.imwrite('overlay.jpg', overlay_image)
        drawing = False

    # Adjust the size of the rectangle
    if drawing and key == ord('w'):
        RECT_WIDTH += RECT_STEP
        RECT_HEIGHT = int(RECT_WIDTH * (240 / 320))
    elif drawing and key == ord('s'):
        RECT_WIDTH -= RECT_STEP
        RECT_HEIGHT = int(RECT_WIDTH * (240 / 320))

# Clean up
cv2.destroyAllWindows()
