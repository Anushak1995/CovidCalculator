
import psycopg2

import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import json
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import pandas as pd
import re
from flask_sqlalchemy import SQLAlchemy
from datetime import date
#from config import config

l_email=""
APP = Flask(__name__)

#-----------------------start page---------------------------------
@APP.route('/')
def home():
    print("here start")
    return render_template('index1.html')

#-----------------------------------------------signup----------------
@APP.route('/signup', methods=['POST'])
    
def signingup():
    print("here signup1")
    '''
    For rendering results on HTML GUI
    '''
    ##taking input given by user in form to int_feature dataframe using request
    #print(request.form.getlist())
    int_features = [x for x in request.form.values()]
    print(int_features)
    
    p_name = int_features[0]
    p_email=int_features[1]
    p_password=int_features[2]
    #print("here"+p_name)
    

#     """ create tables in the PostgreSQL database"""
#     commands = (
#         """
#         CREATE TABLE USER_PROFILE (
#             USER_NAME VARCHAR(100) PRIMARY KEY,
#             EMAIL_ADDRESS VARCHAR(255),
#             PASS_WORD VARCHAR(100)
#         )
#         """
#                )
    print("here1")
    
    
    command_in = """ INSERT INTO USER_PROFILE (USER_NAME,EMAIL_ADDRESS,PASS_WORD) VALUES (%s,%s,%s);"""
    command_select= """ select email_Address from user_profile;"""
    #conn = None
    try:
        # read the connection parameters
        #params = config()
        # connect to the PostgreSQL server
        print("here2")

#------------------------db conncetion local--------------
        #conn =  psycopg2.connect("dbname=covidcal user=postgres password=AK1234")
#----------------------db connection host------------------------------------
         conn = psycopg2.connect(
             host="ec2-44-199-22-207.compute-1.amazonaws.com",
             database="d9m6c77v184dph",
             user="daolbbnurgtgwd",
             password="de4a06735c26a7aca7ae26f165e93e3f635e6caaee0681bf4fdeafb68e94586d")
        cur = conn.cursor()
        print("here3")
        # create table one by one
        #for command in commands[:-1]:
        print("here4")
#-----------------------to get presently stored values-------------------------
        df=pd.read_sql(command_select,conn)
        print (df)
         
   #-------------------------checking if stored value= new input----------------------
        check_email=0
        for i in range(len(df)):
            if df.loc[i, "email_address"]==p_email:
                check_email=check_email+1  
                
               
 #---------------------------inserting input from form in table --------------------
        
        if check_email==0:
            record_to_insert = (p_name, p_email, p_password)
            cur.execute(command_in,record_to_insert)
            t_message = "Signup successful, please login with your credentials"
        else:
            t_message = "This email address is taken, please login or try using new email"
            return render_template("index1.html", message = t_message)
        print("here5")
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        return render_template("index1.html", message = t_message)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#-----------------------------------------------login--------------------------------------
@APP.route('/login', methods=['POST'])

def login():
        #print("here login")
        '''
        For rendering results on HTML GUI
        '''
    ##taking input given by user in form to int_feature dataframe using request
    #print(request.form.getlist())
        int_features_login = [x for x in request.form.values()]
        print(int_features_login)

        global l_email
        l_email=int_features_login[0]
        l_password=int_features_login[1]
        print(l_email)
        #print("here login1")
        
        userResultCount=getUserResultCount(l_email)
        ##userResult = getUserResult(l_email)
        print(userResultCount)
        print("COUNT SHOWN")
    
     
        login_select= """ select email_Address,pass_word from user_profile;"""
        try:
        # read the connection parameters
        #params = config()
        # connect to the PostgreSQL server
            #print("here login2")

#------------------------db conncetion local--------------
            #conn =  psycopg2.connect("dbname=covidcal user=postgres password=AK1234")
#----------------------db connection host------------------------------------
          conn = psycopg2.connect(
              host="ec2-44-199-22-207.compute-1.amazonaws.com",
              database="d9m6c77v184dph",
              user="daolbbnurgtgwd",
              password="de4a06735c26a7aca7ae26f165e93e3f635e6caaee0681bf4fdeafb68e94586d")
            cur = conn.cursor()
            print("here login3")
        # create table one by one
        #for command in commands[:-1]:
        #print("here l4")
