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

    # Example data: lineup of players and their positions
    players = {
        'Goalkeeper': {'name': 'Alisson Becker', 'x': 5, 'y': 50},
        'Left Back': {'name': 'Andrew Robertson', 'x': 20, 'y': 30},
        'Center Back 1': {'name': 'Virgil van Dijk', 'x': 20, 'y': 50},
        'Center Back 2': {'name': 'Joe Gomez', 'x': 20, 'y': 70},
        'Right Back': {'name': 'Trent Alexander-Arnold', 'x': 20, 'y': 90},
        'Defensive Midfielder': {'name': 'Fabinho', 'x': 40, 'y': 50},
        'Central Midfielder 1': {'name': 'Jordan Henderson', 'x': 60, 'y': 30},
        'Central Midfielder 2': {'name': 'Thiago Alcântara', 'x': 60, 'y': 70},
        'Left Wing': {'name': 'Sadio Mané', 'x': 80, 'y': 30},
        'Right Wing': {'name': 'Mohamed Salah', 'x': 80, 'y': 70},
        'Striker': {'name': 'Roberto Firmino', 'x': 90, 'y': 50},
    }

    # Importing mplsoccer to draw the soccer pitch
    from mplsoccer import Pitch

    # Create the pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
    fig, ax = pitch.draw(figsize=(10, 7))

    # Plot each player on the pitch
    for position, player in players.items():
        x, y = player['x'], player['y']
        pitch.scatter(x, y, s=600, color='blue', edgecolors='black', linewidth=1.5, ax=ax)
        ax.text(x, y + 2, player['name'], color='white', ha='center', va='center', fontsize=10, weight='bold')

    # Add a title to the pitch
    ax.set_title("4-3-3 Formation View: FIFA All Star Lineup", fontsize=16, color="white")

    # Display the pitch in Streamlit
    st.pyplot(fig)

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
