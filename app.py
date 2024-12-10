import altair as alt
import pandas as pd
import streamlit as st

st.title("FIFA All Star Lineup")
st.markdown("All-star Players with cost analysis")

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

if st.sidebar.button("Formation".upper()):
    switch_page("Formation")

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

def Formation():
    st.subheader("Formation View: Players on the Soccer Field")

    # Define the soccer field layout
    field_lines = pd.DataFrame({
        "x": [
            0, 100, 100, 0, 0,  # Outer boundary
            50, 50,             # Center line
            17, 17, 83, 83, 17,  # Penalty area
            0, 6, 6, 0, 0,      # Left goal area
            100, 94, 94, 100, 100  # Right goal area
        ],
        "y": [
            0, 0, 100, 100, 0,  # Outer boundary
            0, 100,             # Center line
            21, 79, 79, 21, 21,  # Penalty area
            42, 42, 58, 58, 42,  # Left goal area
            42, 42, 58, 58, 42   # Right goal area
        ],
        "group": [
            1, 1, 1, 1, 1,  # Outer boundary
            2, 2,           # Center line
            3, 3, 3, 3, 3,  # Penalty area
            4, 4, 4, 4, 4,  # Left goal area
            5, 5, 5, 5, 5   # Right goal area
        ]
    })

    # Add center circle as a separate layer
    center_circle = pd.DataFrame({
        "x": [50],
        "y": [50],
        "radius": [8]
    })

    # Define players' positions
    players = [
        {"name": "Thomas Lemar", "x": 40, "y": 70, "nationality": "France", "position": "Midfielder", "rating": 85, "age": 27},
        {"name": "Roberto Firmino Barbosa de Oliveira", "x": 50, "y": 30, "nationality": "Brazil", "position": "Forward", "rating": 87, "age": 32},
        {"name": "Virgil van Dijk", "x": 30, "y": 50, "nationality": "Netherlands", "position": "Defender", "rating": 89, "age": 32},
        {"name": "Alisson Becker", "x": 10, "y": 50, "nationality": "Brazil", "position": "Goalkeeper", "rating": 90, "age": 31}
    ]

    players_df = pd.DataFrame(players)

    # Draw field lines
    field_chart = alt.Chart(field_lines).mark_line(color="black").encode(
        x="x:Q",
        y="y:Q",
        detail="group:N"
    ).properties(
        width=600,
        height=400
    )

    # Add center circle
    center_circle_chart = alt.Chart(center_circle).mark_circle(color="black", opacity=0.0).encode(
        x="x:Q",
        y="y:Q",
        size=alt.value(500)

def Data():
    st.subheader("Data Page")
    st.dataframe(fifa_cleaned_df)

# Display the appropriate page based on the current state
if st.session_state.current_page == "Comparison":
    Comparison()
elif st.session_state.current_page == "Barchart":
    Barchart()
elif st.session_state.current_page == "Formation":
    Formation()
elif st.session_state.current_page == "Data":
    Data()
else:
    st.write("Welcome! Use the navigation bar to select a page.")
