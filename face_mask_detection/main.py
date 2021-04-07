import cv2 as cv
import os
import RPi_I2C_driver
import RPi.GPIO as GPIO
import tempfile

from time import sleep
from gpiozero import Button, LED

from tensorflow.keras.models import load_model


GPIO_PINS = {
    'red_led': 19,
    'green_led': 26,
    'button': 4,
}

CONFIDENCE = 0.8  # 80%


def capture_image():
    cap = cv.VideoCapture(0)
    _, frame = cap.read()

    # write frame to disk
    img_fp = None
    with tempfile.NamedTemporaryFile(suffix-'.png', delete=False) as fp:
        print(f"Image file path: {img_fp}")
        img_fp = fp.name
        cv.imwrite(img_fp, frame)

    cap.release()

    return img_fp


def detect_face_mask(img_fp):
    # load serialized face detector model from disk
    print("[INFO] loading face detector model...")
    prototxt_path = os.path.sep.join(["face_detector", "deploy.prototxt"])
    weights_path = os.path.sep.join(["face_detector",
        "res10_300x300_ssd_iter_140000.caffemodel"])
    net = cv.dnn.readNet(prototxt_path, weights_path)

    # load the face mask detector model from disk
    print("[INFO] loading face mask detector model...")
    model = load_model("face_mask_detector.model")

    # load the input image from disk, clone it, and grab the image spatial
    # dimensions
    image = cv.imread(img_fp)
    orig = image.copy()

    # construct a blob from the image
    blob = cv.dnn.blobFromImage(
        image, 1.0, (300, 300), (104.0, 177.0, 123.0)
    )

    # pass the blob through the network and obtain the face detections
    print("[INFO] computing face detections...")
    net.setInput(blob)
    detections = net.forward()

    mask_detected = False

    # loop over the detections
    for i in range(detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        if confidence > CONFIDENCE:
            mask_detected = True

    return mask_detected


def main():
    try:
        # initialize sensors and output modules
        lcd = RPi_I2C_driver.lcd()
        red_led = LED(GPIO_PINS['red_led'])
        green_led = LED(GPIO_PINS['green_led'])
        button = Button(GPIO_PINS['button'])

        while True:
            # wait for button to be pressed to take image
            button.wait_for_press()

            # capture image from camera
            img_fp = capture_image()

            # detect if person has face mask or not
            mask_detected = detect_face_mask(img_fp)

            if mask_detected:
                # flash green led and display on LCD
                lcd.lcd_display_string("Access granted!", 1)
                green_led.on()
                sleep(3)
                lcd.lcd_clear()
                green_led.off()
            else:
                # flash red led and display on LCD
                lcd.lcd_display_string("Access denied!", 1)
                red_led.on()
                sleep(3)
                lcd.lcd_clear()
                red_led.off()

    except KeyboardInterrupt:
        print("[INFO] Terminating")


if __name__ == "__main__":
    main()
