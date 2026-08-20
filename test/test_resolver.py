from src.automation.resolver import resolve_command


tests = [
    "search google leetcode",
    "search google for leetcode binary search",
    "can you search google for python sockets",
    "please search youtube for python tutorials",
    "look up leetcode on google",
    "search for machine learning",

    "open youtube",
    "take me to youtube",
    "go to github",

    "open my downloads folder",
    "show me my documents",

    "close chrome",
    "I'm finished with chrome, get it out of the way",

    "don't close chrome",
]


for command in tests:
    print("\nINPUT :", command)
    print("OUTPUT:", resolve_command(command))