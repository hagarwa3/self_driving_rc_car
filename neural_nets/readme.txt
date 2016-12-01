Use training_collect.py to collect training images and tag them with the user-provided "correct" direction for the car to go in each image. This creates a training set so a model can be fit to human inputs.

Use training.py to create an ANN backpropogation model fitted to the data collected.

Run test_model.py to verify the accuracy of the model from training.py against the training set.

Only every 10th image is tagged in training. Tagging more images before testing can create a partial evaluation set.

TODO: Write a script to tag the test data above to create a better separation of training and testing data.