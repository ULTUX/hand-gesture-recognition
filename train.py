import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

RANDOM_SEED = 44

dataset_path = "model/train_data.csv"
model_export = "model/model.hdf5"
tflite_export = "model/model.tflite"

class_size = 3

dataset = np.loadtxt(dataset_path, delimiter=',', dtype='float32',
                     usecols=list(range(1, 21 * 2 + 1)))
print(np.version.version)
values = np.loadtxt(dataset_path, delimiter=',', dtype='int32', usecols=(0))

X_train, X_test, y_train, y_test = train_test_split(dataset, values,
                                                    test_size=0.2,
                                                    random_state=RANDOM_SEED)

layers = tf.keras.layers
model = tf.keras.models.Sequential([
    layers.Input((21 * 2)),
    layers.Dropout(0.2),
    layers.Dense(20, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(10, activation='relu'),
    layers.Dense(class_size, activation='softmax')
])

save_listener = tf.keras.callbacks.ModelCheckpoint(model_export, verbose=1,
                                                   save_weights_only=False)
early_stop = tf.keras.callbacks.EarlyStopping(patience=20, monitor='val_loss')

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=1000, validation_data=(X_test, y_test),
          callbacks=[save_listener, early_stop])

val_loss, val_acc = model.evaluate(X_test, y_test, batch_size=128)

model = tf.keras.models.load_model(model_export)

result = model.predict(np.array([X_test[0]]))

print(np.squeeze(result))
print(np.argmax(np.squeeze(result)))

model.save(model_export, include_optimizer=False)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

open(tflite_export, "wb").write(tflite_model)
