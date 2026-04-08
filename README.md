# Soft Fuzzy Number-Valued Fuzzy Graph (SFNVFG)

This repository contains the Python implementation and output data supporting the manuscript:

**“Soft Fuzzy Number-Valued Fuzzy Graph: A Novel Hybrid Approach to Uncertainty Modeling”**

## Overview
The code constructs and analyzes SFNVFGs using triangular fuzzy numbers. It performs α-cut analysis, supports both user-defined and automatically generated α-values, and performs parameter-wise graph analysis, including included and borderline vertices.

## Requirements
Install dependencies using:

pip install -r requirements.txt

## Input
An Excel file with two sheets:
- **Vertices:** Vertex, Parameter, l, m, r  
- **Edges:** Source, Target, Parameter, l, m, r  

## Usage
Run the script and provide:
- Excel file path  
- Number of α-values (0 for automatic generation)  

## Output
Results are printed and saved as:

`sfnvfg_results.xlsx`

## Data Availability
All data and code used in this study are available in this repository.
