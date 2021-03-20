import tensorflow as tf
import numpy as np
slim = tf.contrib.slim

class URLCNN(object):

    def __init__(
            self, sequence_length, num_classes,
            embedding_size, filter_sizes, num_filters, l2_reg_lambda=0.0):
        # Placeholders for input, output, dropout
        self.input_x = tf.placeholder(tf.float32, [None, sequence_length, embedding_size], name="input_x")
        self.input_y = tf.placeholder(tf.float32, [None, num_classes], name="input_y")
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")

        # Keeping track of l2 regularization loss (optional)
        l2_loss = tf.constant(0.0)

        self.embedded_chars = self.input_x
        self.embedded_chars_expended = tf.expand_dims(self.embedded_chars, -1)

        # Create a convolution + maxpool layer for each filter size
        pooled_outputs = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope("conv-maxpool-%s" % filter_size):
                # Convolution layer
                filter_shape = [filter_size, embedding_size, 1, num_filters]
                W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")
                conv = tf.nn.conv2d(
                        self.embedded_chars_expended,
                        W,
                        strides=[1, 1, 1, 1],
                        padding="VALID",
                        name="conv")
                # Apply nonlinearity
                h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                # Maxpooling over the outputs
                pooled = tf.nn.max_pool(
                        h,
                        ksize=[1, sequence_length - filter_size + 1, 1, 1],
                        strides=[1, 1, 1, 1],
                        padding="VALID",
                        name="pool")
                pooled_outputs.append(pooled)

        # Combine all the pooled features
        num_filters_total = num_filters * len(filter_sizes)
        self.h_pool = tf.concat(pooled_outputs, 3)
        self.h_pool_flat = tf.reshape(self.h_pool, [-1, num_filters_total])


        epsilon = 1e-3
        with tf.name_scope("BATCH-NORM"):
            batch_mean,batch_var = tf.nn.moments(self.h_pool_flat,[0])
            scale = tf.Variable(tf.ones([384]))
            beta = tf.Variable(tf.zeros([384]))
            self.BN = tf.nn.batch_normalization(self.h_pool_flat,batch_mean,batch_var,beta,scale,epsilon)

        # Add 2-layer-MLP
        h1_units=128
        h2_units=64
        with tf.name_scope("FC-Layer-1"):
            W = tf.Variable(tf.truncated_normal(shape=[384,h1_units], stddev=0.1), name="W")
            b = tf.Variable(tf.constant(0.1, shape=[h1_units]), name="b")
            self.hidden_1 = tf.nn.relu(tf.nn.xw_plus_b(self.BN,W,b,name="fc1"))
        with tf.name_scope("FC-Layer-2"):
            W = tf.Variable(tf.truncated_normal(shape=[h1_units,h2_units], stddev=0.1), name="W")
            b = tf.Variable(tf.constant(0.1, shape=[h2_units]), name="b")
            self.hidden_2 = tf.nn.relu(tf.nn.xw_plus_b(self.hidden_1,W,b,name="hidden"))

        # Final (unnomalized) scores and predictions
        with tf.name_scope("output"):
            W = tf.get_variable(
                    "W",
                    # shape=[num_filters_total, num_classes],
                    shape=[h2_units,num_classes],
                    initializer=tf.contrib.layers.xavier_initializer())
            b = tf.Variable(tf.constant(0.1, shape=[num_classes], name="b"))
            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)
            self.scores = tf.nn.xw_plus_b(self.hidden_2, W, b, name="scores")
            self.predictions = tf.argmax(self.scores, 1, name="predictions")

        # Calculate Mean cross-entropy loss
        with tf.name_scope("loss"):
            losses = tf.nn.softmax_cross_entropy_with_logits(logits=self.scores, labels=self.input_y)
            self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

        # Accuracy
        with tf.name_scope("accuracy"):
            correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")
