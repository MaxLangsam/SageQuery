import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

prompt_template = """
Given the following database schema and example pairs, translate the user's question into a SQL query.

Schema:
{schema}

Examples:
{examples}

Question: {question}
SQL:
"""

def nl_to_sql_service(question, examples, schema=None):
    # Format prompt with schema and examples
    formatted_examples = "\n".join([
        f"Q: {ex['question']}\nSQL: {ex['sql']}" for ex in examples
    ])
    prompt = PromptTemplate(
        input_variables=["schema", "examples", "question"],
        template=prompt_template
    )
    llm = OpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY)
    chain = LLMChain(llm=llm, prompt=prompt)
    # Schema can be injected or discovered
    schema_str = schema or "<schema omitted for brevity>"
    result = chain.run(schema=schema_str, examples=formatted_examples, question=question)
    return result.strip() 