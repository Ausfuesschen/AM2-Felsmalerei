import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import imageio
from sklearn import datasets

#sess = tf.Session()

#iris = datasets.load_iris()
image_file = 'MEC.jpg'

image = imageio.imread('MEC.jpg')
print(image.shape)

#sess = tf.Session()

#tf.global_variables_initializer()

#coord = tf.train.Coordinator()
#threads = tf.train.start_queue_runners(coord=coord)

#image_tensor = sess.run([image])
#print(image_tensor)

#coord.request_stop()
#coord.join(threads)

print('Hello!')
