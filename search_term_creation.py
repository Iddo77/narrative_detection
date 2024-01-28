from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


def create_search_term(narrative: str) -> str:
    prompt_text = """### CONTEXT
The text below is a narrative found in YouTube videos:
---
{narrative}

### INSTRUCTIONS
Create a search term for use with DuckDuckGo Search to find more similar videos for the narrative.
Only use words from the given narrative or derivatives of those words. Use at most 5 words.

### OUTPUT FORMAT
Respond with a single string containing the search term, and nothing else.
"""

    prompt_template = PromptTemplate(
        input_variables=["narrative"],
        template=prompt_text
    )
    llm = ChatOpenAI(temperature=1, model_name='gpt-3.5-turbo-16k', max_tokens=25)

    chain = LLMChain(llm=llm, prompt=prompt_template)
    result = chain.invoke({"narrative": narrative})
    return result["text"]


if __name__ == '__main__':
    desc = 'The West Bank and Gaza Strip are identified as the Palestinian state with divided governance between Israel and the Palestinian National Authority, while the densely-populated and blockaded Gaza Strip is controlled by Hamas.'
    print(create_search_term(desc))
