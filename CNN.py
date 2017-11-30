from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import tensorflow as tf
import csv
import numpy as np
import random

##########################################################
## Read feature corrosponding data
Feature = np.zeros( (12029,4))
Label = np.zeros( (12029,2))
f = open('hack_training_done.csv', 'r')
count = 0
## Read the features, normaolize them, and create label
for row in csv.DictReader(f):
    if row["Login_count"] == "NULL":
        Feature[(count,0)] = 0
    else: Feature[(count,0)] = row["Login_count"]
    if row["Video_watch_count"] == "NULL":
        Feature[(count,1)] = 0
    else: Feature[(count,1)] = row["Video_watch_count"]
    if row["Video_complete_rate"] == "NULL":
        Feature[(count,2)] = 0
    else: Feature[(count,2)] = row["Video_complete_rate"]
    if row["Video_watch_time"] == "NULL":
        Feature[(count,3)] = 0
    else: Feature[(count,3)] = row["Video_watch_time"]
    if row["target"] == 'T':
        Label[(count,0)] = 1
    else:
        Label[(count,1)] = 1
    count += 1
## Normalize
Feature = Feature / Feature.max(axis = 0)
f.close()

AnswerFeature = np.zeros((3560,4))
count2 = 0
g = open('hack_question02_done.csv', 'r')

for row in csv.DictReader(g):
    if row["Login_count"] == "NULL": AnswerFeature[(count2,0)] = 0
    else: AnswerFeature[(count2,0)] = row["Login_count"]
    if row["Video_watch_count"] == "NULL": AnswerFeature[(count2,1)] = 0
    else: AnswerFeature[(count2,1)] = row["Video_watch_count"]
    if row["Video_complete_rate"] == "NULL": AnswerFeature[(count2,2)] = 0
    else: AnswerFeature[(count2,2)] = row["Video_complete_rate"]
    if row["Video_watch_time"] == "NULL": AnswerFeature[(count2,3)] = 0
    else: AnswerFeature[(count2,3)] = row["Video_watch_time"]
    count2 += 1
        
AnswerFeature = AnswerFeature / AnswerFeature.max(axis = 0)
g.close()
##########################################################

FLAGS = None

def deepnn(x):
  x_image = tf.reshape(x, [-1, 1, 1, 4])

  # First convolutional layer
  W_conv1 = weight_variable([1, 1, 4, 64])
  b_conv1 = bias_variable([64])
  h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

  # Second convolutional layer
  W_conv2 = weight_variable([1, 1, 64, 256])
  b_conv2 = bias_variable([256])
  h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2) + b_conv2)
  
  #Third convolutional layer
  W_conv3 = weight_variable([1, 1, 256, 512])
  b_conv3 = bias_variable([512])
  h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3) + b_conv3)
  
  #Fourth concolutional Layer
#  W_conv4 = weight_variable([1, 1, 512, 1024])
#  b_conv4 = bias_variable([1024])
#  h_conv4 = tf.nn.relu(conv2d(h_conv3, W_conv4) + b_conv4)

  # Fully connected layer 1
  W_fc1 = weight_variable([1*1* 512, 1024])
  b_fc1 = bias_variable([1024])
  h_pool2_flat = tf.reshape(h_conv3, [-1, 1*1*512])
  h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

  # Dropout
  keep_prob = tf.placeholder(tf.float32)
  h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

  # Map the 1024 features to 2 classes, for T and F
  W_fc2 = weight_variable([1024, 2])
  b_fc2 = bias_variable([2])
  y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
  return y_conv, keep_prob


def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def main(_):
  # Import data
  x = tf.placeholder(tf.float32, [None, 4])
  x_answer = tf.placeholder(tf.float32, [None, 4])
  y_ = tf.placeholder(tf.float32, [None, 2])
  y_conv, keep_prob= deepnn(x)

  cross_entropy = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
  train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
  ## tf.argmax: Returns the index with the largest value across axes of a tensor.
  correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
  AnswerPredicted = tf.argmax(y_conv, 1)
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(10000):
        if i % 100 == 0:
            RandomIndex = random.sample(range(1,12029), 1000)
            train_accuracy = accuracy.eval(feed_dict = { x: Feature[RandomIndex, :], y_: Label[RandomIndex, :], keep_prob: 1.0})
            print('step %d, training accuracy %g' % (i, train_accuracy))
        train_step.run(feed_dict={x:Feature[RandomIndex, :], y_:Label[RandomIndex, :], keep_prob: 0.5})
    AnswerCSV = AnswerPredicted.eval(feed_dict = {x:AnswerFeature, keep_prob: 1.0})
    with open('tmp.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(AnswerCSV)
    print('test accuracy %g' % accuracy.eval(feed_dict={x: Feature, y_:Label, keep_prob: 1.0}))
    
    
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', type=str,
                      default='/tmp/tensorflow/mnist/input_data',
                      help='Directory for storing input data')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)