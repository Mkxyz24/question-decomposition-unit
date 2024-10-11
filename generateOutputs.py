'''
The generate function outputs two files:
1)bartOutput.json which contains the outputs from GPT3 by giving the input from BART decompositions.
2)gpt3OutputWithoutDecomposition.json which contains the outputs from GPT3 for the undecomposed questions.
'''



import json
from difflib import SequenceMatcher
import re
import openai
import os
from dotenv import load_dotenv
import time

def accuracy(true,preds):
    c = 0
    t = len(true)
    for i,j in zip(true,preds):
        if(ord(i.strip())-97 == j):
            c+=1
    return (c/t)

def find_ans_original(prompt,context,options,trueval):
    
    full_prompt = prompt + "\ncontext: " + context +"\noptions: " + options
    time.sleep(1)
    response = openai.Completion.create(engine="text-davinci-003", prompt=full_prompt, max_tokens=128)
    ans = response['choices'][0]['text']
    return find_ans(ans,options,trueval),ans

def find_ans_bart(prompt,context,options,trueval,decompositions):
    example = """context: diana is painting statues . she has 1 / 2 of a gallon of paint remaining . each statue requires 1 / 16 gallon of paint . how many statues can she paint ?
    options: a ) 8 , b ) 20 , c ) 28 , d ) 14 , e ) 19
    subproblem-1: How much paint does one statue require?
    subproblem-2: How much paint does Diana have left?
    subproblem-3: division ! answer of sub-problem 2 ! answer of sub-problem 1
    answer-1: 1/16 gallon
    answer-2: 1/2 gallon
    answer-3: 8 statues
    Final answer: 8"""
    full_prompt =  prompt + "\n" +example
    full_prompt = full_prompt + "\n\ncontext: " + context +"\n\noptions: " + options
    for i,d in enumerate(decompositions):
        full_prompt+="\nSubproblem-"+str(i+1)+": "+ d['question']
    
    time.sleep(1)
    response = openai.Completion.create(engine="text-davinci-003", prompt=full_prompt, max_tokens=128)
    ans = response['choices'][0]['text']
    ans = ans.split('\n')[-1].split(':')[1]
    return find_ans(ans,options,trueval),ans

def find_ans(ans,options,trueval):
    options_l = re.split(',\s+', options)
    max_match = 0
    pred = -1
    for i,option in enumerate(options_l):
        string1 = option.split(')')[1]
        string2 = ans
        match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
        if(match.size>max_match):
            max_match = match.size
            pred = i
    if pred != -1 and pred==(ord(trueval.strip())-97):
        # print('correct')
        pass
    else:
        # print('incorect')
        pass

    return pred

def evaluateBARTvsManual():
    with open('bartDecompositions.json') as f:
        bartDecompositions = json.load(f)
    with open('../task-1/manualDecomposition.json') as f:
        manualDecompositions = json.load(f)
    preds= []
    truths = []
    preds_w= []
    # original_prompt = """Given a problem and 5 options, return the correct option. In order to choose the correct option, you will have to perform some mathematical operations based on the information present in the problem. Look at the examples given below to understand how to answer."""
    bart_prompt = """Given a problem and 5 options, return the correct option. In order to chose the correct option, you have to solve the problem given in the context by using the decomposed questions and performing some mathematical operations . Solve each sub problem sequentially using the answers to previous sub problems and return the final answer."""
    o_original = {}
    for i,instance in enumerate(bartDecompositions):
        pred = find_ans(manualDecompositions[instance]['decomposition'][-1]['answer'],manualDecompositions[instance]['options'],manualDecompositions[instance]['correct'])
        preds.append(pred)
        truths.append(manualDecompositions[instance]['correct'])
        b_context = bartDecompositions[instance]['context']
        b_options = bartDecompositions[instance]['options']
        b_correct = bartDecompositions[instance]['correct']
        b_decomps = bartDecompositions[instance]['decomposition']
        pred_w, ans = find_ans_bart(bart_prompt,b_context,b_options,b_correct,b_decomps)
        preds_w.append(pred_w)
        o_original['instance_'+str(i+1)] = {'context':bartDecompositions[instance]['context'],
                                            'options':bartDecompositions[instance]['options'],
                                            'correct':bartDecompositions[instance]['correct'],
                                            'decomposition':bartDecompositions[instance]['decomposition'],
                                            'answer':ans}

    with open('bartOutput.json','w') as f:
        json.dump(o_original ,f, indent=4, ensure_ascii=False)
        pass
    print(accuracy(truths,preds),"with manual decompositions")
    print(accuracy(truths,preds_w),"with bart decompositions")


def evaluateGPT3vsGroundTruth():
    with open('trainingSamples.json') as f:
        samples = json.load(f)
    
    preds= []
    truths = []
    preds_w= []
    original_prompt = """Given a problem and 5 options, return the correct option. In order to choose the correct option, you will have to perform some mathematical operations based on the information present in the problem. Look at the examples given below to understand how to answer."""
    o_original = {}
    for i,instance in enumerate(samples):
        pred = find_ans(samples[instance]['decompositions'][-1]['answer'],samples[instance]['options'],samples[instance]['correct'])
        preds.append(pred)
        truths.append(samples[instance]['correct'])
        pred_w, ans = find_ans_original(original_prompt, samples[instance]['context'],samples[instance]['options'],samples[instance]['correct'])
        preds_w.append(pred_w)
        o_original['instance_'+str(i+1)] = {'context':samples[instance]['context'],
                                            'options':samples[instance]['options'],
                                            'correct':samples[instance]['correct'],
                                            'answer':ans.strip("\n")}

    with open('gpt3OutputWithoutDecomposition.json','w') as f:
        json.dump(o_original ,f, indent=4, ensure_ascii=False)
    print(accuracy(truths,preds),"with decompositions")
    print(accuracy(truths,preds_w),"without decompositions")




if __name__ == '__main__':

    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API')
    evaluateBARTvsManual()
    evaluateGPT3vsGroundTruth()
