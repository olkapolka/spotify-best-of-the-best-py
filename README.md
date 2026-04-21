# 🎵 Spotify Best of the Best - Data Analytics Dashboard

Capstone project for Coursera Google Data Analytics.

An interactive data analytics web application built with Python and Streamlit for analyzing Spotify playlist data.

## 🚀 Features

- **Interactive Dashboard**: Web-based interface for exploring playlist data
- **Data Explorer**: Filter, view, and download data subsets
- **Visualizations**: Create histograms, box plots, scatter plots, and correlation heatmaps
- **Statistical Analysis**: Comprehensive statistical summaries for numeric and categorical data
- **Text Analytics**: Utilities for analyzing text columns in your dataset

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🛠️ Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd spotify-best-of-the-best
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Running the Dashboard

Start the Streamlit application:

```bash
streamlit run app.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`.

### Using the Utility Modules

You can also use the utility modules in your own scripts:

```python
from utils.data_processor import DataProcessor, load_and_validate_csv
from utils.text_analyzer import TextAnalyzer, analyze_column_text

# Load data
df = load_and_validate_csv('playlist-data-fully-enriched.csv')

# Process data
processor = DataProcessor(df)
cleaned_df = processor.clean_data()
stats = processor.get_summary_stats()

# Analyze text
text_stats = analyze_column_text(df, 'your_text_column')
```

## 📁 Project Structure

```
spotify-best-of-the-best/
├── app.py                              # Main Streamlit application
├── requirements.txt                     # Python dependencies
├── playlist-data-fully-enriched.csv    # Dataset
├── utils/
│   ├── __init__.py
│   ├── data_processor.py               # Data processing utilities
│   └── text_analyzer.py                # Text analysis utilities
├── .gitignore
└── README.md
```

## 📊 Dashboard Pages

1. **Overview**: View dataset summary, column information, and sample data
2. **Data Explorer**: Filter columns, adjust row display, and download filtered data
3. **Visualizations**: Create various charts and plots for data exploration
4. **Statistics**: View detailed statistical summaries for all columns

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib & Seaborn**: Data visualization
- **Plotly**: Interactive visualizations

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements.

## 📧 Contact

For questions or feedback about this project, please open an issue in the repository.
