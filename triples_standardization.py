import ast

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser


class TriplesStandardizationOutputParser(BaseOutputParser):

    def parse(self, input_string: str):
        # Convert the string representation to a list of strings
        data = ast.literal_eval(input_string)
        return data


def standardize_triples(triples: list[tuple]) -> list[tuple]:
    prompt_text = """### CONTEXT
The triples below are about the Israel-Hamas conflict that started on 7 October 2023:
---
{triples}
---

### OBJECTIVE
Standardize these triples by replacing synonyms and alternative phrasings in these triples with a single, consistent text throughout all triples, so that I can create a single consistent knowledge graph with them.

### RESULT
Respond as a list of 3-tuples in the format [("man" ,"eats", "lunch"), ("Peter", "lives in", "London")]. Do NOT add any other text.
"""

    prompt_template = PromptTemplate(
        input_variables=["triples"],
        template=prompt_text
    )

    llm = ChatOpenAI(temperature=1, model_name='gpt-4-1106-preview', max_tokens=4000)

    chain = LLMChain(llm=llm, prompt=prompt_template, output_parser=TriplesStandardizationOutputParser())
    result = chain.invoke({"triples": str(triples)})
    return result["text"]
