import json
import sys

def main():
    with open("/autograder/lean_results.json", 'r') as f_lean, open("/autograder/tex_results.json", 'r') as f_tex:
        s_lean = f_lean.read()
        s_tex = f_tex.read()
        print(s_lean)
        print(s_tex)
        json_lean = json.loads(s_lean)
        json_tex = json.loads(s_tex)

    results = {"tests": json_tex["tests"]}
    
    # The lean result contains a "tests" field iff it was able to complete testing - otherwise
    # it just has a score of 0 and a description of the error that prevented testing.
    if "tests" in json_lean:
        results["tests"] += json_lean["tests"]
    else:
        results["tests"] += json_lean

    with open("results/results.json", "w") as f_out:
        f_out.write(json.dumps(results))

if __name__ == "__main__":
    main()
