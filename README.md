# Graph-RAG

***This project is still under development...

List of queries the agent can answer-:

1.) Site-specific queries - Good
"What was the total unique group count for Phoenix Mall on 05-05-2025?"
"Total unique group count for Inorbit Mall"

2.) Date-specific queries -Good
"Show the total unique groups count for 05-05-2025."
"List all metrics recorded on 10-05-2025."

3.) Region/Area-specific queries - Good
"Tell the total visitors for Chennai stores in May 2025."
"Give me metrics for Karnataka region" -> Barely able to answer
"Compare total unique group count for Karnataka and Telangana." -> Able to answer based on the System Prompt

4.) Metric comparison queries(Site-wise) -Good
"Compare the total unique groups count of Inorbit Mall and MOA." 
"Which site had the highest total unique groups on 19-05-2025?"

5.) Temporal Analysis Queries -Good
"How has the unique group count changed for Inorbit Mall over May 2025?"
"Show the daily trend for Indiranagar."

6.) Aggregation Queries - Good
"Give me the average total unique groups per day of Inorbit Mall for May 2025"
"What is average total unique groups per site on 10-05-2025?"

7.) General Insight Queries -Decent(Can answer most of user's queries)
"What was the overall footfall pattern in may 2025?"
"Which malls were busiest during weekends?"  --> Will support queries if weekday data is added to the database(LLM must know the day of the week)

8.) Predictive Queries - Good
What will be the footfall for the next month?

9.) Ranking Queries -Good
What are the top performing sites for may 2025 on the basis of total in count?



**Points to Note-:
All queries that require aggregation of metrics over a month are not supported. All queries(analytical+ retrieval-based) are fully supported given the data required in limited to specific sites/region. Also, queries related to more than one region are not fully supported.  ### Solved

**Problems to be solved-:
Data being passed to the LLM as System Prompt will at some point of time become so large that it will outweigh it's capacity(Reponse time will be large). The data that I am working on rn is only for a month.
Possible Solution-:
Use traditional RAG to store the System Prompt as vector embeddings, convert user's prompt to vector embeddings and then perform semantic search across the vectordb. Retrieve relevant data and pass it as context to the System Prompt.
