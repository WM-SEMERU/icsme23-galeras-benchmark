# %% [markdown]
# ### Pylint codesmells analysis

# %%
import json
import subprocess
import os
import glob

# %%
def analyze_code_snippet(code):
    # Save the code to a temporary file with UTF-8 encoding
    with open('temp.py', 'w', encoding='utf-8') as temp_file:
        temp_file.write(code)

    command = [
        'pylint',
        'temp.py',
        #'--disable=all',
        #'--enable=bad-chained-comparison,bad-staticmethod-argument,bad-thread-instantiation,binary-op-exception,broad-exception-caught,broad-exception-raised,confusing-with-statement,consider-ternary-expression,duplicate-except,duplicate-value,invalid-envvar-default,lost-exception,modified-iterating-list,nested-min-max,return-in-finally,too-many-try-statements,unbalanced-dict-unpacking,unbalanced-tuple-unpacking,unnecessary-lambda,unreachable,blacklisted-name,invalid-name,non-ascii-name,singleton-comparison,too-many-lines,unnecessary-direct-lambda-call,unnecessary-lambda-assignment,chained-comparison,comparison-with-itself,consider-merging-isinstance,duplicate-code,inconsistent-return-statements,literal-comparison,magic-value-comparison,simplifiable-condition,too-complex,too-many-arguments,too-many-boolean-expressions,too-many-branches,too-many-nested-blocks,too-many-return-statements,too-many-statements',
        '--output-format=json'
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    full_analysis = json.loads(result.stdout) if result.stdout else []

    # Read the code again to extract lines, using UTF-8 encoding
    with open('temp.py', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    os.remove('temp.py')  # Clean up the temporary file

    simplified_analysis = []
    for issue in full_analysis:
        line = int(issue['line']) if issue['line'] is not None else 0
        end_line = int(issue.get('endLine', line)) if issue.get('endLine', line) is not None else line
        start_line = line - 1
        end_line = end_line - 1

        issue_code = ''.join(lines[start_line:end_line + 1]).strip() if start_line >= 0 and end_line >= 0 and start_line <= end_line else ""

        simplified_analysis.append({
            'msg_id': issue['message-id'],
            'line': issue['line'],
            'column': issue['column'],
            'end_line': issue.get('endLine', issue['line']),
            'end_column': issue['endColumn'],
            'code_smell': issue_code
        })

    return simplified_analysis


# %%
def process_file(file_path):
    # Read the original JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding here
        data = json.load(file)

    # Perform pylint analysis for each code entry
    for entry in data:
        analysis_results = analyze_code_snippet(entry['code'])
        entry['pylint_analysis'] = analysis_results

    # Write the modified data with analysis results back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# %%
def process_directory(base_path):
    # Walk through all directories and files in the base path
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                print(f"Analyzing {file_path}")
                process_file(file_path)

# %%
base_path = '/workspaces/galeras-benchmark/datasets/pylint'
process_directory(base_path)


