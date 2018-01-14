from moviepy.editor import VideoFileClip
from os.path        import exists, splitext
from scipy.misc     import imsave
from os             import makedirs, listdir
import numpy as np
import cv2
       

CONFIDENCE_THRESHOLD = 0.7
CAFFE_PROTOTYPE      = 'models/mobilenet_ssd.prototxt'
CAFFE_MODEL          = 'models/mobilenet_ssd.caffemodel'


class ClassesFromVideos(object):

    def __init__(self):
        self.__count = 0
        self.__caffe = cv2.dnn.readNetFromCaffe(CAFFE_PROTOTYPE, CAFFE_MODEL)

    def __detect(self, class_name, image):
        if len(image.shape) == 3 and image.shape[2] == 3:
            h, w    = image.shape[:2]
            resized = cv2.resize(image, (300,300))
            scaled  = cv2.dnn.blobFromImage(
                resized,
                0.007843,
                (300,300), 
                127.5
            )
            self.__caffe.setInput(scaled)
            cats = self.__caffe.forward()
            for i in np.arange(0, cats.shape[2]):
                if cats[0,0,i,2] > CONFIDENCE_THRESHOLD and cats[0,0,i,1] == 8:
                    bounds  = cats[0,0,i,3:7] * np.array([w,h,w,h])
                    a,b,c,d = bounds.astype(np.int)
                    image   = image[a:c,b:d]
                    if image.shape[0]>127 and image.shape[1]>127:
                        save_name = 'data/{}/{}.png'.format(class_name, self.__count)
                        imsave(save_name, image)
                        self.__count += 1

    def generate(self):
        dirlist     = listdir('videos')
        video_names = [f for f in dirlist if 'mp4' in f]
        for video_name in video_names:
            class_name = splitext(video_name)[0]
            class_name = ''.join(i for i in class_name if not i.isdigit())
            if not exists('data/{}'.format(class_name)):
                makedirs('data/{}'.format(class_name))
            video_file = 'videos/{}'.format(video_name)
            for frame in VideoFileClip(video_file).iter_frames():
                self.__detect(class_name, frame)

