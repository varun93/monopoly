import tensorflow as tf

class Neural_Network:

	def __init__(self):
		self.feedforward()
		self.backforward()
		self.reset_graph()

	def reset_graph(self):
		tf.reset_default_graph()

	def feedforward(self):
		# These lines establish the feed-forward part of the network used to choose actions
		inputs1 = tf.placeholder(shape=[1, 23], dtype=tf.float32)
		W = tf.Variable(tf.random_uniform([23, 3], 0, 0.01))
		Qout = tf.matmul(inputs1, W)
		predict = tf.argmax(Qout, 1)

	def backforward(self):
		# Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
		nextQ = tf.placeholder(shape=[1, 3], dtype=tf.float32)
		loss = tf.reduce_sum(tf.square(nextQ - Qout))
		trainer = tf.train.GradientDescentOptimizer(learning_rate=0.2)
		updateModel = trainer.minimize(loss)