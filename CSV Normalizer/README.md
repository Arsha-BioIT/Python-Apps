# Flask Web App

This Flask web application allows users to upload CSV files, normalize data using various techniques, and visualize results.

## Features

### 1. File Upload Handling (`/upload`)
- Accepts CSV file uploads.
- Reads the CSV file using Pandas.
- Extracts column names and passes them to an HTML template for selection.

### 2. Data Normalization (`/normalize`)
- Applies multiple normalization techniques:
  - MinMax Scaling
  - Standard Scaling
  - Robust Scaling
  - MaxAbs Scaling
  - Log, Square Root, Box-Cox, and Yeo-Johnson transformations
- Saves the transformed data as a CSV file and provides it for download.

### 3. Data Visualization (`/visualize`)
- Generates histograms for a selected column.
- Converts the plot to a Base64-encoded image and displays it in an HTML template.

### 4. Safe File Storage
- Stores uploaded files in an `uploads` folder (automatically created if missing).


## Running the App

1. Start the Flask server:
   ```sh
   python app.py
   ```
2. Open a browser and go to `http://127.0.0.1:5000/`


## Dependencies
- Flask
- Pandas
- Scikit-learn
- Scipy
- Matplotlib
- Numpy


