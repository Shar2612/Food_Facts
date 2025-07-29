import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from gtts import gTTS
from playsound import playsound
import os


def speech(text):
    print(text)
    language = "en"
    output = gTTS(text=text, lang=language, slow=False)

    if not os.path.exists("./sounds"):
        os.makedirs("./sounds")

    output_path = "./sounds/output.mp3"
    output.save(output_path)
    playsound(output_path)


video = cv2.VideoCapture(0)
labels = []

try:
    while True:
        ret, frame = video.read()
        if not ret:
            break

        bbox, label, conf = cv.detect_common_objects(frame)
        output_image = draw_bbox(frame, bbox, label, conf)
        cv2.imshow("Detection", output_image)

        for item in label:
            if item not in labels:
                labels.append(item)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    video.release()
    cv2.destroyAllWindows()

new_sentence = []
for i, label in enumerate(labels):
    if i == 0:
        new_sentence.append(f"I found a {label}, and, ")
    else:
        new_sentence.append(f"a {label},")

speech(" ".join(new_sentence))
speech("Here are the food facts I found for these items:")

for label in labels:
    try:
        print(f"\n\t{label.title()}")
        food_facts(label)
    except Exception as e:
        print(f"No food facts for this item: {e}")
