"""
SOURCES:
    • https://github.com/googlecreativelab/teachablemachine-community/issues/55#issuecomment-560447633
    • https://teachablemachine.withgoogle.com/train/image (teachable machine syntax)
    • https://stackoverflow.com/questions/1614059/how-to-make-python-speak/50195835#50195835
"""

def main(filename, messages=[]):
  import pyttsx3
  engine = pyttsx3.init()
  import cv2
  import tensorflow.keras
  import numpy as np

  data_for_model = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
  model = tensorflow.keras.models.load_model(filename)
  cv2.namedWindow("Camera Preview")
  vc = cv2.VideoCapture(0)

  def image_resize(image, height, inter = cv2.INTER_AREA):
      dim = None
      (h, w) = image.shape[:2]
      r = height / float(h)
      dim = (int(w * r), height)
      resized = cv2.resize(image, dim, interpolation = inter)
      return resized

  def cropTo(img):
      size = 224
      height, width = img.shape[:2]

      sideCrop = (width - 224) // 2
      return img[:,sideCrop:(width - sideCrop)]

  if vc.isOpened():
      status, frame = vc.read()
  else:
      status = False

  while status:
      key = cv2.waitKey(20)
      if key == 27:
          break
      cv2.imshow("Camera Preview", frame)
      status, frame = vc.read()
      img = frame
      img = image_resize(img, height=224)
      img = cropTo(img)
      img = cv2.flip(img, 1)
      normalized_img = (img.astype(np.float32) / 127.0) - 1
      data_for_model[0] = normalized_img
      prediction = model.predict(data_for_model)
      prediction = prediction.tolist()
      prediction = prediction[0]
      prediction1 = max(prediction)
      listindex = prediction.index(prediction1)
      message = messages[listindex]
      engine.say(message)
      engine.runAndWait()