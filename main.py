# Library
import streamlit as st
import pandas as pd
import plotly.express as px

# Set konfigurasi halaman sebelum elemen lainnya
st.set_page_config(page_title="House in London Dashboard", layout="wide")

# Memuat file CSS eksternal
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# Load data
def load_data():
    data = pd.read_csv("Dataset/london_houses.csv")
    return data
data = load_data()

st.header("Eksplorasi Dinamika Pasar Properti di London") 
# Sidebar dengan judul
st.sidebar.image("logo.png") 
st.sidebar.markdown("----------------------------")
st.sidebar.header("Opsi Filter")

# Filter Neighborhood
neighborhood_options = data['Neighborhood'].unique().tolist()
neighborhood_options.insert(0, "Semua")  
selected_neighborhood = st.sidebar.multiselect(
    "Pilih Neighborhood(s):", options=neighborhood_options, default="Semua")

if "Semua" in selected_neighborhood:
    filtered_neighborhoods = data['Neighborhood'].unique()
else:
    filtered_neighborhoods = selected_neighborhood

# Filter harga
price_range = st.sidebar.slider(
    "Pilih Jangkauan Harga (£):", 
    int(data['Price (£)'].min()), 
    int(data['Price (£)'].max()), (500000, 2000000)
)
bedrooms = st.sidebar.slider(
    "Jumlah Kamar Tidur (Bedrooms):",
    min_value=int(data["Bedrooms"].min()),
    max_value=int(data["Bedrooms"].max()),
    value=(int(data["Bedrooms"].min()), int(data["Bedrooms"].max()))
)

# Filter Bathrooms
bathrooms = st.sidebar.slider(
    "Jumlah Kamar Mandi (Bathrooms):",
    min_value=int(data["Bathrooms"].min()),
    max_value=int(data["Bathrooms"].max()),
    value=(int(data["Bathrooms"].min()), int(data["Bathrooms"].max()))
)
# Filter Floors
floors = st.sidebar.slider(
    "Jumlah Lantai (Floors):",
    min_value=int(data["Floors"].min()),
    max_value=int(data["Floors"].max()),
    value=(int(data["Floors"].min()), int(data["Floors"].max()))
)

# Filter Garden
garden_options = data["Garden"].unique().tolist()
selected_garden = st.sidebar.selectbox("Taman (Garden):", options=["Semua"] + garden_options)

# Filter Garage
garage_options = data["Garage"].unique().tolist()
selected_garage = st.sidebar.selectbox("Garasi (Garage):", options=["Semua"] + garage_options)

# Filter Heating Type
heating_options = data["Heating Type"].unique().tolist()
selected_heating = st.sidebar.selectbox("Tipe Pemanas (Heating Type):", options=["Semua"] + heating_options)

# Filter Balcony
balcony_options = data["Balcony"].unique().tolist()
selected_balcony = st.sidebar.selectbox("Balkon (Balcony):", options=["Semua"] + balcony_options)

# Filter Building Status
building_status_options = data["Building Status"].unique().tolist()
selected_building_status = st.sidebar.selectbox(
    "Status Bangunan (Building Status):", options=["Semua"] + building_status_options
)

# Filter data
filtered_data = data[
    (data['Neighborhood'].isin(filtered_neighborhoods)) & 
    (data['Price (£)'].between(price_range[0], price_range[1])) &
    (data["Bedrooms"].between(bedrooms[0], bedrooms[1])) &
    (data["Bathrooms"].between(bathrooms[0], bathrooms[1])) &
    (data["Floors"].between(floors[0], floors[1]))
]
if selected_garden != "Semua":
    filtered_data = filtered_data[filtered_data["Garden"] == selected_garden]

if selected_garage != "Semua":
    filtered_data = filtered_data[filtered_data["Garage"] == selected_garage]

if selected_heating != "Semua":
    filtered_data = filtered_data[filtered_data["Heating Type"] == selected_heating]

if selected_balcony != "Semua":
    filtered_data = filtered_data[filtered_data["Balcony"] == selected_balcony]

if selected_building_status != "Semua":
    filtered_data = filtered_data[filtered_data["Building Status"] == selected_building_status]

