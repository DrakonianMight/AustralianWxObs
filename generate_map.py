import get_station_locations from getObs

def create_station_map(output_html='station_map.html'):
    """
    Creates a map with station markers using Plotly and saves it as an HTML file.
    
    Parameters:
    - output_html (str): Path to save the output HTML file. Default is 'station_map.html'.
    """
    import plotly.express as px
    
    # Get station locations from the database
    station_data = get_station_locations()
    
    # Create a scatter mapbox plot
    fig = px.scatter_mapbox(
        station_data,
        lat="latitude",
        lon="longitude",
        hover_name="name",  # Shows station name on hover
        zoom=4,  # Adjust the initial zoom level of the map
        height=600  # Adjust the height of the map
    )
    
    # Customize the layout for the map
    fig.update_layout(
        mapbox_style="open-street-map",  # Use OpenStreetMap tiles
        title_text="Weather Station Locations",  # Map title
        title_x=0.5  # Center the title
    )
    
    # Save the figure as an HTML file
    fig.write_html(output_html)
    print(f"Map has been saved to {output_html}")