import math
import cv2
import numpy as np
import tensorflow as tf
from scipy import ndimage
import os

from MNIST_data import input_data


class Recognizer:
    def __init__(self):
        pass

    @staticmethod
    def shift(img, sx, sy):
        rows, cols = img.shape
        M = np.float32([[1, 0, sx], [0, 1, sy]])
        shifted = cv2.warpAffine(img, M, (cols, rows))
        return shifted

    @staticmethod
    def getBestShift(img):
        cy, cx = ndimage.measurements.center_of_mass(img)
        rows, cols = img.shape
        shiftx = np.round(cols / 2.0 - cx).astype(int)
        shifty = np.round(rows / 2.0 - cy).astype(int)
        return shiftx, shifty

    def TrainRecognizer(self):
        mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
        self.x = tf.placeholder("float", [None, 784])
        # we need our weights for our neural net
        W = tf.Variable(tf.zeros([784, 10]))
        # and the biases
        b = tf.Variable(tf.zeros([10]))
        self.y = tf.nn.softmax(tf.matmul(self.x, W) + b)
        self.y_ = tf.placeholder("float", [None, 10])
        cross_entropy = -tf.reduce_sum(self.y_ * tf.log(self.y))
        train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
        init = tf.initialize_all_variables()
        self.sess = tf.Session()
        self.sess.run(init)
        # use 1000 batches with a size of 100 each to train our net
        for i in range(10000):
            batch_xs, batch_ys = mnist.train.next_batch(100)
            # run the train_step function with the given image values (x) and the real output (y_)
            self.sess.run(train_step, feed_dict={self.x: batch_xs, self.y_: batch_ys})
        correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(self.y_, 1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        # print('Probability: ' + str(self.sess.run(self.accuracy, feed_dict={self.x: mnist.test.images,
                                                                        # self.y_: mnist.test.labels})))

    def TestRecognizer(self, directory, images_list):
        # create an array where we can store our 4 pictures
        images = np.zeros((len(images_list), 784))
        # and the correct values
        correct_vals = np.zeros((len(images_list), 10))
        index = 0
        # we want to test our images which you saw at the top of this page
        for no in images_list:
            # read the image
            gray = cv2.imread(directory + '\\' + no, cv2.IMREAD_GRAYSCALE)
            os.remove(directory + '\\' + no)
            # resize the images and invert it (black background)
            gray = cv2.resize(255 - gray, (28, 28))
            (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            while np.sum(gray[0]) == 0:
                gray = gray[1:]
            while np.sum(gray[:, 0]) == 0:
                gray = np.delete(gray, 0, 1)
            while np.sum(gray[-1]) == 0:
                gray = gray[:-1]
            while np.sum(gray[:, -1]) == 0:
                gray = np.delete(gray, -1, 1)
            rows, cols = gray.shape
            if rows > cols:
                factor = 20.0 / rows
                rows = 20
                cols = int(round(cols * factor))
                gray = cv2.resize(gray, (cols, rows))
            else:
                factor = 20.0 / cols
                cols = 20
                rows = int(round(rows * factor))
                gray = cv2.resize(gray, (cols, rows))
            colsPadding = (int(math.ceil((28 - cols) / 2.0)), int(math.floor((28 - cols) / 2.0)))
            rowsPadding = (int(math.ceil((28 - rows) / 2.0)), int(math.floor((28 - rows) / 2.0)))
            gray = np.lib.pad(gray, (rowsPadding, colsPadding), 'constant')
            shiftx, shifty = self.getBestShift(gray)
            shifted = self.shift(gray, shiftx, shifty)
            gray = shifted
            # save the processed images
            # cv2.imwrite(directory + '\\' + 'changed'+no, gray)
            """
            all images in the training set have an range from 0-1
            and not from 0-255 so we divide our flatten images
            (a one dimensional vector with our 784 pixels)
            to use the same 0-1 based range
            """
            flatten = gray.flatten() / 255.0
            """
            we need to store the flatten image and generate
            the correct_vals array
            correct_val for the first digit (9) would be
            [0,0,0,0,0,0,0,0,0,1]
            """
            images[index] = flatten
            # correct_val = np.zeros((10))
            # correct_val[no] = 1
            # correct_vals[index] = correct_val
            index += 1
        """
        the prediction will be an array with four values,
        which show the predicted number
        """
        prediction = tf.argmax(self.y, 1)
        """
        we want to run the prediction and the accuracy function
        using our generated arrays (images and correct_vals)
        """
        return self.sess.run(prediction, feed_dict={self.x: images})
        # print(self.sess.run(self.accuracy, feed_dict={self.x: images, self.y_: correct_vals}))


if __name__ == '__main__':
    recognizer = Recognizer()
    recognizer.TrainRecognizer()
    print(recognizer.TestRecognizer('Images', ['5.png']))
