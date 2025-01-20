import argparse
import json
import os

def validate_format(flashcards:dict) -> bool:
    # format: [{"question": "What is the capital of France?", "answer": "Paris"}]
    if not isinstance(flashcards, list):
        return False
    for flashcard in flashcards:
        if not isinstance(flashcard, dict):
            return False
        if "question" not in flashcard or "answer" not in flashcard:
            return False
    return True

def create_flashcard(question: str, answer: str, idx: int) -> str:
    """
    Returns a LaTeX snippet for a flashcard with:
      - A large multiline text field (where the user can type their solution).
      - An overlayed official answer revealed by a 'Solve' button (using ocgx2).
    """
    return f"""        \\newpage
        \\vspace*{{\\fill}}
        \\begin{{center}}
            \\begin{{QA}}
                % Question text
                \\textbf{{QUESTION:}} {question}

                % Large multiline text box for the user to write their own solution
                \\par\\vspace*{{0.5cm}}
                \\TextField[name=flashcard_{idx}, width=12cm, height=5cm, multiline=true]{{\\null}}

                % Overlayed official answer (hidden by default)
                % The 'off' parameter means it's initially invisible.
                \\begin{{ocg}}{{Answer Overlay}}{{answer{idx}}}{{off}}
                    \\par\\vspace*{{0.5cm}}
                    % Some styling for the overlay box:
                    % We use a red background box to simulate a covering overlay.
                    % If you want just text, remove the 'tcolorbox' approach.
                    \\noindent
                    \\begin{{tcolorbox}}[width=12cm,colback=red!10,colframe=red!80!black,title=OFFICIAL\\ ANSWER]
                        {answer}
                    \\end{{tcolorbox}}
                \\end{{ocg}}
            \\end{{QA}}

            % "Solve" button toggles the overlay
            \\switchocg{{answer{idx}}}{{\\fbox{{\\textbf{{Solve}}}}}}
        \\end{{center}}
        \\vspace*{{\\fill}}
    """


def parse_flashcards(filename:str) -> str:
    with open(filename, 'r') as file:
        flashcards = json.load(file)
    if not validate_format(flashcards):
        raise ValueError("Invalid flashcard format")
    
    return "\n".join([create_flashcard(flashcard["question"], flashcard["answer"], i) for i, flashcard in enumerate(flashcards)])

def main():
    parser = argparse.ArgumentParser(description="Parse flashcards")
    parser.add_argument("filename", type=str, help="The filename of the flashcards")
    parser.add_argument("--author", type=str, help="The author of the flashcards", required=False, default="")
    parser.add_argument("--title", type=str, help="The title of the flashcards", required=False, default="Flashcards")
    
    args = parser.parse_args()
    
    flashcards = parse_flashcards(args.filename)
    with open(os.path.join(os.path.dirname(__file__), "templates", "empty.tex"), "r") as file:
        template = file.read()
    
    with open("output.tex", "w") as file:
        # Find and replace the placeholders in the template - AUTHOR, TITLE, CONTENT
        template = template.replace("AUTHOR", args.author)
        template = template.replace("TITLE", args.title)
        template = template.replace("CONTENT", flashcards)
        
        file.write(template)
    
if __name__ == "__main__":
    main()
