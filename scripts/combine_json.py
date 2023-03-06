import json
import os

def read_tex_results():
    with open("/autograder/tex_results.json", 'r') as f_tex:
        s_tex = f_tex.read()
        json_tex = json.loads(s_tex)
        return {"tests": json_tex["tests"]}

def read_lean_results():
    with open("/autograder/lean_results.json", 'r') as f_lean:
        s_lean = f_lean.read()
        json_lean = json.loads(s_lean)  
        # The lean result contains a "tests" field iff it was able to complete testing - otherwise
        # it just has a score of 0 and a description of the error that prevented testing.
        return { "tests": (json_lean["tests"] if "tests" in json_lean else json_lean) }


def main():
    has_lean, has_tex = os.path.isfile("/autograder/lean_results.json"), os.path.isfile("/autograder/tex_results.json")

    #lean_results = read_lean_results() if has_lean else {"tests": [{"name": "No .lean file found", "score": 0, "output": "You are expected to upload exactly one .lean file!", "status": "failed"}]}
    tex_results = read_tex_results() if has_tex else {"tests": [{"name": "No .tex file found", "score": 0, "output": "You are expected to upload at least one .tex file!", "status": "failed"}]}


    with open("results/results.json", "w") as f_out:
        f_out.write(json.dumps({"tests": tex_results["tests"] ++ [{"name": "PDF upload reminder", "score": 0, "max_score": 0, "output": "Thanks! Remember to also upload your PDF to the HW5 assignment on Gradescope. (This submission is for your .tex file only.)"}]}))

if __name__ == "__main__":
    main()
