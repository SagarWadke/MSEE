# Motorized Stage Error Estimation (MSEE) - Position
*This project provides a Python-based positional error estimation tool for a motorized stage (linear or rotational) by estimating the extrinsic parameters from a series of images taken at defined displacement intervals using an intrinsically calibrated camera.*

---

## Features

- Supports positional error estimation using a checkerboard as a target.
- Can estimate errors for displacements up to 0.5mm with reasonable accuracy*.
- All calculated extrinsic parameters are saved in Excel file format.
- Good repeatability if external conditions remain unchanged.
- Extended analysis feature provides plots for better visualization with total percentage error.
- Modular code structure with reusable utility functions.
- Quick and easy to use.

---

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/camera-calibration.git
    cd camera-calibration
    ```

2. **(Optional) Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate   # On Windows
    # source venv/bin/activate   # On Linux/Mac
    ```

3. **Install the necessary libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Save the images of the checkerboard taken from your camera in the same directory where the `msee` folder is located.**

5. **Run the code:**
    ```bash
    python -m msee.get_extrinsics
    ```

---

## Notes

- *Reasonable accuracy: The experimental results have not been compared with a ground truth, but experience shows the results are good enough for approximation.*
- Ensure the intrinsic parameters of the camera have a very low reprojection error. For this project, the calculated reprojection error is approx 0.01578 pixels.
- Make sure there are no external vibrations or disturbances when collecting images from the linear stage.
- Glue/tape the pattern to a flat surface for better estimation of errors.

---

## License

[MIT](LICENSE)