from flask import Flask, request, render_template, send_file
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, MaxAbsScaler, QuantileTransformer
import os
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        df = pd.read_csv(filepath)
        columns = df.columns.tolist()
        return render_template('normalize.html', columns=columns, filename=file.filename)
    return "Invalid file format"

@app.route('/normalize', methods=['POST'])
def normalize():
    column_name = request.form['column_name']
    filename = request.form['filename']
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    df = pd.read_csv(filepath)
    
    # Normalization techniques
    scalers = {
        'Min-Max Scaling': MinMaxScaler(),
        'Standard Scaling': StandardScaler(),
        'Robust Scaling': RobustScaler(),
        'MaxAbs Scaling': MaxAbsScaler(),
        'Log Transformation': None,  # Handle separately
        'Square Root Transformation': None,  # Handle separately
        'Box-Cox Transformation': None,  # Handle separately
        'Yeo-Johnson Transformation': None,  # Handle separately
        'Quantile Transformation': QuantileTransformer(output_distribution='uniform')
    }
    
    results = {}

    for name, scaler in scalers.items():
        if name in ['Log Transformation', 'Square Root Transformation']:
            if (df[column_name] >= 0).all():  # Ensure non-negative values
                if name == 'Log Transformation':
                    results[name] = np.log1p(df[column_name])  # log(1 + x) to handle 0
                elif name == 'Square Root Transformation':
                    results[name] = np.sqrt(df[column_name])
        elif name == 'Box-Cox Transformation':
            if (df[column_name] > 0).all():  # Box-Cox requires strictly positive values
                results[name], _ = stats.boxcox(df[column_name])  
        elif name == 'Yeo-Johnson Transformation':
            results[name], _ = stats.yeojohnson(df[column_name])  # Yeo-Johnson works for all values
        else:
            scaled_data = scaler.fit_transform(df[[column_name]])
            results[name] = scaled_data.flatten()
    
    # Create a new DataFrame with the results
    result_df = pd.DataFrame(results)
    result_filepath = os.path.join(UPLOAD_FOLDER, f'normalized_{filename}')
    result_df.to_csv(result_filepath, index=False)
    
    return send_file(result_filepath, as_attachment=True)

@app.route('/visualize', methods=['POST'])
def visualize():
    filename = request.form['filename']
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    df = pd.read_csv(filepath)
    
    column_name = request.form.get('column_name')  # Get column name for visualization
    
    # Create a plot
    plt.figure(figsize=(8, 5))
    
    if column_name and column_name in df.columns:
        df[column_name].hist(bins=30, alpha=0.7, color='blue', edgecolor='black')
        plt.xlabel(column_name)
        plt.ylabel("Frequency")
        plt.title(f"Histogram of {column_name}")
    else:
        return "Invalid column selected for visualization"
    
    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template('visualize.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
