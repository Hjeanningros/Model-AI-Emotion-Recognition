import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator


# Initialize image data generator with rescaling
train_data_gen = ImageDataGenerator(rescale=1. / 255)
validation_data_gen = ImageDataGenerator(rescale=1. / 255)

# Preprocess all test images
train_generator = train_data_gen.flow_from_directory(
    'Data/train',
    target_size=(48, 48),
    batch_size=64,
    color_mode="grayscale",
    class_mode='categorical')

# Preprocess all train images
validation_generator = validation_data_gen.flow_from_directory(
    'Data/test',
    target_size=(48, 48),
    batch_size=64,
    color_mode="grayscale",
    class_mode='categorical')

# create model structure
emotion_model = Sequential()

# First block: 2 x Convolution layer with 128 filters + Max pooling
emotion_model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
emotion_model.add(Conv2D(128, (3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))

# Second block: 2 x Convolution layer with 64 filters + Max pooling
emotion_model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
emotion_model.add(Conv2D(64, (3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))

# Third block: 2 x Convolution layer with 32 filters + Max pooling
emotion_model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(48, 48, 1)))
emotion_model.add(Conv2D(32, (3, 3), activation='relu'))
emotion_model.add(Conv2D(32, (3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))

# Flattening followed by Dense layers
emotion_model.add(Flatten())
emotion_model.add(Dense(256, activation='relu'))
emotion_model.add(Dropout(0.5))
emotion_model.add(Dense(5, activation='softmax')) 

emotion_model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.0001),
                      metrics=['accuracy'])


# Train the neural network/model
emotion_model_info = emotion_model.fit(
    train_generator,
    steps_per_epoch= 24176 // 64,
    epochs=50,
    validation_data=validation_generator,
    validation_steps=6043 // 64)


emotion_model.save('emotion_model.h5')

