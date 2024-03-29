import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

# meaningful_points = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
#                      17, 18, 19, 20]


meaningful_points = [2, 4, 5, 8, 9, 12, 13, 16, 17, 20]


def print_confusion_matrix(y_true, y_pred, report=True):
    labels = sorted(list(set(y_true)))
    cmx_data = confusion_matrix(y_true, y_pred, labels=labels)

    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)

    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(df_cmx, annot=True, fmt='g', square=True, cmap="crest")
    ax.set_ylim(len(set(y_true)), 0)
    ax.set_xlabel('Wartość przewidywana')
    ax.set_ylabel('Wartość rzeczywista')
    plt.show()

    if report:
        print('Classification Report')
        print(classification_report(y_test, y_pred))


RANDOM_SEED = 44

dataset_path = "model/stupid_data.csv"
model_export = "model/model.hdf5"
tflite_export = "model/model.tflite"

class_size = 6

XDataset = np.loadtxt(dataset_path, delimiter=',', dtype='float32',
                      usecols=list(range(1, (21 * 2) + 1)))
new_list = []
for i in meaningful_points:
    new_list.append(i * 2)
    new_list.append(i * 2 + 1)
meaningful_points = new_list
print(meaningful_points)

XDataset = XDataset[:, meaningful_points]

YDataset = np.loadtxt(dataset_path, delimiter=',', dtype='float32',
                      usecols=(0))

X_train, X_test, y_train, y_test = train_test_split(XDataset, YDataset,
                                                    train_size=0.75,
                                                    random_state=RANDOM_SEED)

layers = tf.keras.layers
model = tf.keras.models.Sequential([
    layers.Input(len(meaningful_points)),
    layers.Dropout(0.2),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(16, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(class_size, activation='softmax')
])
# layers.Input(len(meaningful_points)),
# layers.Dense(100, activation='relu'),
# layers.Dropout(0.2),
# layers.Dense(50, activation='relu'),
# layers.Dropout(0.2),
# layers.Dense(100, activation='relu'),
# layers.Dropout(0.2),
# layers.Dense(1000, activation='relu'),
# layers.Dropout(0.3),
# layers.Dense(5, activation='relu'),
# layers.Dense(class_size, activation='softmax')

save_listener = tf.keras.callbacks.ModelCheckpoint(model_export, verbose=1,
                                                   save_weights_only=False)
early_stop = tf.keras.callbacks.EarlyStopping(patience=60, verbose=1)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=300, batch_size=64,
          validation_data=(X_test, y_test),
          callbacks=[save_listener, early_stop])

val_loss, val_acc = model.evaluate(X_test, y_test, batch_size=128)

model = tf.keras.models.load_model(model_export)
predict_result = model.predict(np.array([X_test[0]]))
print(np.squeeze(predict_result))
print(np.argmax(np.squeeze(predict_result)))

Y_pred = model.predict(X_test)
y_pred = np.argmax(Y_pred, axis=1)

print_confusion_matrix(y_test, y_pred)

model.save(model_export, include_optimizer=False)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

open(tflite_export, "wb").write(tflite_model)
