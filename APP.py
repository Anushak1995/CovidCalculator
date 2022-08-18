#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import json
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import pandas as pd
import re


# In[2]:


APP = Flask(__name__)


# In[3]:


@APP.route('/')
def home():
    return render_template('index.html')


# In[ ]:


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
    
    P_name = int_features[0]
    p_email=int_features[1]
    in_fever=int_features[2]
    in_cough=int_features[3]
    in_rd=int_features[4]
    in_tastelessness=int_features[5]
    in_fatigue=int_features[6]
    in_headache=int_features[7]
    in_bodypain=int_features[8]
    in_losssmell=int_features[9]
    in_diarrhoea=int_features[10]
    
    
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


    in_diarrhoea_no=0
    in_diarrhoea_yes=1
    if in_diarrhoea_val < 0.5:
        in_diarrhoea_no = 1
        in_diarrhoea_yes=0
    else:
        in_diarrhoea_no=0
        in_diarrhoea_yes = 1


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

    
    output=round(defuzz_centroid)
    if output<=3:
        x="Your possibility to be covid positive is "
        y=" in a scale of 10. You donot require a test now"
        z=x+str(output)+y
        #print(x+str(output)+y)
    if  3<output<=5:
        x="Your possibility to be covid positive is "
        y=" in a scale of 10. Please stay in isolation and remain vigilant"
        z=x+str(output)+y
        #print(x+str(output)+y)
    if  output>5:
        x="Your possibility to be covid positive is "
        y=" in a scale of 10. Please test immediately and consult specialist"
        z=x+str(output)+y
        #print(x+str(output)+y)

    
    
    return render_template('index.html', prediction_text='Result: {}'.format(z))
    #print('i am here')
    
if __name__ == "__main__":
    APP.run(debug=True) 


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