# Row A
def metric_card(title, value):
    st.write(
        f"""
        <div class='metric-card'>
            <h5>{title}</h5>
            <h3>{value}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

col_left, col_right = st.columns((9, 1.8), gap='medium')

# Kolom kiri 
with col_left:
    # Row A
    col1, col2, col3 = st.columns([1, 1, 1]) 
    total_properties = filtered_data.shape[0]
    average_price = filtered_data['Price (£)'].mean()
    average_size = filtered_data['Square Meters'].mean()

    with col1:
        metric_card("Total Properti", total_properties)

    with col2:
        metric_card("Rata-Rata Harga", f"£{average_price:,.2f}")

    with col3:
        metric_card("Rata-Rata Luas", f"{average_size:,.2f} m²")

    # Plot
    # Changed to blue color palette
    color_palette = [
        '#0066CC', '#1A75D1', '#3385D6', '#4D94DB', '#66A3E0',  
        '#80B3E6', '#99C2EB', '#B3D1F0', '#CCE0F5', '#66A3E0'   
    ]

    # Row B
    col4, col5 = st.columns([1.5, 1.5])

    with col4:
        with st.container():
            st.subheader("Distribusi Harga")
            neighborhood_price = px.box(
                filtered_data, 
                x="Neighborhood", 
                y="Price (£)", 
                labels={"Price (£)": "Harga (£)", "Neighborhood": "Neighborhood"},
                color="Neighborhood",
                color_discrete_sequence=color_palette
            )
            neighborhood_price.update_layout(showlegend=False)
            st.plotly_chart(neighborhood_price, use_container_width=True)

    grouped_df = filtered_data.groupby(['Property Type'])['Price (£)'].mean().reset_index()
    with col5:
        with st.container():
            st.subheader("Rata-Rata Harga Tipe Properti")
            property_vs_price = px.bar(
                grouped_df,
                x="Price (£)",
                y="Property Type",
                labels={"Price (£)": "Harga (£)", "Property Type": "Tipe Properti"},
                color="Property Type",
                orientation='h',
                color_discrete_sequence=color_palette
            )
            property_vs_price.update_layout(showlegend=False)
            st.plotly_chart(property_vs_price, use_container_width=True)

    # Row C
    col6, col7 = st.columns([1.5, 1.5])

    average_price_by_age = filtered_data.groupby('Building Age')['Price (£)'].mean().reset_index()
    with col6:
        with st.container():
            st.subheader("Rata-Rata Harga Usia Bangunan")
            line_plot = px.line(
                average_price_by_age,
                x="Building Age",
                y="Price (£)",
                labels={"Price (£)": "Harga (£)", "Building Age": "Usia Bangunan (Tahun)"},
                markers=True
            )
            # Changed from red to blue
            line_plot.update_traces(line_color='#0066CC')
            st.plotly_chart(line_plot, use_container_width=True)
        
    with col7:
        with st.container():
            st.subheader("Distribusi Gaya Interior dan View")
            
            interior_data = filtered_data["Interior Style"].value_counts().reset_index()
            interior_data.columns = ["Interior Style", "Count"]
            view_data = filtered_data["View"].value_counts().reset_index()
            view_data.columns = ["View", "Count"]
            
            nested_pie = px.sunburst(
                data_frame=filtered_data,
                path=["Interior Style", "View"],
                values=None,
                # Changed to blue colors
                color_discrete_sequence=['#0066CC', '#4D94DB', '#80B3E6', '#6B89A3']
            )
            nested_pie.update_layout(
                margin=dict(t=50, l=50, r=50, b=50)
            )
            nested_pie.update_traces(
                textinfo="label+percent entry", 
                textfont=dict(color='white'),
                insidetextorientation='horizontal', 
                marker=dict(
                    line=dict(color="white", width=2))
            )
            st.plotly_chart(nested_pie, use_container_width=True)

    with st.container():
        st.subheader("Frekuensi Material")
        material_data = filtered_data["Materials"].value_counts().reset_index()
        material_data.columns = ["Materials", "Count"]
        material_bar = px.bar(
            material_data,
            x="Materials",
            y="Count",
            text="Count",
            color="Materials",
            # Changed to blue colors
            color_discrete_sequence=['#0066CC', '#4D94DB', '#80B3E6', '#6B89A3'],
            labels={"Materials": "Jenis Material", "Count": "Jumlah Material"},
        )
        material_bar.update_traces(textposition="outside")
        material_bar.update_layout(showlegend=False)
        st.plotly_chart(material_bar, use_container_width=True)
    
with col_right:
    # Tabel properti
    total_properti_neighborhood = filtered_data['Neighborhood'].value_counts().reset_index()
    total_properti_neighborhood.columns = ['Neighborhood', 'Total']
    st.markdown('##### Properti Setiap Neighborhood')
    st.dataframe(total_properti_neighborhood, hide_index=True)
    
    # Tabel Harga Termahal
    top_3_harga_termahal = filtered_data.nlargest(3, 'Price (£)')[['Neighborhood', 'Price (£)']]
    st.markdown('##### Top 3 Harga Termahal')
    st.dataframe(top_3_harga_termahal.reset_index(drop=True), hide_index=True)
    
    # Tabel Harga Termurah
    top_3_harga_termurah = filtered_data.nsmallest(3, 'Price (£)')[['Neighborhood', 'Price (£)']]
    st.markdown('##### Top 3 Harga Termurah')
    st.dataframe(top_3_harga_termurah.reset_index(drop=True), hide_index=True)

# Footer 
st.write("\n")  
st.write("© Josua Pane - Basic Visualization Project")