# Heuristic Algorithm for Cograph Editing Problem
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) 
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


### Reference Paper:
Wahid, Dewan F; Hassini, Elkafi. User-generated short-text classification using cograph editing-based network clustering with an application in invoice categorization, Data & Knowledge Engineering, 148,102238, 2023.
[[Available Online](https://www.sciencedirect.com/science/article/abs/pii/S0169023X23000988)]


## Project Description
In this repository, we developed an heuristic algorithm for the Cograph Editing  ($P_4$-free) problem (weighted network) based on its integer linear programming (ILP) formulations. Ultimately, this framework allows for the identification of business line-item categories for invoices in a real-world setting.


## Basic Definitions

**Cograph:** A cograph is a $P_4$-free network (i.e., $P_4$ is the forbidden structure) 

**Cograph Editing (CoE) Problem on Weighted Network:** 

***Input:*** A weighted network $G(V,E)$, where $V$ is the set of nodes/vertices, and $E$ is the set of link/edges. 

***Task:*** Find a node partition set $\{P_1, ..., P_k\}$ in $V$ such that each $P\subseteq V$ is a cograph (i.e., $P_4$-free) in network $G^* (V, (E \cup E^+) \setminus E^-)$ with minimized $w(E^+) + w(E^-)$.


## Install Packages 
The requirements.txt file contains list all Python libraries that will require to this project and, they will be installed using:

```
pip install -r requirements.txt
```

## Quick Start

In this repository, `src\heuristic_coe_algo\huristic_algorithm_coe_wn.py` presents proposed heuristic algorithm for the Cograph Editing problems. 

In addition to the heuristic algorithm, the implementation of max-agree and min-error versions of the exact CoE problems given in the follows: `src\exact_algos\exact_coe_max.py` (max-aggre) and `src\exact_algos\exact_coe_min.py` (min-error).


If you have any questions, feel free to email at dfwahid@gmail.com 
