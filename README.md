# London Property Market Dashboard

## Project Overview
This interactive dashboard provides comprehensive visualization and exploration of London's property market dynamics. The application enables users to analyze property trends, price distributions, and various housing characteristics across different neighborhoods in London through an intuitive and visually appealing interface.

## Features
- **Interactive Filtering**: Extensive filtering options for neighborhoods, price ranges, bedrooms, bathrooms, and more
- **Dynamic Visualizations**: Real-time updates of visualizations based on selected filters
- **Comprehensive Metrics**: Key statistics including average prices, property counts, and size measurements
- **Detailed Property Analysis**: Insights into property types, building ages, interior styles, and materials
- **Comparative Views**: Neighborhood comparisons and property characteristic relationships

## Technology Stack
- **Python**: Core programming language
- **Streamlit**: Web application framework for interactive dashboard
- **Pandas**: Data manipulation and analysis
- **Plotly Express**: Interactive data visualizations
- **CSS**: Custom styling for enhanced visual appeal

## Dashboard Components

### Filters
- Neighborhood selection
- Price range
- Number of bedrooms and bathrooms
- Number of floors
- Garden availability
- Garage availability
- Heating type
- Balcony presence
- Building status

### Visualizations
1. **Metric Cards**: Total properties, average price, and average size
2. **Price Distribution**: Box plots showing price distribution by neighborhood
3. **Property Type Analysis**: Bar charts displaying average prices by property type
4. **Building Age Impact**: Line charts showing price trends based on building age
5. **Interior Style and View**: Sunburst charts for interior style and view relationships
6. **Material Analysis**: Bar charts showing frequency of different building materials
7. **Neighborhood Statistics**: Data tables with property counts and price extremes

## Data Description
The dashboard uses a comprehensive dataset (`london_houses.csv`) containing detailed information about properties in various London neighborhoods, including:
- Prices
- Property types
- Physical characteristics (size, rooms, floors)
- Building features (age, materials, status)
- Interior attributes (style, heating type)
- External elements (garden, garage, view, balcony)

## Installation and Setup

### Prerequisites
- Python 3.7+
- Git

### Local Setup
```bash
# Clone the repository
git clone https://github.com/josuapane13/DataVisualizationProject.git
cd DataVisualizationProject

# Install required packages
pip install streamlit pandas plotly

# Run the application
streamlit run main.py
