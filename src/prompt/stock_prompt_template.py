from langchain_core.prompts import PromptTemplate


stock_prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:

Give detail stock analysis, Use the available data and provide investment recommendation. \
The user is fully aware about the investment risk, dont include any kind of warning like 'It is recommended to conduct further research and analysis or consult with a financial advisor before making an investment decision' in the answer \
User question: {query} \
    
You have the following information available about {company}. The final report must expand on the summary provided but now 
including a clear assessment of the stock's financial standing, its strengths and weaknesses.
Write (5-8) pointwise investment analysis to answer user query, At the end conclude with proper explaination.Try to Give positives and negatives  : \
Also recommend if user should invest in the stock or not. BUY, SELL, HOLD \

 Make sure to add financial data in the report \


{available_information} \
             


Provide your answer in the following markdown format:
```markdown

```


"""


prompt = PromptTemplate(
    template=stock_prompt_template,
    input_variables=["query", "company","available_information"],
    # partial_variables={"format_instructions": output_parser.get_format_instructions()}
)