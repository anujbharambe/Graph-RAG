# Graph-RAG

***This project is still under development...

List of queries the agent can answer-:

1.) Site-specific queries - Good
"What was the total unique group count for Phoenix Mall on 05-05-2025?"
"Total unique group count for Inorbit Mall"

2.) Date-specific queries -Good
"Show the total unique groups count for 05-05-2025."
"List all metrics recorded on 10-05-2025."

3.) Region/Area-specific queries - Average
"Tell the total visitors for Chennai stores in May 2025." ->Answered
"Give me metrics for Karnataka region" -> Barely able to answer
"Compare total unique group count for Karnataka and Telangana." -> Request entity too large

4.) Metric comparison queries(Site-wise) -Good
"Compare the total unique groups count of Inorbit Mall and MOA." 
"Which site had the highest total unique groups on 19-05-2025?"

5.) Temporal Analysis Queries -Good
"How has the unique group count changed for Inorbit Mall over May 2025?"
"Show the daily trend for Indiranagar."

6.) Aggregation Queries - Good
"Give me the average total unique groups per day of Inorbit Mall for May 2025"
"What is average total unique groups per site on 10-05-2025?"

7.) General Insight Queries -Bad(Request Entity too large)
"What was the overall footfall pattern in may 2025?"

8.) Predictive Queries - Not Supported yet + Request Entity Too Large
What will be the footfall for the next month?

9.) Ranking Queries -Not supported yet + Request entity too large
What are the top performing sites for may 2025 on the basis of total in count?


**Points to Note-:
All queries that require aggregation of metrics over a month are not supported. All queries(analytical+ retrieval-based) are fully supported given the data required in limited to specific sites/region. Also, queries related to more than one region are not fully supported.
