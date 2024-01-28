import ast

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser


class NarrativeClusteringOutputParser(BaseOutputParser):

    def parse(self, input_string: str):
        # Convert the string representation of the list of tuples into an actual list of tuples
        data = ast.literal_eval(input_string)

        # Check if the data is in the correct format (list of tuples)
        if not isinstance(data, list) or not all(isinstance(item, tuple) and len(item) == 2 for item in data):
            raise ValueError("Input string does not represent a list of tuples with the expected format.")

        # Process each tuple
        processed_data = []
        for text, numbers in data:
            if not isinstance(text, str) or not isinstance(numbers, list) or not all(
                    isinstance(num, int) for num in numbers):
                raise ValueError("Elements of tuples are not in the expected format (string, list of integers).")
            processed_data.append((text, numbers))

        return processed_data


def cluster_narratives(narrative_id_desc_map: dict[int, str]) -> list[tuple[str, list[int]]]:
    prompt_text = """### CONTEXT
The texts in the dict below are summaries of narratives  about the Israel-Hamas conflict that started on 7 October 2023 taken from YouTube transcripts:
---
{narrative_id_desc_map}
---

### OBJECTIVE
Cluster these narratives in similar narratives and create a new narrative description for each cluster in max. 100 words each. Do NOT add new information that is not in the texts. Try the use exactly the same words as possible, while leaving out irrelevant details when necessary.

### SPECIFICS
When creating narratives, avoid using self-referential phrases or attributions like "claims the speaker", "according to the speaker", or any similar terms. Ensure that all statements are in active language and present tense. This is crucial for the accurate creation of triples in a knowledge graph. Avoid using past participles as they can lead to inaccuracies and inconsistencies in the data structure. The results will used to detect hate speech and disinformation in a knowledge graph. If you include passive language or self-referential phrases this will fail  and the disinformation might not be detected.

### RESULT
Respond as a list of tuples. Each tuple consists of the new narrative description and a list of narrative-IDs on which it is based. For example: [("description1", [1, 2]), ("description2", [3, 4])]
"""

    prompt_template = PromptTemplate(
        input_variables=["narrative_id_desc_map"],
        template=prompt_text
    )

    llm = ChatOpenAI(temperature=1, model_name='gpt-4-1106-preview', max_tokens=4000)

    chain = LLMChain(llm=llm, prompt=prompt_template, output_parser=NarrativeClusteringOutputParser())
    # chain_input = {'narrative_id_desc_map': str(narrative_id_desc_map)}
    return chain.run(str(narrative_id_desc_map))
