import datetime
import streamlit as st
import pymysql
import openai
import whisper
import tempfile
import os
from google.cloud import storage
from google.oauth2 import service_account
from io import StringIO

openai.api_key = st.secrets["open_api_key"]

##Hard coded username  take it after login
#username = st.session_state.logged_in_user
###########################################

def chat_gpt(query,prompt):
    response_summary =  openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", 
        messages = [
            {"role" : "user", "content" : f'{query} {prompt}'}
        ]
    )
    return response_summary['choices'][0]['message']['content']
 
def image_generate(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256",
    )
    response_url = []
    response_url.append(response["data"][0]["url"])
    response_url.append(response["data"][1]["url"])
    return(response_url)

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
         
def fetch_patient(username):
    try:
        conn, cursor = database_conn()
        sql_select = "SELECT ID, Gender, Age, Medical_History FROM Patients_Details WHERE Name = %s;"
        record = (username,)
        cursor.execute(sql_select, record)
        result = cursor.fetchone()
        cursor.close()
        return result

    except Exception as error:
        print("Failed to select record from table {}".format(error))
        return False
 
   
def upload_objects(file, filename):
    credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket(st.secrets["bucket_name"])
    blob = bucket.blob("Analysis/" + filename)
    if isinstance(file, str):
        blob.upload_from_filename(file)
    else:
        blob.upload_from_string(file.read(), content_type='text/plain')

class SessionState:
    def __init__(self):
        self.button1_clicked = False
        self.button2_clicked = False
        self.button3_clicked = False
        self.button4_clicked = False

state = SessionState()

# Define the Streamlit UI
def main():
    
    username = 'asd'
    
    
    st.title("Chatbot")
    
    # Add a text input field for user input
    user_input = st.text_input("You", "")
    with st.form("Upload_form", clear_on_submit=True):

        uploaded_file=st.file_uploader("Choose an audio file",type=['mp3'],accept_multiple_files=False)
        submitted = st.form_submit_button("Upload Recording")
        
        with st.spinner('Wait for it...'):
            if uploaded_file is not None and submitted:
                model = whisper.load_model("base")
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file.flush()
                    os.fsync(tmp_file.fileno())
                result = model.transcribe(tmp_file.name)['text']
                os.unlink(tmp_file.name)
                
    # Add a button to send the user input
    send = st.button("Send", key='send')
    
    # Generate response when the user clicks the Send button
    if send and (user_input or uploaded_file):
        #Prompt 
        username = st.session_state.logged_in_user
        response=fetch_patient(username=username)
        string_generated=f"for a person with age = {response[1]}, gender = {response[0]} and medical_history = {response[2]}. Suggest some home remedy and advice. Give many links and reference documents and drugs list."
        if user_input is None:
            st.text_area("You", string_generated)
            gpt_response=chat_gpt(result ,string_generated)
        else:
            st.text_area("You", user_input,key=hash("user_input"))
            gpt_response=chat_gpt(user_input ,string_generated)
            splited=gpt_response.split('.')
            gpt_response = ''
            for i in range(len(splited)):
                if "As an AI language model" in splited[i] or "":
                    continue
                gpt_response+=splited[i]
        # Add user input to conversation history
        import datetime
        ct = datetime.datetime.now()
        filename = f"{username}-{ct}.txt"
        with open(filename, "w") as f:
            f.write(gpt_response)
        upload_objects(filename, filename)
        os.remove(filename)
        st.text_area("Chatbot",gpt_response)
        
        # ##More options
        # col1, col2, col3, col4 = st.columns(4)

        # # if col1.button('Home remedies') and not state.button1_clicked:
        # #     state.button1_clicked = True
        # #     more_remedies= chat_gpt(gpt_response, "Suggest home remedies")
        # #     print(more_remedies)
        # #     st.text_area("Chatbot",gpt_response)
        # with col1:
        #     st.button('Home remedies', key='home_remedies')
        #     if st.session_state.home_remedies:
        #         print('home remedies')
        #         st.write('home remedies')
                # more_remedies = chat_gpt(gpt_response, "Suggest home remedies")
                # print(more_remedies)
                # st.text_area("Chatbot", gpt_response)
        # if col1.button('Home remedies'):
        #     # state.button1_clicked = True
        #     more_remedies= chat_gpt(gpt_response, "Suggest home remedies")
        #     print(more_remedies)
        #     st.text_area("Chatbot",gpt_response)
        
       

        # if col2.button('Simple Reading Material') and not state.button2_clicked:
        #     state.button2_clicked = True
        #     reading_material= chat_gpt(gpt_response, " Give some reading materials")
        #     print(reading_material)
        #     st.text_area("Chatbot",reading_material)

        # if col3.button('Video Links') and not state.button3_clicked:
        #     state.button3_clicked = True
        #     video_links= chat_gpt(gpt_response, " Give some video links")
        #     print(video_links)
        #     st.text_area("Chatbot",video_links)
        
        # if col4.button('Get Images') and not state.button3_clicked:
        #     state.button4_clicked = True
        #     ##Image generation
        #     keywords=chat_gpt(gpt_response,"Give the keywords")
        #     keywords = keywords + string_generated + " counter this situation"
        #     image_url=image_generate(keywords)
        #     st.image(
        #         image_url,
        #         width=400,
        #         use_column_width=True
        #     )

if __name__ == "__main__":
    if "logged_in_user" not in st.session_state:
        st.write("Please login to access this page") 
    elif not st.session_state.logged_in_user:
        st.write("Please login to access this page") 
    else:
        main()