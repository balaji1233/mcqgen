import os
import json
import PyPDF2
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdfReader = PyPDF2.PdfReader(file)
            text = ""
            for i in range(len(pdfReader.pages)):
                text += page.extractText()
            return text
        except Exception as e:
            raise Exception("Error reading the file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(" unsupported file format only .txt and .pdf files are supported") 
    


def get_table_data(quiz_str):
    try:
        #convert the quiz  from a str to dict

        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]


        #iterate through the quiz_dict and extract the required information
        for key,value in quiz_dict.items():
            mcq=value['mcq']
            options=" || ".join(
                [
                    f"{option}->{option_value}" for option,option_value in value['options'].items()
                ]
            )


            correct=value['correct']
                          
            quiz_table_data.append({"MCQ":mcq,"Choices":options,"Correct":correct})

        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(  type(e), e, e.__traceback__)
        return False