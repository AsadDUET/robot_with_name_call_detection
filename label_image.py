# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
#
#from __future__ import absolute_import
#from __future__ import division
#from __future__ import print_function

import argparse
import sys
import time
import picamera
import numpy as np
import tensorflow as tf
#import cv2


file_name ="foo.jpg"
model_file = "output_graph.pb"
label_file = "output_labels.txt"
input_height = 224
input_width = 224
input_mean = 128
input_std = 128
input_layer = "input"
output_layer = "final_result"


def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()
  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)
  return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)


#  image_reader=cv2.imread('potato_late_blight/42451eb3-fb45-4b9a-8dd3-c9b9aa3a29c8___RS_LB 4340.JPG')
#  image_reader=tf.constant(image_reader)

  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')

  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
#  sess = tf.Session()

  return normalized

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

#
#def result(data):
#    if data[0]=='p':
#        plant ='আলু'
#    else:
#        plant = 'টমেটো'


graph = load_graph(model_file)
def start_process():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 1024)
        camera.start_preview()
        time.sleep(2)
        camera.capture('foo.jpg')
    start = time.time()
    with tf.Session(graph=graph) as sess:
        t = read_tensor_from_image_file(file_name,
                                        input_height=input_height,
                                        input_width=input_width,
                                        input_mean=input_mean,
                                        input_std=input_std)
        t = sess.run(t)
        input_name = "import/" + input_layer
        output_name = "import/" + output_layer
        input_operation = graph.get_operation_by_name(input_name);
        output_operation = graph.get_operation_by_name(output_name);
        results = sess.run(output_operation.outputs[0],
                          {input_operation.outputs[0]: t})
        end=time.time()
        results = np.squeeze(results)
        top_k = results.argsort()[-5:][::-1]
        labels = load_labels(label_file)

        print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))
        #return 10
#        template = "{} (score={:0.5f})"
#        for i in top_k:
#            print(template.format(labels[i], results[i]))
        #print(labels[top_k[0]])
        if results[top_k[0]]>=0.4:
            if top_k[0]==0:
                return 'আলু','আগাম ধ্বসা'
            if top_k[0]==1:
                return 'আলু','সুস্থ'
            if top_k[0]==2:
                return 'আলু','নাবী ধ্বসা'
        else:
            return 'unknown'




if __name__=='__main__':
    start_process()
    start_process()
