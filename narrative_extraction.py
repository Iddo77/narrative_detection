import ast

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser

from utils import read_from_file


class NarrativeExtractionOutputParser(BaseOutputParser):

    def parse(self, input_string: str):
        # Convert the string representation to a list of strings
        data = ast.literal_eval(input_string)
        return data


def extract_narratives(transcript: str) -> list[str]:
    prompt_text = """### CONTEXT
The text below is a YouTube transcript  about the Israel-Hamas conflict that started on 7 October 2023:
---
{transcript}
---

### OBJECTIVE
Your objective is to extract and summarize the narratives in this text. Extract at most 10 narratives. If there are more, extract the ones most likely to contain disinformation or hate speech.

### SPECIFICS
When summarizing narratives, avoid using self-referential phrases or attributions like "claims the speaker", "according to the speaker", or any similar terms. Ensure that all statements are in active language and present tense. This is crucial for the accurate creation of triples in a knowledge graph. Avoid using past participles as they can lead to inaccuracies and inconsistencies in the data structure. The results will used to detect hate speech and disinformation in a knowledge graph. If you include passive language or self-referential phrases this will fail  and the disinformation might not be detected.

### RESULT
Respond as a list of strings, one for each narrative in the format ["string1",  "string2"].
"""

    prompt_template = PromptTemplate(
        input_variables=["transcript"],
        template=prompt_text
    )

    llm = ChatOpenAI(temperature=1, model_name='gpt-4-1106-preview', max_tokens=4000)

    chain = LLMChain(llm=llm, prompt=prompt_template, output_parser=NarrativeExtractionOutputParser())
    result = chain.invoke({"transcript": transcript})
    return result["text"]


if __name__ == '__main__':
    transcript_ = read_from_file('./data/example_transcript.txt')
    narratives = extract_narratives(transcript_)
    print(narratives)
