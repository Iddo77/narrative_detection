import ast

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser


class TriplesExtractionOutputParser(BaseOutputParser):

    def parse(self, input_string: str):
        # Convert the string representation to a list of strings
        data = ast.literal_eval(input_string)
        return data


def extract_triples(narrative: str) -> list[str]:
    prompt_text = """### CONTEXT
The text below is a narrative found in YouTube videos about the Israel-Hamas conflict that started on 7 October 2023:
---
{narrative}
---

### OBJECTIVE
Extract triples for this text that can be used in a knowledge graph. For verbs use present tense. Try to prevent complex triple parts consisting of multiple words.

### RESULT
Respond as a list of 3-tuples in the format [("man" ,"eats", "lunch"), ("Peter", "lives in", "London")]. Do NOT add any other text.
"""

    prompt_template = PromptTemplate(
        input_variables=["narrative"],
        template=prompt_text
    )

    llm = ChatOpenAI(temperature=1, model_name='gpt-4-1106-preview', max_tokens=200)

    chain = LLMChain(llm=llm, prompt=prompt_template, output_parser=TriplesExtractionOutputParser())
    result = chain.invoke({"narrative": narrative})
    return result["text"]


if __name__ == '__main__':
    text = "The Oslo Accords establish the first direct Palestinian-Israeli peace agreement, recognizing each other's leadership, but not resolving peace in the region as conflicts continue."
    narratives = extract_triples(text)
    print(narratives)
