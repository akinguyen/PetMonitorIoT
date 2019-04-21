# pip install --upgrade google-cloud-vision

import argparse
import numpy as np
import cv2


def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations
    
    print(objects)
    

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

w, h = (26, 26)
while True:
    ret, frame = cap.read()
    #original = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow("video", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite("fish.jpg", frame)
        localize_objects("fish.jpg")


cap.release()
cv2.destroyAllWindows()

#localize_objects(img)

# When everything done, release the capture
#cap.release()
#cv2.destroyAllWindows()



"""
print('Number of objects found: {}'.format(len(objects)))
for object_ in objects:
    print('\n{} (confidence: {})'.format(object_.name, object_.score))
    print('Normalized bounding polygon vertices: ')
    for vertex in object_.bounding_poly.normalized_vertices:
        print(' - ({}, {})'.format(vertex.x, vertex.y))
"""
        
# Insert into db

'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('path')

    args = parser.parse_args()
    
    localize_objects(args.path) '''