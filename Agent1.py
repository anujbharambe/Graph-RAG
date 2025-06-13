import pandas as pd
import networkx as nx
from groq import Groq
import os
import dotenv
from SystemPrompt import generate_system_prompt

dotenv.load_dotenv()

# === Load Data ===
df = pd.read_excel("HourWiseData (4).xlsx")

# === Build Knowledge Graph ===
def build_graph(df):
    G = nx.MultiDiGraph()

    for _, row in df.iterrows():
        date = str(row["Date"])
        region = str(row["Region"])
        area = str(row["Area"])
        site_code = str(row["Site Code"])
        site_name = str(row["Site Name"])
        total_in = int(row["Total In Count"])
        group_count = int(row["Group Count"])
        unique_groups = int(row["Total Unique Groups"])

        # Add nodes
        G.add_node(site_name, type="Site")
        G.add_node(area, type="Area")
        G.add_node(region, type="Region")
        G.add_node(site_code, type="Code")
        G.add_node(date, type="Date")

        metric_node = f"{site_name}_{date}_metrics"
        G.add_node(metric_node, type="DailyMetrics", total_in=total_in, group_count=group_count, unique_groups=unique_groups)

        # Edges
        G.add_edge(site_name, area, relation="located_in_area")
        G.add_edge(site_name, region, relation="located_in_region")
        G.add_edge(site_name, site_code, relation="has_code")
        G.add_edge(site_name, metric_node, relation="has_metrics_on")
        G.add_edge(metric_node, date, relation="recorded_on")

    return G

graph = build_graph(df)

# === Convert Graph to Readable Text ===
def graph_to_text(graph):
    lines = []
    for u, v, data in graph.edges(data=True):
        node_type = graph.nodes[v].get("type", "")
        if node_type == "DailyMetrics":
            total_in = graph.nodes[v]["total_in"]
            group_count = graph.nodes[v]["group_count"]
            unique_groups = graph.nodes[v]["unique_groups"]
            date = next((tgt for src, tgt, d in graph.edges(v, data=True) if d.get("relation") == "recorded_on"), None)
            lines.append(f"{u} on {date} had total in: {total_in}, group count: {group_count}, unique groups: {unique_groups}")
        else:
            lines.append(f"{u} {data['relation']} {v}")
    return "\n".join(lines)

graph_text = graph_to_text(graph)

# Complex query detection removed - always using system prompt approach

# === Ask Groq API with system prompt ===
def ask_llm_with_graph_context(graph_text, user_question, model="compound-beta"):
    # Always use system prompt approach
    system_prompt = generate_system_prompt(df)
    prompt = f"""
Based on the aggregated data provided in the system message, answer the following question:
"{user_question}"

Additional context from specific graph data:
{graph_text}

Provide a comprehensive answer using both the aggregated metrics and specific details where relevant.
"""
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# === Entry Point for Input Script ===
def run_graphrag_agent(query: str):
    # Always use system prompt approach with relevant subgraph data
    
    import re
    # Find all site names mentioned in the graph that appear in query
    mentioned_sites = [n for n in graph.nodes if graph.nodes[n].get("type") == "Site" and n.lower() in query.lower()]
    
    # Find all dates mentioned in query
    mentioned_dates = re.findall(r"\b\d{2}-\d{2}-\d{4}\b", query)

    # Find all regions mentioned in query
    mentioned_regions = [n for n in graph.nodes if graph.nodes[n].get("type") == "Region" and n.lower() in query.lower()]
    
    # Find all areas mentioned in query
    mentioned_areas = [n for n in graph.nodes if graph.nodes[n].get("type") == "Area" and n.lower() in query.lower()]

    nodes_to_include = set()
    
    # Build combinations of site + date subgraphs
    if mentioned_sites:
        for site in mentioned_sites:
            if mentioned_dates:
                for date in mentioned_dates:
                    metric_node = f"{site}_{date}_metrics"
                    if metric_node in graph:
                        nodes_to_include |= {site, date, metric_node}
                        nodes_to_include |= set(graph.successors(metric_node))
                        nodes_to_include |= set(graph.predecessors(metric_node))

            else:
                # If no dates mentioned, include all metrics for the site
                for node in graph.nodes:
                    if node.startswith(f"{site}_") and graph.nodes[node].get("type") == "DailyMetrics":
                        nodes_to_include |= {site, node}
                        nodes_to_include |= set(graph.successors(node))
                        nodes_to_include |= set(graph.predecessors(node))

    # If no sites were mentioned, include all metrics for the given dates
    elif mentioned_dates:
        for date in mentioned_dates:
            for node in graph.nodes:
                if graph.nodes[node].get("type") == "DailyMetrics":
                    # Check if the metric node has an edge to the target date
                    edges = graph.edges(node, data=True)
                    for _, tgt, d in edges:
                        if d.get("relation") == "recorded_on" and tgt == date:
                            nodes_to_include |= {node, date}
                            nodes_to_include |= set(graph.successors(node))
                            nodes_to_include |= set(graph.predecessors(node))

    # If regions are mentioned, include all sites in those regions
    elif mentioned_regions:
        for region in mentioned_regions:
            for u, v, data in graph.edges(data=True):
                if data.get("relation") == "located_in_region" and v == region:
                    site = u
                    for node in graph.nodes:
                        if node.startswith(f"{site}_") and graph.nodes[node].get("type") == "DailyMetrics":
                            nodes_to_include |= {site, node, region}
                            nodes_to_include |= set(graph.successors(node))
                            nodes_to_include |= set(graph.predecessors(node))
    
    elif mentioned_areas:
        for area in mentioned_areas:
            for u, v, data in graph.edges(data=True):
                if data.get("relation") == "located_in_area" and v == area:
                    site = u
                    for node in graph.nodes:
                        if node.startswith(f"{site}_") and graph.nodes[node].get("type") == "DailyMetrics":
                            nodes_to_include |= {site, node, area}
                            nodes_to_include |= set(graph.successors(node))
                            nodes_to_include |= set(graph.predecessors(node))

    # If nothing specific was mentioned or for general queries, use a limited sample
    if not nodes_to_include:
        # Use a small sample of sites to avoid token limits
        sample_sites = list([n for n in graph.nodes if graph.nodes[n].get("type") == "Site"])[:5]
        subgraph_text = f"Sample sites available: {', '.join(sample_sites)}"
    else:
        # Limit subgraph size to avoid token issues
        if len(nodes_to_include) > 50:
            nodes_to_include = set(list(nodes_to_include)[:50])
        
        subgraph = graph.subgraph(nodes_to_include)
        subgraph_text = graph_to_text(subgraph)
    
    return ask_llm_with_graph_context(subgraph_text, query)
