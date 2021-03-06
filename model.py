import csv
import cv2
import numpy as np
from PIL import Image


lines = []

with open('download/data/driving_log.csv') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        lines.append(line)

images = []
measurements = []

cnt = -1
for line in lines:
    cnt += 1
    if cnt == 0:
        continue
    for i in range(1):
        source_path = line[i]
        filename = source_path.split('/')[-1]
        current_path = 'download/data/IMG/'+filename
        # image = cv2.imread(current_path)
        image = Image.open(current_path)
        image = np.asarray(image)
        # print(image)
        images.append(image)
        measurement = float(line[3])
        # print(measurement)
        measurements.append(measurement)
    
augmented_images, augmented_measurements = [], []
for image, measurement in zip(images, measurements):
    augmented_images.append(image)
    augmented_measurements.append(measurement)
    augmented_images.append(cv2.flip(image, 1))
    augmented_measurements.append(measurement*-1.0)

X_train = np.array(augmented_images)
y_train = np.array(augmented_measurements)

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D


model = Sequential()
model.add(Lambda(lambda x:x/255.0-0.5, input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((70,25), (0,0))))
model.add(Convolution2D(24,5,5,subsample=(2,2),activation='relu'))
model.add(Convolution2D(36,5,5,subsample=(2,2),activation='relu'))
model.add(Convolution2D(48,5,5,subsample=(2,2),activation='relu'))
model.add(Convolution2D(64,3,3,activation='relu'))
model.add(Convolution2D(64,3,3,activation='relu'))
model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))

model.compile(loss='mse', optimizer='adam')
model.fit(X_train, y_train, validation_split=0.2, 
shuffle=True, nb_epoch=5, verbose=1)

model.save('model.h5')

from keras.utils import plot_model
plot_model(model, to_file='model.png')
