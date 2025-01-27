import gradio as gr
from PIL import Image
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
#from tensorflow.keras.models import load_model
import joblib
import time
from plots import plot_3d_scatter
from metrics import rmse_metric, mae_metric, r2_metric


prediction_columns = target_cols = ['surface_pressure: pw (Pa)',
            'shear_stress_x: tauwx (Pa)', 'shear_stress_y: tauwy (Pa)', 'shear_stress_z: tauwz (Pa)',
            'heat_flux: qw (W/m^2)',
            'boundary_layer_thickness: delta (m)',
            'reynolds_number-momentum_thickness']

mlp_model = tf.keras.models.load_model('../../models/enhanced_mlp_model.keras', custom_objects={'rmse_metric': rmse_metric, 'mae_metric': mae_metric, 'r2_metric': r2_metric})    
mlp_scaler_inputs = joblib.load('../../models/enhanced_mlp_scaler_inputs.pkl')    
mlp_scaler_targets = joblib.load('../../models/enhanced_mlp_scaler_targets.pkl')

# get the surface points x, y, z
xyz_df = pd.read_feather('../../data/data.feather')
cols = ['x_coordinate: xw (m)',
    'y_coordinate: yw (m)', 'z_coordinate: zw (m)']

xyz_df = xyz_df[cols]

def get_predictions(altitude, velocity, angle_of_attack, feature='heat_flux: qw (W/m^2)'):

    # Create a DataFrame with the same input on each row
    X_data = pd.DataFrame({
        'altitude (m)': [altitude] * len(xyz_df),
        'velocity (m/s)': [velocity] * len(xyz_df),
        'angle_of_attack (deg)': [angle_of_attack] * len(xyz_df)
    })
    # Merge the X_data with xyz_df
    X_data = pd.concat([X_data, xyz_df], axis=1)
    X_data = X_data.drop_duplicates()
    tmp = X_data[(X_data['altitude (m)'] == 60000) & (X_data['velocity (m/s)'] == 7000)]
    X_scaled = mlp_scaler_inputs.transform(X_data)
 
    predictions = mlp_model.predict(X_scaled)
    predictions = mlp_scaler_targets.inverse_transform(predictions)
    
    # Merge predictions with xyz_df
    predictions_df = pd.DataFrame(predictions, columns=prediction_columns)
    results_df = pd.concat([xyz_df, predictions_df], axis=1)

    # Save the predictions to a file
    #results_df.to_feather('results_df.feather')

    plot_3d_scatter(results_df, feature)

    return f"Inputs received: Altitude={altitude}, Velocity={velocity}, Angle of Attack={angle_of_attack}"

# Function to simulate loading and return images
def display_images():
    time.sleep(2)  # Simulate processing delay
    pred_img = Image.open("surface_predictions.png")
    res_img = Image.open("surface_residuals.png")
    return pred_img, res_img

# Function to display spinner status
def show_spinner():
    return "In Progress..."

# Function to clear the spinner after results are ready
def clear_spinner():
    return ""

# Reset interface function
def reset_interface():
    return (
        "",                        # prediction_output (TextBox)
        "",                        # spinner_output (TextBox)
        52500,                     # altitude_input (Number)
        5250,                      # velocity_input (Number)
        154,                       # angle_input (Number)
        "heat_flux: qw (W/m^2)",   # target_input (Dropdown)
        None,                      # pred_image (Image)
        None,                      # res_image (Image),
        gr.update(visible=False),  # btn_get_results visibility (Button)
        gr.update(visible=False)   # result_row visibility (Row)
    )

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>Deloitte AI-Accelerated Reentry Thermodynamics (DAART)</h1>")

    # Entry image
    entry_image = gr.Image(value="entry_corridor.png", label="Entry Corridor", interactive=False)

    # Input fields
    with gr.Row():
        altitude_input = gr.Number(label="Altitude (m)", value=52500)
        velocity_input = gr.Number(label="Velocity (m/s)", value=5250)
        angle_input = gr.Number(label="Angle of Attack (degrees)", value=154)

    # Dropdown for target
    target_input = gr.Dropdown(
        label="Target",
        choices=prediction_columns,
        value="heat_flux: qw (W/m^2)"
    )

    # Buttons
    with gr.Row():
        btn_get_predictions = gr.Button("Get Predictions")
        btn_reset = gr.Button("Reset")

    # Output components
    prediction_output = gr.Textbox(label="Prediction Status", interactive=False)
    spinner_output = gr.Textbox(label="Status", interactive=False, visible=False)
    btn_get_results = gr.Button("Get Results", visible=False)

    # Results section
    with gr.Row(visible=False) as result_row:
        pred_image = gr.Image(label="Surface Predictions")
        res_image = gr.Image(label="Surface Residuals")

    # Button Actions
    btn_get_predictions.click(
        fn=get_predictions,
        inputs=[altitude_input, velocity_input, angle_input, target_input],
        outputs=prediction_output,
        show_progress=False
    )

    btn_get_predictions.click(
        lambda: gr.update(visible=True),
        inputs=[],
        outputs=btn_get_results
    )

    btn_get_results.click(fn=show_spinner, inputs=[], outputs=spinner_output)
    btn_get_results.click(fn=display_images, outputs=[pred_image, res_image])
    btn_get_results.click(fn=clear_spinner, inputs=[], outputs=spinner_output)
    btn_get_results.click(lambda: gr.update(visible=True), inputs=[], outputs=result_row)

    # Reset button
    btn_reset.click(
        fn=reset_interface,
        inputs=[],
        outputs=[
            prediction_output, spinner_output, altitude_input, velocity_input, angle_input,
            target_input, pred_image, res_image, btn_get_results, result_row
        ]
    )

# Launch the app
demo.launch()

