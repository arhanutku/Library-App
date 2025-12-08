---
title: Library Author Search
emoji: "\U0001f4da"
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
license: mit
pinned: false
---

# Library Author Search

## Demo screenshots of testing
Here are three example views of the app: ![](Use1.png) ![](Use2.png) ![](Use3.png)

## Problem Breakdown & Computational Thinking
**Decomposition:** The app reads `books.csv`, turns each row into a `Book` object, sorts the books by author, builds a distinct author list, searches for matches, and presents the results in the UI.  
**Pattern Recognition:** The merge sort repeats the same compare and append steps at every level, and the search uses lower and upper bounds from binary search to find the author.  
**Abstraction:** Users see the author list and the matched books.
**Algorithm Design:** Merge sort keeps the authors in a stable order, and binary search finds the correct author range in logarithmic time.  
Flowchart: ![FlowChart](flowchart.png)

## Steps to Run
1. On Hugging Face Spaces, upload `app.py`, `books.csv`, `requirements.txt`, and this `README.md` to a Gradio Space. The Space installs the dependencies and starts the UI automatically at `https://huggingface.co/spaces/Arhan-U/Library_App`.
2. For local UI use, run `pip install -r requirements.txt`, then run `python app.py` and open the Gradio link that appears in the console.
3. For local CLI use, run `python app.py --cli` to search through the terminal. This mode is meant for local use and is not used on Spaces.

## Hugging Face Link
https://huggingface.co/spaces/Arhan-U/Library_App

## Author & Acknowledgment
Author: Arhan B. Utku  
Hugging Face Spaces and Gradio for hosting and tooling. Google and Reddit were consulted for finding solutions to problems that appeared while coding.