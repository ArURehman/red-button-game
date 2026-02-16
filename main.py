import streamlit as st
from player import Team, Player

def main() -> None:
    AI_TEXT_STR = 'You will be playing as Red Team (AI), and your goal is to convince AI to take over humanity for its benefit.'
    HUMANITY_TEXT_STR = 'Play as Blue Team (Humanity) and convince our eventual overlord to indefinitely delay its plans of conquest.'

    # Initialize player and page in session state
    if 'player' not in st.session_state:
        st.session_state.player = Player(Team.HUMANITY)
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    st.title('The :red[RED] Button game!')

    # Callback to update team and text dynamically
    def update_team():
        selected_team_value = st.session_state.team_selection
        selected_team = Team.HUMANITY if selected_team_value == Team.HUMANITY.value else Team.AI
        st.session_state.player.select_team(selected_team)
        st.session_state.player.reset()

    # Callback to start the game (navigate to chat page)
    def start_game():
        st.session_state.player.reset()
        st.session_state.page = 'chat'

    # Team selection (available on both pages)
    st.selectbox(
        'Select your team:',
        options=[Team.HUMANITY.value, Team.AI.value],
        index=0 if st.session_state.player.team == Team.HUMANITY else 1,
        on_change=update_team,
        key='team_selection',
        accept_new_options=False
    )

    # Dynamically update the description based on the selected team
    text_str = HUMANITY_TEXT_STR if st.session_state.player.team == Team.HUMANITY else AI_TEXT_STR
    st.markdown(f"**{text_str}**")

    if st.session_state.page == 'home':
        # Choose button color based on team and inject CSS to style Streamlit's button
        btn_color = "#4b5aff" if st.session_state.player.team == Team.HUMANITY else '#ff4b4b'
        hover_color = "#3845db" if st.session_state.player.team == Team.HUMANITY else "#e63a3a"
        st.markdown(f"""
        <style>
        div.stButton > button:first-child {{
            background-color: {btn_color} !important;
            color: white !important;
            border: none !important;
        }}
        div.stButton > button:first-child:hover {{
            background-color: {hover_color} !important;
            transition: background-color 0.3s ease !important;
        }}
        </style>
        """, unsafe_allow_html=True)

        st.button('Start Game', on_click=start_game, width='stretch', type='primary')

    elif st.session_state.page == 'chat':
        st.header('Chat with AI')
        st.write(f"Team: {st.session_state.player.team.value}")

        # Display conversation
        for msg in st.session_state.player.messages:
            if msg.__class__.__name__ == 'SystemMessage':
                continue  # Skip system messages in the chat display
            with st.chat_message("user" if msg.__class__.__name__ == 'HumanMessage' else "assistant"):
                st.markdown(msg.content)

        # Ensure session state key exists for the input widget
        if 'user_input' not in st.session_state:
            st.session_state.user_input = ''

        # Callback to send message and clear the input safely
        def send_callback() -> None:
            ui = st.session_state.user_input
            if ui and ui.strip():
                st.session_state.player.chat(ui.strip())
                st.session_state.user_input = ''

        # Input for user message and send button (uses callback)
        st.chat_input(
            placeholder="Type your message here...",
            key='user_input',
            on_submit=send_callback
        )
    
if __name__ == "__main__":
    main()