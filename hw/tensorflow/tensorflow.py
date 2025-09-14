import tensorflow as tf
import numpy as np

# True parameters
actual_slope = 12.5
actual_intercept = 25

SAMPLE_COUNT = 100
x_data = np.linspace(0, 10, SAMPLE_COUNT)
y_data = actual_slope * x_data + actual_intercept + np.random.normal(scale=1.5, size=SAMPLE_COUNT)

# Define a simple linear regression model
regression_model = tf.keras.Sequential([
    tf.keras.layers.Dense(1, input_shape=[1])
])

regression_model.compile(optimizer='adam', loss='mean_squared_error')

print("Training the linear regression model...")
training_history = regression_model.fit(x_data, y_data, epochs=50, verbose=1)
print("Model training complete.")

estimated_slope = regression_model.layers[0].get_weights()[0][0][0]
estimated_intercept = regression_model.layers[0].get_weights()[1][0]

print(f"Actual slope (m): {actual_slope:.2f}, intercept (c): {actual_intercept:.2f}")
print(f"Estimated slope (m): {estimated_slope:.2f}, intercept (c): {estimated_intercept:.2f}")

# Predict for new data point
x_test = np.array([15.0])
predicted_y = regression_model.predict(x_test)

print(f"\nFor x = {x_test[0]:.0f}, predicted y = {predicted_y[0][0]:.2f}")
