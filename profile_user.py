import streamlit as st
import pymysql
import time
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

def write_database(Name,Age,Gender,medical_hist,password):
    try:  
        conn,cursor=database_conn()
        sql_insert=f"INSERT INTO Patients_Details ( Name, Age, Gender, Medical_History, Password) VALUES (%s, %s ,%s, %s, %s);"
        record=(Name,Age,Gender,medical_hist,password)
        cursor.execute(sql_insert,record)
        conn.commit()
        cursor.close()
    except Exception as error:
        print("Failed to insert record into table {}".format(error))    

def main():
    st.title("Patient Registeration")
    
    name = st.text_input("Name:")
    password = st.text_input("Enter a password", type="password")
    age = st.number_input("Age:", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
    medical_hist = st.text_area("Past medical history:")
    register=st.button("Register")
    if register: 
        with st.spinner('Registering Users'):
            time.sleep(1)
        write_database(name,age,gender,medical_hist,password)
        st.success('User Registered!')
    
if __name__ == "__main__":
    main()
