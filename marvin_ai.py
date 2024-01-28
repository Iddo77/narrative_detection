import marvin

from utils import read_from_file


marvin.settings.openai.chat.completions.model = 'gpt-4-1106-preview'


def check_settings():
    print(f"OpenAI model: {marvin.settings.openai.chat.completions.model}")


@marvin.fn
def extract_narratives(transcript: str) -> list[str]:
    """
### CONTEXT
The text below is a YouTube transcript  about the Israel-Hamas conflict that started on 7 October 2023:
---
`transcript`
---

### OBJECTIVE
Your objective is to extract and summarize the narratives in this text. Extract at most 10 narratives. If there are more, extract the ones most likely to contain disinformation or hate speech.

### SPECIFICS
When summarizing narratives, avoid using self-referential phrases or attributions like "claims the speaker", "according to the speaker", or any similar terms. Ensure that all statements are in active language and present tense. This is crucial for the accurate creation of triples in a knowledge graph. Avoid using past participles as they can lead to inaccuracies and inconsistencies in the data structure. The results will used to detect hate speech and disinformation in a knowledge graph. If you include passive language or self-referential phrases this will fail  and the disinformation might not be detected.

### RESULT
Respond as a list of strings, one for each narrative in the format ["string1",  "string2"].
"""

@marvin.fn
def merge_narratives(narratives: list[str]) -> str:
    """### CONTEXT
The texts below are similar narratives found in YouTube videos about the Israel-Hamas conflict that started on 7 October 2023:
---
`narrative`
---

### INSTRUCTIONS
Merge these narratives into a single coherent narrative of maximum 100 words.

### OUTPUT FORMAT
Respond with a single string containing the narrative, and nothing else.
"""


@marvin.fn
def create_search_term(narrative: str) -> list[str]:
    """### CONTEXT
The text below is a narrative found in YouTube videos about the Israel-Hamas conflict that started on 7 October 2023:
---
`narrative`
---

### INSTRUCTIONS
Create a search term for use with DuckDuckGo Search to find more similar videos for the narrative.
Only use words from the given narrative or derivatives of those words. Use at most 5 words.

### OUTPUT FORMAT
Respond with a single string containing the search term, and nothing else.
"""

@marvin.fn
def cluster_narratives(narrative_id_desc_map: dict[int, str]) -> list[tuple[str, list[int]]]:
    """### CONTEXT
The texts in the dict below are summaries of narratives  about the Israel-Hamas conflict that started on 7 October 2023 taken from YouTube transcripts:
---
`str(narrative_id_desc_map)`
---

### OBJECTIVE
Cluster these narratives in similar narratives and create a new narrative description for each cluster in max. 100 words each. Do NOT add new information that is not in the texts. Try the use exactly the same words as possible, while leaving out irrelevant details when necessary.

### SPECIFICS
When creating narratives, avoid using self-referential phrases or attributions like "claims the speaker", "according to the speaker", or any similar terms. Ensure that all statements are in active language and present tense. This is crucial for the accurate creation of triples in a knowledge graph. Avoid using past participles as they can lead to inaccuracies and inconsistencies in the data structure. The results will used to detect hate speech and disinformation in a knowledge graph. If you include passive language or self-referential phrases this will fail  and the disinformation might not be detected.

### RESULT
Respond as a list of tuples. Each tuple consists of the new narrative description and a list of narrative-IDs on which it is based. For example: [("description1", [1, 2]), ("description2", [3, 4])]
"""

if __name__ == '__main__':
    check_settings()
    transcript_ = read_from_file('./data/example_transcript.txt')
    narratives = extract_narratives(transcript_)
    print(narratives)
