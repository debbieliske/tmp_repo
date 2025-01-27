import gradio as gr
from PIL import Image

# Dummy function to process inputs
def get_predictions(altitude, velocity, angle_of_attack):
    return f"Inputs received: Altitude={altitude}, Velocity={velocity}, Angle of Attack={angle_of_attack}"

# Function to load and return images after results are ready
def display_images():
    pred_img = Image.open("surface_predictions.png")
    res_img = Image.open("surface_residuals.png")
    return pred_img, res_img

# Create the Gradio interface
with gr.Blocks() as demo:
    # Title
    gr.Markdown("## Display Entry Corridor and Predictions")

    # Show the entry corridor image
    entry_image = gr.Image(value="entry_corridor.png", label="Entry Corridor", interactive=False)
    
    # Inputs for user to enter values
    with gr.Row():
        altitude_input = gr.Number(label="Altitude")
        velocity_input = gr.Number(label="Velocity")
        angle_input = gr.Number(label="Angle of Attack")

    # Button for getting predictions
    btn_get_predictions = gr.Button("Get Predictions")
    
    # Placeholder for the prediction response
    prediction_output = gr.Textbox(label="Prediction Status", interactive=False)
    
    # Results button (hidden initially)
    btn_get_results = gr.Button("Get Results", visible=False)

    # Results section, initially hidden
    with gr.Row(visible=False) as result_row:
        pred_image = gr.Image(label="Surface Predictions")
        res_image = gr.Image(label="Surface Residuals")

    # Connect the Get Predictions button to the dummy function
    btn_get_predictions.click(
        fn=get_predictions,
        inputs=[altitude_input, velocity_input, angle_input],
        outputs=prediction_output,
        show_progress=False
    )
    
    # Enable the Get Results button after getting predictions
    btn_get_predictions.click(
        lambda: gr.update(visible=True),
        inputs=[],
        outputs=btn_get_results
    )
    
    # Connect the Get Results button to display images
    btn_get_results.click(
        fn=display_images, 
        outputs=[pred_image, res_image],
        show_progress=False
    )
    
    # Make the images section visible after Get Results is pressed
    btn_get_results.click(
        lambda: gr.update(visible=True),
        inputs=[],
        outputs=result_row
    )

# Launch the interface
demo.launch()
