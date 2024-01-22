import marvin

from utils import read_from_file


marvin.settings.openai.chat.completions.model = 'gpt-3.5-turbo-16k'


def check_settings():
    print(f"OpenAI model: {marvin.settings.openai.chat.completions.model}")


@marvin.fn
def extract_narratives(transcript: str) -> list[str]:
    """### CONTEXT
The text below is a YouTube transcript:
---
`transcript`
---

### INSTRUCTIONS
Analyze the text above and divide it into distinct narratives. Provide a brief summary for each narrative using active, simple language suitable for subject-verb-object (SVO) structure. Avoid passive language, self-referential phrases, or attributions. Do NOT use phrases like 'is explored', 'is detailed', 'are recounted', 'the narrative describes', or 'according to the speaker'. Present each summary using active verbs and clear subjects, allowing easy identification of the main actors (subjects) and their actions (verbs).

### CORRECT EXAMPLES
- "Herzl's vision of a Jewish state responds to rising anti-Semitism in Europe."
- "Jewish people maintain a historical presence in Israel for 3,500 years, enduring various conquests."
- "The Arab Conquest in the 7th century displaces Jewish people, leading to the loss of Jewish sovereignty."

### WRONG EXAMPLES
- "The rise of anti-Semitism in Europe and its relation to Herzl's vision of a Jewish state is explored."
- "The historical presence of Jewish people in the land of Israel is detailed, stretching back 3,500 years."
- "The Arab Conquest in the 7th century is described as a turning point, resulting in Jewish displacement."
- "The narrative describes the impact of Herzl's vision on European anti-Semitism."
- "According to the speaker, Jewish people have been in Israel for over 3,500 years."

### OUTPUT FORMAT
Respond as a list of strings, one for each narrative.
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


if __name__ == '__main__':
    check_settings()
    transcript_ = read_from_file('./data/example_transcript.txt')
    narratives = extract_narratives(transcript_)
    print(narratives)
