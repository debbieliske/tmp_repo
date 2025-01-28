# Modified Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>Deloitte AI-Accelerated Reentry Thermodynamics (DAART)</h1>")

    # Input fields
    with gr.Row():
        altitude_input = gr.Slider(
            label="Altitude (m)",
            minimum=30000,
            maximum=80000,
            value=52500,
            step=100
        )
        velocity_input = gr.Slider(
            label="Velocity (m/s)",
            minimum=3000,
            maximum=11000,
            value=5250,
            step=10
        )
        angle_input = gr.Slider(
            label="Angle of Attack (degrees)",
            minimum=angle_of_attack_min,
            maximum=angle_of_attack_max,
            value=154,
            step=1
        )

    # Dropdown for target
    target_input = gr.Dropdown(
        label="Target",
        choices=prediction_columns,
        value="heat_flux: qw (W/m^2)"
    )

    # Single Button
    btn_calculate = gr.Button("Calculate")

    # Output components
    prediction_output = gr.Textbox(label="Prediction Status", interactive=False, value="")
    pred_image = gr.Image(label="Surface Predictions", visible=False)
    ec_image = gr.Image(label="Entry Corridor", visible=False)

    # Button Action
    btn_calculate.click(
        fn=lambda altitude, velocity, angle, target: (
            "Running model. Prediction in progress...",
            get_predictions(altitude, velocity, angle, target),
        ),
        inputs=[altitude_input, velocity_input, angle_input, target_input],
        outputs=[prediction_output, prediction_output],
        show_progress=True
    )

    btn_calculate.click(
        fn=lambda: ("Predictions Complete. Creating plots.", gr.update(visible=True), gr.update(visible=True)),
        inputs=[],
        outputs=[prediction_output, pred_image, ec_image]
    )

# Launch the app
demo.launch()
