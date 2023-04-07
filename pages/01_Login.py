import streamlit as st
import pymysql

def database_conn():
    try:  
        conn = pymysql.connect(
                host = st.secrets["host"], 
                user = st.secrets["user"],
                password = st.secrets["password"],
                db = st.secrets["db"])
        cursor = conn.cursor()
        return conn,cursor
    except Exception as error:
        print("Failed to connect to database {}".format(error))
         
def login_database(username, password):
    try:
        conn, cursor = database_conn()
        sql_select = "SELECT Password FROM Patients_Details WHERE Name = %s;"
        record = (username,)
        cursor.execute(sql_select, record)
        result = cursor.fetchone()
        cursor.close()

        if result is not None and result[0] == password:
            return True
        else:
            return False

    except Exception as error:
        print("Failed to select record from table {}".format(error))
        return False


# Define the Streamlit app
def main():
    
    if "logged_in_user" not in st.session_state:
        st.session_state['logged_in_user'] = False

    # Add a title to the app
    st.title("Patient Login")
    
    # Create input fields for the username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Create a button to submit the login credentials
    if st.button("Login"):
        # Check if the username and password are valid
        login_status=login_database(username,password)
        if login_status: 
            ###Move to the main page 
            st.session_state.logged_in_user = username
            st.write("success")
        else:
            st.write("Login Failed")
            
if __name__ == "__main__":
    main()