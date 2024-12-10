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
    
    # Retrieve previous selections from session state, or set default values
    selected_x_var = st.session_state.get("selected_x_var", x_choices[0])
    selected_y_var = st.session_state.get("selected_y_var", y_choices[0])

    # Allow users to select X and Y axis variables
    selected_x_var = st.selectbox("Select X-axis variable:", x_choices, index=x_choices.index(selected_x_var))
    selected_y_var = st.selectbox("Select Y-axis variable:", y_choices, index=y_choices.index(selected_y_var))

    # Store the selected values in session state to persist them
    st.session_state.selected_x_var = selected_x_var
    st.session_state.selected_y_var = selected_y_var

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
    
    # Retrieve the selected club from session state, or set the default value
    selected_club = st.session_state.get("selected_club", allowed_club_teams[0])

    # Selection box for club teams, limited to the allowed list
    selected_club = st.selectbox(
        "Select a Club Team:",
        options=allowed_club_teams,
        index=allowed_club_teams.index(selected_club)
    )

    # Store the selected club in session state to persist it
    st.session_state.selected_club = selected_club

    # Filter the data for the selected club team
    filtered_data = fifa_cleaned_df[fifa_cleaned_df['club_team'] == selected_club]

    # Dropdown for selecting the Y-axis variable
    y_var = st.session_state.get("selected_y_var_barchart", "overall_rating")

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

    # Store the selected Y-axis variable in session state to persist it
    st.session_state.selected_y_var_barchart = y_var

def Formation():
    st.subheader("Formation View: All-Star Lineup")

    formation = {
        "GK": fifa_cleaned_df[fifa_cleaned_df["positions"].str.contains("GK")].nlargest(1, "overall_rating"),
        "LB": fifa_cleaned_df[fifa_cleaned_df["positions"].str.contains("LB")].nlargest(1, "overall_rating"),
        "CB1": fifa_cleaned_df[fifa_cleaned_df["positions"].str.contains("CB")].nlargest(1, "overall_rating"),
        "CB2": fifa_cleaned_df[fifa_cleaned_df["positions"].str.contains("CB")].nlargest(2, "overall_rating").iloc[1:],
        "RB": fifa_cleaned_df[fifa_cleaned_df["positions"].str.contains("RB")].nlargest(1, "overall_rating"),
        "CM1": fifa_cleaned_df[fifa_cleaned_df["positions"].str.contains("CM")].nlargest(1, "overall_rating"),
        "CM2": fifa_cleaned_df[fifa_cleaned_df["positions"].str.contains("CM")].nlargest(2, "overall_rating").iloc[1:],
        "LW": fifa_cleaned_df[fifa_cleaned_df["positions"].str.contains("LW")].nlargest(1, "overall_rating"),
        "ST": fifa_cleaned_df[fifa_cleaned_df["positions"].str.contains("ST")].nlargest(1, "overall_rating"),
        "RW": fifa_cleaned_df[fifa_cleaned_df["positions"].str.contains("RW")].nlargest(1, "overall_rating"),
        "CDM": fifa_cleaned_df[fifa_cleaned_df["positions"].str.contains("CDM")].nlargest(1, "overall_rating"),
    }
    
    lineup = pd.concat(formation.values(), ignore_index=True)
    
    # Calculate the sum of value_euro for the selected players
    total_value = lineup["value_euro"].sum()

    # Display the total value below the formation chart
    st.write(f"Total Value: €{total_value:,.2f}")
    
    # Define positions on the soccer pitch
    pitch_positions = {
        "GK": (50, 10),
        "LB": (15, 30),
        "CB1": (35, 30),
        "CB2": (65, 30),
        "RB": (85, 30),
        "CM1": (35, 60),
        "CM2": (65, 60),
        "LW": (15, 90),
        "ST": (50, 90),
        "RW": (85, 90),
        "CDM": (50, 50),
    }
    
    # Add pitch coordinates to the lineup dataframe
    lineup["x"] = [pitch_positions[pos][0] for pos in pitch_positions]
    lineup["y"] = [pitch_positions[pos][1] for pos in pitch_positions]
    
    # Draw the soccer pitch
    field = alt.Chart(pd.DataFrame({
        "x": [0, 100, 100, 0, 0],
        "y": [0, 0, 100, 100, 0]
    })).mark_line(color="green", strokeWidth=5).encode(
        x="x:Q", y="y:Q"
    ).properties(width=600, height=400)
    
    # Add player positions as points (without x and y in the tooltip)
    players = alt.Chart(lineup).mark_circle(size=200, color="blue").encode(
        x="x:Q",
        y="y:Q",
        tooltip=["name", "positions", "overall_rating", "club_team"]  # Removed x and y
    )
    
    # Add player names as text
    text = alt.Chart(lineup).mark_text(align="center", fontSize=12, color="white").encode(
        x="x:Q",
        y="y:Q",
        text="name",
        tooltip=["name", "positions", "overall_rating", "club_team",]
    )
    
    # Combine the pitch, players, and text into one chart
    formation_chart = field + players + text
    st.altair_chart(formation_chart, use_container_width=True)

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
