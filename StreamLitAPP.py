import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st  
from langchain.callbacks import get_openai_callback
from src.mcqgenerator import MCQGenerator import generate_evaluate_chain

from src.mcqgenerator.logger import logging


#loading Json files
with open('F:\mcqgen\Response.json','r') as file:
    RESPONSE_JSON = json.load(file)      


#Creatinga title for the app
st.title("MCQ Generator Application With langchain")

#create  a form using st.form
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Upload aPDF or txt  file")


    #Input Fields
    mcq_count =  st.number_input("Number of MCQs to generate",min_value=3,max_value=50)

    #Subject
    subject = st.text_input("Insert Subject",max_chars=20)


    ##Quiz Tone

    tone=st.txt_input("Complexity Level Of Questions",max_chars=20,placeholder="Simple")

    #Add Button
    button=st.form_sublit("Create MCQs")

    #Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
       with st.spinner("loading..."):
              try:
                #Read the uploaded file
                text=read_file(uploaded_file)
                #count tokens and the count of API call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                        "text":text,
                        mcq_count:mcq_count,
                        subject:subject,
                        tone:tone,
                        "respinse_json":json.dumps(RESPONSE_JSON)
                        }

                    )

                    #st.write(response)
                except Exception as e:
                       traceback.print_exception( type(e), e, e.__traceback__)
                

                       st.error("Error")
              else:
print("Total Toekns:{cb.total_toekns}")

print(f"Prompt Tokens:{cb.prompt_tokens}")
print(f"Completion Tokens:{cb.completion_tokens}")
print( f"Total Cost::{cb.total_cost}")
if isinstance(response,dict):

    #Extract the quiz from the response
    quiz=response.get("quiz",None)
    if quiz is not None:
        table_data=get_table_data(quiz)
        if table_data is not None:
            df=pd.DataFrame(table_data)
            df.index=df.index+1
            st.table(df)
            #Display the review in atext box as well
            st.text_area( label="Review",value=response.get("review",""))
        else:
            st.error("Error in the table data")

    else:
        st.write(response)
        




           
           
         
        