#-----------------------to get presently stored values-------------------------
            df=pd.read_sql(login_select,conn)
            #print (df)
            cur.close()
            conn.commit()
   #-------------------------checking if stored value= new input----------------------
            login_email=0
            for i in range(len(df)):
                if df.loc[i, "email_address"]==l_email and df.loc[i, "pass_word"]==l_password :
                    login_email=login_email+1  
                
            
 #---------------------------inserting input from form in table --------------------
            cnt_message="No result available"
            if login_email==1:
                if int(userResultCount)>0:
                    userResult = getUserResult(l_email)
                    return render_template("index.html", userResult=userResult, arrRange=range(len(userResult)))
                else:
                    return render_template("index.html", message_cnt = cnt_message)
                #t1_message = "login successful"
                #return render_template("index1.html", message_log = t1_message)
                 
            else:
                t1_message = "Wrong credential, please try again"
                return render_template("index1.html", message_1 = t1_message)
            #print("here5")
        # close communication with the PostgreSQL database server
        #cur.close()
        # commit the changes
        #conn.commit()
        #return render_template("index1.html", message = t_message)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

@APP.route('/submit', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    ##taking input given by user in form to int_feature dataframe using request
    #print(request.form.getlist())
    int_features = [x for x in request.form.values()]
    print(int_features)
    #outputProbability = 5

    #data = {
    #    'shouldShowResult': True,
    #    'Probability': outputProbability
    #}

    # Generate universe variables
    #defining inputs
    x_fever = np.arange(96, 105, 1)
    x_cough = np.arange(0, 6, 1)
    x_rd  = np.arange(0,6,1)
    x_output= np.arange(0, 11, 1)
    print("here1")
    #generate fuzzy mf
    fever_abs= fuzz.trimf(x_fever, [96, 96, 99])
    fever_low = fuzz.trimf(x_fever, [98, 100, 102])
    fever_high=fuzz.trimf(x_fever, [101, 104, 104])

    cough_abs= fuzz.trapmf(x_cough,[0,0,0,2])
    cough_low = fuzz.trapmf(x_cough, [1, 2,3, 4])
    cough_high=fuzz.trapmf(x_cough, [3, 5, 5,5])

    rd_abs= fuzz.trapmf(x_rd,[0,0,0,2])
    rd_low = fuzz.trapmf(x_rd, [1, 2,3, 4])
    rd_high=fuzz.trapmf(x_rd, [3, 5, 5,5])

    output_noneed=fuzz.trimf(x_output, [0, 0,3])
    output_isolation=fuzz.trimf(x_output, [2, 4, 6])
    output_testimm=fuzz.trimf(x_output, [5, 10, 10])

    print("here2")
    #pip install pyit2fls
    from pyit2fls import zero_mf, singleton_mf, const_mf, tri_mf, ltri_mf, rtri_mf, trapezoid_mf, gaussian_mf
    from numpy import linspace


    x_tastelessness = linspace(0, 1, 1001)
    tastelessness_singleton = singleton_mf(x_tastelessness, [1, 1])

    x_fatigue = linspace(0, 1, 1001)
    fatigue_singleton = singleton_mf(x_fatigue, [1, 1])

    x_headache = linspace(0, 1, 1001)
    headache_singleton = singleton_mf(x_headache, [1, 1])

    x_bodypain = linspace(0, 1, 1001)
    bodypain_singleton = singleton_mf(x_bodypain, [1, 1])

    x_losssmell = linspace(0, 1, 1001)
    losssmell_singleton = singleton_mf(x_losssmell, [1, 1])

    x_diarrhoea = linspace(0, 1, 1001)
    diarrhoea_singleton = singleton_mf(x_diarrhoea, [1, 1])
    print("here3")
    #P_name = int_features[0]
    #p_email=int_features[1]
    in_fever=int_features[0]
    in_cough=int_features[1]
    in_rd=int_features[2]
    in_tastelessness=int_features[3]
    in_fatigue=int_features[4]
    in_headache=int_features[5]
    in_bodypain=int_features[6]
    in_losssmell=int_features[7]
    in_diarrhoea=int_features[8]

    print("here4")
    in_fever_abs= fuzz.interp_membership(x_fever, fever_abs, in_fever)
    in_fever_low= fuzz.interp_membership(x_fever, fever_low, in_fever)
    in_fever_high= fuzz.interp_membership(x_fever, fever_high, in_fever)

    in_cough_abs=fuzz.interp_membership(x_cough, cough_abs, in_cough)
    in_cough_low=fuzz.interp_membership(x_cough, cough_low, in_cough)
    in_cough_high=fuzz.interp_membership(x_cough, cough_high, in_cough)

    in_rd_abs=fuzz.interp_membership(x_rd, rd_abs, in_rd)
    in_rd_low=fuzz.interp_membership(x_rd, rd_low, in_rd)
    in_rd_high=fuzz.interp_membership(x_rd, rd_high, in_rd)

    in_tastelessness_val=fuzz.interp_membership(x_tastelessness, tastelessness_singleton, in_tastelessness)
    print("here5")
    in_tastelessness_no=0
    in_tastelessness_yes=1
    if in_tastelessness_val < 0.5:
        in_tastelessness_no = 1
        in_tastelessness_yes=0
    else:
        in_tastelessness_no=0
        in_tastelessness_yes = 1

    in_fatigue_val=fuzz.interp_membership(x_fatigue, fatigue_singleton, in_fatigue)

    in_fatigue_no=0
    in_fatigue_yes=1
    if in_fatigue_val < 0.5:
        in_fatigue_no = 1
        in_fatigue_yes=0
    else:
        in_fatigue_no=0
        in_fatigue_yes = 1

    in_headache_val=fuzz.interp_membership(x_headache, headache_singleton, in_headache)

    in_headache_no=0
    in_headache_yes=1
    if in_headache_val < 0.5:
        in_headache_no = 1
        in_headache_yes=0
    else:
        in_headache_no=0
        in_headache_yes = 1

    in_bodypain_val=fuzz.interp_membership(x_bodypain, bodypain_singleton, in_bodypain)
    print("here6")
    in_bodypain_no=0
    in_bodypain_yes=1
    if in_bodypain_val < 0.5:
        in_bodypain_no = 1
        in_bodypain_yes=0
    else:
        in_bodypain_no=0
        in_bodypain_yes = 1


    in_losssmell_val=fuzz.interp_membership(x_losssmell, losssmell_singleton, in_losssmell)

    in_losssmell_no=0
    in_losssmell_yes=1
    if in_losssmell_val < 0.5:
        in_losssmell_no = 1
        in_losssmell_yes=0
    else:
        in_losssmell_no=0
        in_losssmell_yes = 1

    in_diarrhoea_val=fuzz.interp_membership(x_diarrhoea, diarrhoea_singleton, in_diarrhoea)

    print("here7")
    in_diarrhoea_no=0
    in_diarrhoea_yes=1
    if in_diarrhoea_val < 0.5:
        in_diarrhoea_no = 1
        in_diarrhoea_yes=0
    else:
        in_diarrhoea_no=0
        in_diarrhoea_yes = 1

    print("here8")
    #defining rules
    rule_1=np.fmax(in_tastelessness_yes,in_losssmell_yes)
    rule_2=np.fmax(in_rd_low,in_rd_high)
    rule_3=np.fmin(np.fmin(np.fmin(in_fever_abs, np.fmin(in_cough_abs,in_rd_abs)),in_tastelessness_no),in_losssmell_no)
    rule_4=np.fmin(np.fmin(np.fmin(np.fmax(in_fever_low,in_fever_high),in_cough_abs),in_rd_abs),in_headache_no)
    rule_5=np.fmin(np.fmin(np.fmin(in_fever_abs,in_cough_low),in_rd_abs),in_headache_no)
    rule_6=np.fmin(np.fmin(np.fmax(in_fever_low,in_fever_high),np.fmax(in_cough_low,in_cough_high)),np.fmax(in_rd_low,in_rd_high))
    rule_7=np.fmin(np.fmax(in_fever_high,in_fever_low),np.fmax(in_cough_low,in_cough_high))

    #rulewise output
    rule_1_2=np.fmax(rule_1,rule_2)
    rule_1_2_6=np.fmax(rule_1_2,rule_6)
    rule_1_2_6_7=np.fmax(rule_1_2_6,rule_7)
    active_output_testimm=np.fmin(rule_1_2_6_7,output_testimm)


    rule_4_5=np.fmax(rule_4,rule_5)
    active_output_isolation=np.fmin(rule_4_5,output_isolation)


    active_output_noneed=np.fmin(rule_3,output_noneed)

    ##working with output

    op0 = np.zeros_like(x_output)

    #aggregating output

    agg_op=np.fmax(np.fmax(active_output_testimm,active_output_isolation),active_output_noneed)

    #defuzzification--centroid
    defuzz_centroid=fuzz.defuzz(x_output, agg_op, 'centroid')

    #defuzzification--bisector
    defuzz_bisector=fuzz.defuzz(x_output, agg_op, 'bisector')

    #defuzzification--mom
    defuzz_mom = fuzz.defuzz(x_output, agg_op, 'mom')

    #defuzzification--som
    defuzz_som = fuzz.defuzz(x_output, agg_op, 'som')

    #defuzzification--lom
    defuzz_lom = fuzz.defuzz(x_output, agg_op, 'lom')

    print("here5")
    output=round(defuzz_centroid)
    if output<=3:
        x="Your possibility to be covid positive is "
        y=" in a scale of 10. You do not require a test now"
        z=x+str(output)+y
        print(x+str(output)+y)
    if  3<output<=5:
        x="Your possibility to be covid positive is "
        y=" in a scale of 10. Please stay in isolation and remain vigilant"
        z=x+str(output)+y
        print(x+str(output)+y)
    if  output>5:
        x="Your possibility to be covid positive is "
        y=" in a scale of 10. Please test immediately and consult specialist"
        z=x+str(output)+y
        print(x+str(output)+y)
    
    today = date.today()
    result_to_insert = (today,l_email, str(output))    
        
    command_in_result = """ INSERT INTO USER_RESULT (test_Date,EMAIL_ADDRESS,result_txt) VALUES (%s,%s,%s);"""
    #conn = None
    try:
        # read the connection parameters
        #params = config()
        # connect to the PostgreSQL server
        print("here2")

#------------------------db conncetion local--------------
        #conn =  psycopg2.connect("dbname=covidcal user=postgres password=AK1234")
#----------------------db connection host------------------------------------
        conn = psycopg2.connect(
              host="ec2-44-199-22-207.compute-1.amazonaws.com",
              database="d9m6c77v184dph",
              user="daolbbnurgtgwd",
              password="de4a06735c26a7aca7ae26f165e93e3f635e6caaee0681bf4fdeafb68e94586d")
        cur = conn.cursor()
        print("here3")
        # create table one by one
        #for command in commands[:-1]:
        print("here4")

        cur.execute(command_in_result,result_to_insert)

        print("here5")
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        #return render_template("index.html")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
    userResult = getUserResult(l_email)
    return render_template('index.html', prediction_text=z, userResult=userResult, arrRange=range(len(userResult)))



def getUserResultCount(email):
    userResultQuerycnt = '''
SELECT count(*) cnt
 FROM USER_RESULT A
Where email_address = '{email}'
    '''.format(email=email)
    print(userResultQuerycnt)
    try:
        #conn =  psycopg2.connect("dbname=covidcal user=postgres password=AK1234")
#----------------------db connection host------------------------------------
          conn = psycopg2.connect(
              host="ec2-44-199-22-207.compute-1.amazonaws.com",
              database="d9m6c77v184dph",
              user="daolbbnurgtgwd",
              password="de4a06735c26a7aca7ae26f165e93e3f635e6caaee0681bf4fdeafb68e94586d")
        cur = conn.cursor()
        print("here in count login3")
        # create table one by one
        #for command in commands[:-1]:
        #print("here l4")
#-----------------------to get presently stored values-------------------------
        df1=pd.read_sql(userResultQuerycnt,conn)
        cnt=df1.loc[0, "cnt"]
        print (cnt)
        cur.close()
        #return df1
        return cnt
    except:
        print("tried")
    finally:
        if conn is not None:
            conn.close()

def getUserResult(email):
    userResultQuery = '''
SELECT TEST_DATE, RESULT_TXT FROM 
(SELECT ROW_NUMBER( )OVER (PARTITION BY EMAIL_ADDRESS ORDER BY TEST_DATE DESC) AS RNM
 , A.*
 FROM USER_RESULT A
) B
Where email_address = '{email}' AND rnm<=3
 order by rnm DESC
    '''.format(email=email)
    print(userResultQuery)
    try:
        #conn =  psycopg2.connect("dbname=covidcal user=postgres password=AK1234")
#----------------------db connection host------------------------------------
          conn = psycopg2.connect(
              host="ec2-44-199-22-207.compute-1.amazonaws.com",
              database="d9m6c77v184dph",
              user="daolbbnurgtgwd",
              password="de4a06735c26a7aca7ae26f165e93e3f635e6caaee0681bf4fdeafb68e94586d")
        cur = conn.cursor()
        print("here login3")
        # create table one by one
        #for command in commands[:-1]:
        #print("here l4")
#-----------------------to get presently stored values-------------------------
        df=pd.read_sql(userResultQuery,conn)
        #print (df)
        cur.close()
        return df
    except:
        print("tried")
    finally:
        if conn is not None:
            conn.close()


        
    
    
# #if __name__ == '__main__':
#   #  create_tables()
    
    
if __name__ == "__main__":
    APP.run() 
   
