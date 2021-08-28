# Import libraries
from PIL import Image
import pandas as pd
import streamlit as st
import sqlite3
st.set_page_config(page_title='COMPaCT', page_icon="🔐",
                   initial_sidebar_state="collapsed")




# FOR PASSWORD HASHING CHECK
# https://www.youtube.com/watch?v=NOojibue-F4

# DB Management
conn = sqlite3.connect("data.db")
c = conn.cursor()

def create_table():
    c.execute(
        'CREATE TABLE IF NOT EXISTS Users(firstname TEXT, lastname TEXT, email TEXT, institution TEXT, username TEXT, password TEXT)')


# def delete_table(table_name):
#     c.execute('DROP TABLE IF EXISTS ?', table_name)


def add_userdata(firstname, lastname, email, institution, username, password):
    c.execute('INSERT INTO Users(firstname, lastname, email, institution, username, password) VALUES (?, ?, ?, ?, ?, ?)',
              (firstname, lastname, email, institution, username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM Users WHERE username=? AND password=?',
              (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM Users')
    data = c.fetchall()
    return data


def main():
    """Modelling light interaction in articular cartilage"""

    st.title("COMPaCT")

    st.subheader("Modelling light propagation in connective tissues")
    st.write("""
             This project aims to provide a simple UI for modelling light 
             propagation in connective tissues. Please create an account to 
             access the app (👈🏼 Sign Up from the sidebar).
    """)
    st.markdown("""---""")
    # delete_table(Users)

    menu = ["Home", "Login", "SignUp"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        image1 = Image.open("/Users/isaaa/Documents/GitHub/synergy-admin/pymc/login/img/MC1080.png")
        image2 = Image.open("/Users/isaaa/Documents/GitHub/synergy-admin/pymc/login/img/MC1450.png")
        
        img1080, img1450 = st.columns(2)
        img1080.image(image1, caption='Photon propagation in cartilage at 1080nm')
        img1450.image(image2, caption='Photon propagation in cartilage at 1450nm')


    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.checkbox("Login"):  # if st.sidebar.button("Login"):
            create_table()
            result = login_user(username, password)

            if result:

                st.success("Logged in as {}".format(username))

                task = st.selectbox("Task",["Add Post", "Analytics", "Manage"])
                if task == "Add Post":
                    st.subheader("Add Your Post")

                elif task == "Analytics":
                    st.subheader("Analytics")

                elif task == "Manage":
                    st.subheader("Manage User Database ")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result, columns = ["Firstname", "Lastname","Username", "Email", "Password"])
                    st.dataframe(clean_db)

            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")

        col_first, col_last = st.columns(2)
        with col_first:
            new_first = st.text_input("First Name")
        with col_last:
            new_last = st.text_input("Last Name")

        col_email, col_addr = st.columns([5,3])
        with col_email:
            new_email = st.text_input("Email")   
        with col_addr:
            new_addr = st.text_input("Institution (University)")


        col_user, col_pw1, col_pw2 = st.columns(3)
        with col_user:
            new_user = st.text_input("Username")
        with col_pw1:
            new_password = st.text_input("Password", type='password', key='pw1')
        with col_pw2:
            rep_password = st.text_input("Repeat Password", type='password', key='pw2')

        col_ch, bl, sub = st.columns(3)
        with col_ch:
            cbx = st.checkbox("I Agree")

        if sub.button("Sign Up"):
            if cbx:
                if new_password == rep_password:
                    create_table()
                    add_userdata(new_first, new_last, new_email, new_addr, new_user, new_password)
                    st.success("Your account has been successfully created 😃")
                    st.balloons()
                    st.info("Go to Login Menu to login")                
                else:
                    st.warning("Passwords are not the same, please check and correct!")
            else:
                st.warning("Please agree to our Terms and Conditions before proceeding.")



if __name__ == '__main__':
    main()
