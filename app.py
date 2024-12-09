import altair as alt
import pandas as pd
import streamlit as st

st.title("FIFA All Star Lineup")
st.markdown("All-star Players with cost analysis ")

# Load the data
fifa_cleaned_df = pd.read_csv('fifa_cleaned (version 2).csv')

# Initialize session state variables if they don't exist
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Function to switch pages
def switch_page(page: str):
    st.session_state.current_page = page

# Sidebar navigation
st.sidebar.subheader("Navigation")

if st.sidebar.button("Comparison".upper()):
    switch_page("Comparison")

if st.sidebar.button("Barchart".upper()):
    switch_page("Barchart")

if st.sidebar.button("Data".upper()):
    switch_page("Data")

def Comparison():
    st.subheader("Player Value Comparison")
    
    # Predefined scatter plot options
    x_choices = ["overall_rating", "height_cm", "weight_kgs", "age"]
    y_choices = ["value_euro", "wage_euro", "potential", "dribbling"]
    
    # Default selections for x and y axes
    selected_x_var = st.selectbox("Select X-axis variable:", x_choices, index=0)  # Default: overall_rating
    selected_y_var = st.selectbox("Select Y-axis variable:", y_choices, index=0)  # Default: value_euro

    # Plot scatter plot using Altair
    alt_chart = (
        alt.Chart(fifa_cleaned_df)
        .mark_circle()
        .encode(
            x=alt.X(selected_x_var, scale=alt.Scale(zero=False)),
            y=alt.Y(selected_y_var, scale=alt.Scale(zero=False)),
            color="positions",  # Color by position for better visual clarity
            tooltip=["name", "nationality", "positions", selected_x_var, selected_y_var]  # Add nationality to the hover
        )
        .interactive()
    )
    st.altair_chart(alt_chart, use_container_width=True)

# Assuming fifa_cleaned_df is already loaded
# fifa_cleaned_df = pd.read_csv('fifa_cleaned (version 2).csv')

def Barchart():
    st.subheader("Players by Club Analysis")

    # Define the allowed club teams
    allowed_club_teams = [
        "Juventus", "Paris Saint-Germain", "Milan", "Real Madrid", 
        "FC Barcelona", "Manchester City", "Manchester United", 
        "FC Bayern München", "Borussia Dortmund", "Arsenal", 
        "Atlético Madrid", "Chelsea", "Liverpool", 
        "LA Galaxy", "New York City FC"
    ]
    
    # Selection box for club teams, limited to the allowed list
    selected_club = st.selectbox(
        "Select a Club Team:",
        options=allowed_club_teams
    )
    
    # Filter the data for the selected club team
    filtered_data = fifa_cleaned_df[fifa_cleaned_df['club_team'] == selected_club]

    # Dropdowns for selecting the Y-axis variable
    y_var = st.selectbox(
        "Choose a variable for the Y-axis:",
        options=["short_passing", "dribbling", "sprint_speed", "strength", "overall_rating", "potential"]
    )
    
    # Create the Altair bar chart with player names on the X-axis and selected variable on the Y-axis
    chart = alt.Chart(filtered_data).mark_bar().encode(
        x=alt.X('name:N', title="Player Name"),  # Set player names as the X-axis
        y=alt.Y(y_var, title=y_var),  # Set selected variable on the Y-axis
        tooltip=["name", "value_euro"],  # Show player name and value in euros in the tooltip
    ).properties(
        title=f"Bar Chart of {selected_club} - {y_var} vs Player"
    ).configure_mark(
        opacity=0.8
    )

    # Display the chart
    st.altair_chart(chart, use_container_width=True)

# Adds the "Formation" page to the sidebar
def Formation():
    st.subheader("Formation View")

    # Filter data for players you want to show, e.g., Thomas Lemar and Roberto Firmino
    players_of_interest = ['Thomas Lemar', 'Roberto Firmino Barbosa de Oliveira']
    filtered_players = fifa_cleaned_df[fifa_cleaned_df['name'].isin(players_of_interest)]

    # Create a basic soccer field layout using altair with only the field boundary (no lines in the chart)
    field = alt.Chart(pd.DataFrame({
        'x': [0, 0, 100, 100, 50],
        'y': [0, 100, 0, 100, 50],
        'field': ['left', 'right', 'bottom', 'top', 'center']
    })).mark_rect(color='green', opacity=0.1).encode(
        x='x:Q',
        y='y:Q'
    ).properties(
        title="Soccer Field Layout"
    )

    # Create player positions (adjust coordinates as needed for actual positions)
    positions = {
        'Thomas Lemar': {'x': 20, 'y': 50},
        'Roberto Firmino Barbosa de Oliveira': {'x': 80, 'y': 50},
    }

    # Create a scatter plot of players on the field as dots
    players_chart = alt.Chart(filtered_players).mark_circle(size=100, color="blue").encode(
        x=alt.X('x:Q', scale=alt.Scale(domain=[0, 100]), title="Field X"),
        y=alt.Y('y:Q', scale=alt.Scale(domain=[0, 100]), title="Field Y"),
        tooltip=['name:N', 'nationality:N', 'positions:N', 'overall_rating:Q', 'age:Q']
    ).transform_calculate(
        # Adjusting positions based on player names
        x='datum.name == "Thomas Lemar" ? 20 : datum.name == "Roberto Firmino Barbosa de Oliveira" ? 80 : 50',
        y='datum.name == "Thomas Lemar" ? 50 : datum.name == "Roberto Firmino Barbosa de Oliveira" ? 50 : 50'
    ).properties(
        title="Players in Formation"
    )

    # Combine the soccer field (background) and players (dots)
    combined_chart = field + players_chart
    st.altair_chart(combined_chart, use_container_width=True)

# Add the Formation button to the sidebar
formation_button = st.sidebar.button("Formation", on_click=lambda: switch_page("Formation"))

# Page switching logic
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def switch_page(page: str):
    st.session_state.current_page = page

if st.session_state.current_page == "Formation":
    Formation()

def Data():
    st.subheader("Data Page")
    st.dataframe(fifa_cleaned_df)

# Display the appropriate page based on the current state
if st.session_state.current_page == "Comparison":
    Comparison()
elif st.session_state.current_page == "Barchart":
    Barchart()
elif st.session_state.current_page == "Data":
    Data()
else:
    st.write("Welcome! Use the navigation bar to select a page.")