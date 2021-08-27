import streamlit as st
from multiapp import MultiApp
from apps import home, data, model, data_stats # import your app modules here

app = MultiApp()

st.markdown(
    """
    # Multi-Page App

    This multi-page app is using the streamlit-multiapps framework by Praneel Nihar.

    """
)


# Add all your application here
app.add_app("Home", home.app)
app.add_app("Data", data.app)
app.add_app("Data Stats", data_stats.app)
app.add_app("Model", model.app)
# The main app
app.run()