# Crop clothes from images
import os
import cv2

CLASSIFIER_FILENAME = './data/haarcascades/haarcascade_frontalface_default.xml'
FACE_CASCADE = cv2.CascadeClassifier(CLASSIFIER_FILENAME)

INPUT_DIR = './data/clothes/input/'
OUTPUT_DIR = './data/clothes/output/'


def find_faces(img):
    """
    :param img:
    :return: [(x, y, w, h)]
    """
    if img is None:
        raise ValueError("img should not be NONE")

    if FACE_CASCADE.empty():
        raise ValueError("Failed to load classifier file!")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return FACE_CASCADE.detectMultiScale(gray, 1.3, 6)


def find_clothes(faces):
    """
    :param faces:
    :return: [(cx, cy, cw, ch)]
    """
    clothes = []
    for face in faces:
        fx, fy, fw, fh = face
        cw = fw * 3.5
        ch = fh * 3.5
        cx = fx + fw/2 - cw/2
        cy = fy + fh
        clothes.append([cx, cy, cw, ch])
    return clothes


def save_clothes(output_dir, ori_filename, ori_img, clothes):
    if ori_img is None:
        raise ValueError("ori_img should not be NONE")

    if not clothes:
        print "clothes is empty!"
        return

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    for i, cloth in enumerate(clothes):
        cloth = [int(x) for x in cloth]
        cx, cy, cw, ch = cloth
        clo = ori_img[cy:cy+ch, cx:cx+cw]
        output_filename = "%s_%d.jpg" % (output_dir + ori_filename[:-4], i)
        cv2.imwrite(output_filename, clo)
        print "Saved result in %s" % output_filename


def main():
    filenames = os.listdir(INPUT_DIR)
    # filenames = ['timg.jpg']
    for filename in filenames:
        if not filename.endswith('.jpg'):
            continue
        print "processing %s" % INPUT_DIR + filename

        img = cv2.imread(INPUT_DIR + filename)
        faces = find_faces(img)
        print "find %d face(s)" % len(faces)

        clothes = find_clothes(faces)
        save_clothes(OUTPUT_DIR, filename, img, clothes)

        # check one specific image by its file name
        if filename == 'timg.jpg':
            display_img = img.copy()
            x, y, w, h = faces[0]
            cv2.rectangle(display_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cx, cy, cw, ch = [int(x) for x in clothes[0]]
            cv2.rectangle(display_img, (cx, cy), (cx+cw, cy+ch), (0, 255, 0), 2)
            cv2.imshow('img', display_img)
            cv2.moveWindow('img', 20, 20)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
