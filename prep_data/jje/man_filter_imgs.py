import os
import cv2

# replace with the actual path to the images directory
path = "Pinterest"

'''
Manually Filter Images

when compiling a set of images, make sure you know what criteria you are using
Example - looking for images that will go in the 'yes' directory

Run this file

If the image does not meet the 'yes' criteria,
Press 'd' to delete the image

If the image meets the 'yes' criteria,
Press 's' to skip the image so it won't be deleted

When you have filtered all images in the directory,
move the resulting images to the directory that you specified to use for training/testing data
'''

for filename in os.listdir(path):
    if filename.endswith(".jpg"):
        print("Current File: " + filename)
        img = cv2.imread(os.path.join(path, filename))
        cv2.namedWindow(filename, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        cv2.imshow(filename, img)
        cv2.moveWindow(filename, 0, 0)
        key = cv2.waitKey(0)
        if key == 27: # escape key
            cv2.destroyAllWindows()
            break
        elif key == ord('d'): # 's' key
            os.remove(os.path.join(path, filename))
            print("               Deleted: " + filename)
        elif key == ord('s'): # 'p' key
            pass
        cv2.destroyAllWindows()