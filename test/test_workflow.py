from src.automation.workflow import split_workflow


tests = [
    "open chrome and open youtube",

    "open chrome and then open youtube",

    "open vscode, and then open downloads",

    "open chrome then search google leetcode",
]


for command in tests:

    print(f"\nInput: {command}")

    steps = split_workflow(command)

    for i, step in enumerate(steps, 1):

        print(f"  {i}. {step}")