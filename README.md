<h1 align="center">TravelPlanner<br> COMS6998 project<br></h1>

## Note
This code base is adapted from the TravelPlanner's [original code base](https://github.com/OSU-NLP-Group/TravelPlanner). 
We cloned the original code base and made modifications to incorporate our own prompts, evaluation scripts, etc.
This README file is also adapted from the original README where we pruned the content to include only what is relevant for our research.
We also added in additional instructions that is relevant to our project. 

# TravelPlanner

TravelPlanner is a benchmark crafted for evaluating language agents in tool-use and complex planning within multiple constraints.

For a given query, language agents are expected to formulate a comprehensive plan that includes transportation, daily meals, attractions, and accommodation for each day.

For constraints, from the perspective of real world applications, TravelPlanner includes three types of them: Environment Constraint, Commonsense Constraint, and Hard Constraint. 


## Setup Environment

1. Create a conda environment and install dependencies:
```bash
conda create -n travelplanner python=3.9
conda activate travelplanner
pip install -r requirements.txt
```

2. Download the [database](https://drive.google.com/file/d/1pF1Sw6pBmq2sFkJvm-LzJOqrmfWoQgxE/view?usp=drive_link) and unzip it to the `TravelPlanner` directory (i.e., `your/path/TravelPlanner`).

## Running

### Sole-Planning Mode

This mode solely focuses on testing the LLM agent's planning ability.
The sole-planning mode ensures that no crucial information is missed, thereby enabling agents to focus on planning itself.

Please refer to the paper for more details.

```bash
export OUTPUT_DIR=path/to/your/output/file
# We support MODEL in ['gpt-3.5-turbo-X','gpt-4-1106-preview','gemini','mistral-7B-32K','mixtral']
export MODEL_NAME=MODEL_NAME
export OPENAI_API_KEY=YOUR_OPENAI_KEY
# if you do not want to test google models, like gemini, just input "1".
export GOOGLE_API_KEY=YOUR_GOOGLE_KEY
# SET_TYPE in ['validation', 'test']
export SET_TYPE=validation
# STRATEGY in ['direct','cot','react','reflexion', 'greedy', 'prioritize_room_rules', 'allow_budget_overrun', 'allow_budget_overrun_aggressive', 'heuristic', 'backtracking', 'backtracking_with_prioritization']
export STRATEGY=direct

cd tools/planner
python sole_planning.py  --set_type $SET_TYPE --output_dir $OUTPUT_DIR --model_name $MODEL_NAME --strategy $STRATEGY
```

## Postprocess

In order to parse natural language plans, we use gpt-4o-mini to convert these plans into json formats.

```bash
export OUTPUT_DIR=path/to/your/output/file
export MODEL_NAME=MODEL_NAME
export OPENAI_API_KEY=YOUR_OPENAI_KEY
export SET_TYPE=validation
export STRATEGY=direct
export MODE=sole-planning
export TMP_DIR=path/to/tmp/parsed/plan/file
export SUBMISSION_DIR=path/to/your/evaluation/file

cd postprocess
python parsing.py  --set_type $SET_TYPE --output_dir $OUTPUT_DIR --model_name $MODEL_NAME --strategy $STRATEGY --mode $MODE --tmp_dir $TMP_DIR

# Then these parsed plans should be stored as the real json formats.
python element_extraction.py  --set_type $SET_TYPE --output_dir $OUTPUT_DIR --model_name $MODEL_NAME --strategy $STRATEGY --mode $MODE --tmp_dir $TMP_DIR

# Finally, combine these plan files for evaluation. We also provide a evaluation example file "example_evaluation.jsonl" in the postprocess folder.
python combination.py --set_type $SET_TYPE --output_dir $OUTPUT_DIR --model_name $MODEL_NAME --strategy $STRATEGY --mode $MODE  --submission_file_dir $SUBMISSION_DIR
```

## Evaluation

We support the offline validation set evaluation using the provided evaluation script. 

```bash
export SET_TYPE=validation
export EVALUATION_FILE_PATH=your/evaluation/file/path

cd evaluation
python eval.py --set_type $SET_TYPE --evaluation_file_path $EVALUATION_FILE_PATH
```

Using the output from the evaluation script, we are also able to aggregate per-constraint pass rates, similar to what's shown in Table 4 in the paper. To do so, we first copy the outputs into a txt file. An example is shown in `evaluation_results/validation_baseline/constraint_breakdown_raw.txt`.
```bash
export PER_CONSTRAINT_RESULT_FILE_PATH=your/per/constraint/result/file/path
python aggregate_per_constraint_pass_rate.py PER_CONSTRAINT_RESULT_FILE_PATH
```

## Load Datasets

```python
from datasets import load_dataset
# "test" can be substituted by "train" or "validation".
data = load_dataset('osunlp/TravelPlanner','test')['test']
```

## Evaluation results
All evaluation metrics generated for our experiments are included in the repo. They can be found in the `evaluation_results` directory.

## Citation

This code base is adapted from the TravelPlanner's original code base. See citations below:

<a href="https://github.com/OSU-NLP-Group/TravelPlanner"><img src="https://img.shields.io/github/stars/OSU-NLP-Group/TravelPlanner?style=social&label=TravelPanner" alt="GitHub Stars"></a>

```
@inproceedings{xie2024travelplanner,
  title={TravelPlanner: A Benchmark for Real-World Planning with Language Agents},
  author={Xie, Jian and Zhang, Kai and Chen, Jiangjie and Zhu, Tinghui and Lou, Renze and Tian, Yuandong and Xiao, Yanghua and Su, Yu},
  booktitle={Forty-first International Conference on Machine Learning},
  year={2024}
}
```
