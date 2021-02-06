import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd
from tensorflow.keras import optimizers
from datetime import datetime
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

###################### prepare the dataset for training #####################
def convert_time(time_str):
    start = datetime.strptime("2009/01/05", '%Y/%m/%d')
    date = datetime.strptime(time_str, '%Y/%m/%d %I:%M:00+00')
    duration = date - start
    return duration.days

path = "../Purchase_Card_Transactions.csv"
data = pd.read_csv(path)#.head(10)

drop_data = data.dropna(subset=['VENDOR_NAME', "VENDOR_STATE_PROVINCE"])
data = drop_data.groupby('VENDOR_NAME').filter(lambda x : len(x)>100) #366710

mlb = MultiLabelBinarizer()
label_encoder = LabelEncoder()
data_vendor = data['VENDOR_NAME'].fillna("")
mlb.fit_transform([data_vendor])
integer_encoded = label_encoder.fit_transform(data_vendor)
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
vendor_encoded = onehot_encoder.fit_transform(integer_encoded)

mlb = MultiLabelBinarizer()
label_encoder = LabelEncoder()
data_agency = data['AGENCY'].fillna("")
mlb.fit_transform([data_agency])
integer_encoded = label_encoder.fit_transform(data_agency)
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
agency_encoded = onehot_encoder.fit_transform(integer_encoded)

mlb = MultiLabelBinarizer()
label_encoder = LabelEncoder()
data_desc = data['MCC_DESCRIPTION'].fillna("")
mlb.fit_transform([data_desc])
integer_encoded = label_encoder.fit_transform(data_desc)
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
type_encoded = onehot_encoder.fit_transform(integer_encoded)
print(type_encoded.shape)

time_data = data["TRANSACTION_DATE"].apply(lambda x:convert_time(x)).to_numpy()
train_time = np.reshape(time_data, (-1, 1)) / (365*11.0)

y = data["TRANSACTION_AMOUNT"].to_numpy()
y = np.reshape(y, (-1, 1))

data = np.concatenate([vendor_encoded, agency_encoded, train_time, y], -1)

train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
train_input = train_set[:,:-1]
train_labels = train_set[:, -1]
test_input = test_set[:,:-1]
test_labels = test_set[:, -1]

print(train_set.shape, train_input.shape, train_labels.shape)


###################### creating and training the model ######################
batch_size = 256
input_size = train_input.shape[1]
hidden_1 = 2048
hidden_2 = 1024
hidden_3 = 512
hidden_4 = 256
output_size = 1
interval = 200
train_dataset = tf.data.Dataset.from_tensor_slices((train_input, train_labels)).shuffle(200000).batch(batch_size)
test_dataset = tf.data.Dataset.from_tensor_slices((test_input, test_labels)).batch(1)

# sequential model with 2 hidden unit
model = tf.keras.models.Sequential(
    [
        layers.Dense(input_size, activation="relu", name="layer1", kernel_initializer="he_normal", kernel_regularizer=tf.keras.regularizers.l2(0.03)),
        layers.Dense(hidden_1, activation="relu", name="layer2", kernel_initializer="he_normal", kernel_regularizer=tf.keras.regularizers.l2(0.03)),
        layers.Dense(hidden_2, activation="relu", name="layer3", kernel_initializer="he_normal", kernel_regularizer=tf.keras.regularizers.l2(0.03)),
        layers.Dense(hidden_3, activation="relu", name="layer4", kernel_initializer="he_normal", kernel_regularizer=tf.keras.regularizers.l2(0.03)),
        layers.Dense(hidden_4, activation="relu", name="layer5", kernel_initializer="he_normal", kernel_regularizer=tf.keras.regularizers.l2(0.03)),
        tf.keras.layers.Dense(output_size, activation="relu", name="output")
    ]
)

model.build(input_shape=(batch_size, input_size))
optimizer = optimizers.Adam(learning_rate=1e-3)

model.summary()

def train(data, labels):
    with tf.GradientTape() as tape:
        output = model(data)
        loss = tf.reduce_mean(tf.losses.MSE(output, labels))
    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))

    return loss

def test(data, labels):
    output = model(data)
    loss = tf.reduce_mean(tf.losses.MSE(output, labels))
    return loss

log_dir = "log"
model_dir = "model"
writer = tf.summary.create_file_writer(log_dir)
loss_lowest = 10000000000

with writer.as_default():
    for epoch in range(30):
        total_loss = 0
        num_batches = 0
        for batch_id, (data, labels) in enumerate(train_dataset):
            loss = train(data, labels)
            total_loss += loss
            num_batches += 1
            if num_batches % interval == 0:
                train_loss = total_loss / num_batches
                tf.summary.scalar("training_loss", train_loss, step=epoch)
                writer.flush()
                print("Epoch: ", epoch, " batch: ", num_batches, "training loss: ", train_loss)
                if train_loss < loss_lowest:
                    model.save_weights(model_dir + "/" + model_dir)
                model.save_weights(model_dir + "/" + model_dir)

        total_loss = 0
        num_batches = 0
        for batch_id, (data, labels) in enumerate(test_dataset):
            loss = test(data, labels)
            total_loss += loss
            num_batches += 1
        test_loss = total_loss / num_batches
        tf.summary.scalar("testing_loss", test_loss, step=epoch)
        writer.flush()
        print("Epoch: ", epoch, "testing loss: ", test_loss)


