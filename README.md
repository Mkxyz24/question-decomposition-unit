# Project: Building Question Decomposition Unit using Large Language Models (LLMs)

We are building a new model every few months BERT, RoBERTa, GPT2, T5, GPT3…
As a new dataset comes, we build a new model to solve the task. Recent works show that: If we learn to decompose a complex question perfectly and divide it into a set of simple questions, the task can be solved with a simple model.

## Example

<p align='center'>
  <img width="319" alt="project_20" src="https://user-images.githubusercontent.com/47143544/139757837-90d41e9f-c2f6-41d3-856b-c97cb494635d.png">
</p>

This example is taken from the DROP dataset. As you can see, if we decompose a question, it becomes easier to answer the question rather than directly infer from context. In this project, your goal is to check if this kind of decomposition helps or not.

## Literature to Read

1. [Is a Question Decomposition Unit All We Need?](https://arxiv.org/abs/2205.12538)
2. [Text Modular Networks: Learning to Decompose Tasks in the Language of Existing Models](https://arxiv.org/abs/2009.00751)
3. [Least-to-Most Prompting Enables Complex Reasoning in Large Language Models](https://arxiv.org/abs/2205.10625)

Note: If you do not have any basic idea about prompting, then read Sections 2,4,6 and 7 from [Pre-train, Prompt, and Predict](https://arxiv.org/abs/2107.13586)

