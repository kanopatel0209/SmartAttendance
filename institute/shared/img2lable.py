import face_recognition
import cv2
import pickle, base64


def encodeProfile(file_path=None):
  image = face_recognition.load_image_file(file_path)
  rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  image_encode = face_recognition.face_encodings(rgb_image)[0]
  np_bytes = pickle.dumps(image_encode)
  np_base64 = base64.b64encode(np_bytes)
  return np_base64

def facesInImage(file_path=None, padding=50):
  image = face_recognition.load_image_file(file_path)
  rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  face_locations = face_recognition.face_locations(rgb_image)
  
  faces = []
  for loc in face_locations:
    face = image[loc[0]-padding:loc[2]+padding, loc[3]-padding:loc[1]+padding]
    rgb_face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    face_encode = face_recognition.face_encodings(rgb_face)[0]
    faces.append(face_encode)
  return faces

def compareFaces(faces, profile):
  profile = pickle.loads(base64.b64decode(profile))

  for tolerance in range(1,7):
    matches = face_recognition.compare_faces(faces, profile, tolerance/10)
    if sum(matches)==1:
      return True
  else:
    return False

