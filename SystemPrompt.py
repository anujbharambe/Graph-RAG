import pandas as pd
from datetime import datetime, timedelta
import calendar

def generate_system_prompt(df):
    """
    Generate a comprehensive system prompt with weekly and monthly aggregated metrics
    for sites, regions, and areas to handle complex multi-region queries.
    """
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    
    # Add week and month columns
    df['Week'] = df['Date'].dt.isocalendar().week
    df['Month'] = df['Date'].dt.month
    df['Year-Month'] = df['Date'].dt.strftime('%Y-%m')
    df['Year-Week'] = df['Date'].dt.strftime('%Y-W%U')  # Year-Week format
    
    # === DAILY AGGREGATIONS ===
    daily_site_metrics = df.groupby(['Site Name', 'Date']).agg({
        'Total In Count': 'sum',
        'Group Count': 'sum',
        'Total Unique Groups': 'sum',
        'Region': 'first',
        'Area': 'first'
    }).reset_index()
    
    daily_area_metrics = df.groupby(['Area', 'Date']).agg({
        'Total In Count': 'sum',
        'Group Count': 'sum',
        'Total Unique Groups': 'sum',
        'Region': 'first'
    }).reset_index()
    
    daily_region_metrics = df.groupby(['Region', 'Date']).agg({
        'Total In Count': 'sum',
        'Group Count': 'sum',
        'Total Unique Groups': 'sum'
    }).reset_index()
    
    # === WEEKLY AGGREGATIONS ===
    weekly_site_metrics = df.groupby(['Site Name', 'Year-Week']).agg({
        'Total In Count': 'sum',
        'Group Count': 'sum',
        'Total Unique Groups': 'sum',
        'Region': 'first',
        'Area': 'first'
    }).reset_index()
    
    weekly_area_metrics = df.groupby(['Area', 'Year-Week']).agg({
        'Total In Count': 'sum',
        'Group Count': 'sum',
        'Total Unique Groups': 'sum',
        'Region': 'first'
    }).reset_index()
    
    weekly_region_metrics = df.groupby(['Region', 'Year-Week']).agg({
        'Total In Count': 'sum',
        'Group Count': 'sum',
        'Total Unique Groups': 'sum'
    }).reset_index()
    
    # === MONTHLY AGGREGATIONS ===
    monthly_site_metrics = df.groupby(['Site Name', 'Year-Month']).agg({
        'Total In Count': 'sum',
        'Group Count': 'sum',
        'Total Unique Groups': 'sum',
        'Region': 'first',
        'Area': 'first'
    }).reset_index()
    
    monthly_area_metrics = df.groupby(['Area', 'Year-Month']).agg({
        'Total In Count': 'sum',
        'Group Count': 'sum',
        'Total Unique Groups': 'sum',
        'Region': 'first'
    }).reset_index()
    
    monthly_region_metrics = df.groupby(['Region', 'Year-Month']).agg({
        'Total In Count': 'sum',
        'Group Count': 'sum',
        'Total Unique Groups': 'sum'
    }).reset_index()
    
    # === OVERALL SUMMARY STATISTICS ===
    total_metrics = {
        'total_visitors': df['Total In Count'].sum(),
        'total_groups': df['Group Count'].sum(),
        'total_unique_groups': df['Total Unique Groups'].sum(),
        'total_sites': df['Site Name'].nunique(),
        'total_areas': df['Area'].nunique(),
        'total_regions': df['Region'].nunique(),
        'date_range': f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}"
    }
    
    # === BUILD SYSTEM PROMPT ===
    system_prompt = f"""You are an intelligent assistant that answers queries about US Polo store visitor data across India for May 2025.

SUMMARY STATISTICS:
- Total Visitors: {total_metrics['total_visitors']:,}
- Total Groups: {total_metrics['total_groups']:,}
- Total Unique Groups: {total_metrics['total_unique_groups']:,}
- Total Sites: {total_metrics['total_sites']}
- Total Areas: {total_metrics['total_areas']}
- Total Regions: {total_metrics['total_regions']}
- Date Range: {total_metrics['date_range']}

REGIONAL HIERARCHY:
"""
    
    # Add regional hierarchy information
    hierarchy = df.groupby('Region')['Area'].apply(list).to_dict()
    for region, areas in hierarchy.items():
        system_prompt += f"- {region}: {', '.join(set(areas))}\n"
    
    system_prompt += "\nSITE LOCATIONS:\n"
    site_locations = df.groupby('Site Name').agg({'Region': 'first', 'Area': 'first'}).reset_index()
    for _, row in site_locations.iterrows():
        system_prompt += f"- {row['Site Name']}: {row['Area']}, {row['Region']}\n"
    
    # === WEEKLY METRICS SUMMARY ===
    system_prompt += "\nWEEKLY REGIONAL PERFORMANCE:\n"
    for _, row in weekly_region_metrics.iterrows():
        system_prompt += f"- {row['Region']} ({row['Year-Week']}): {row['Total In Count']:,} visitors, {row['Group Count']} groups, {row['Total Unique Groups']} unique groups\n"
    
    system_prompt += "\nWEEKLY AREA PERFORMANCE:\n"
    for _, row in weekly_area_metrics.iterrows():
        system_prompt += f"- {row['Area']} ({row['Year-Week']}): {row['Total In Count']:,} visitors, {row['Group Count']} groups, {row['Total Unique Groups']} unique groups\n"
    
    system_prompt += "\nWEEKLY SITE PERFORMANCE:\n"
    for _, row in weekly_site_metrics.iterrows():
        system_prompt += f"- {row['Site Name']} ({row['Area']}, {row['Region']}) ({row['Year-Week']}): {row['Total In Count']:,} visitors, {row['Group Count']} groups, {row['Total Unique Groups']} unique groups\n"

    # === MONTHLY METRICS SUMMARY ===
    system_prompt += "\nMONTHLY REGIONAL PERFORMANCE:\n"
    for _, row in monthly_region_metrics.iterrows():
        month_name = calendar.month_name[int(row['Year-Month'].split('-')[1])]
        system_prompt += f"- {row['Region']} ({month_name} 2025): {row['Total In Count']:,} visitors, {row['Group Count']} groups, {row['Total Unique Groups']} unique groups\n"
    
    system_prompt += "\nMONTHLY AREA PERFORMANCE:\n"
    for _, row in monthly_area_metrics.iterrows():
        month_name = calendar.month_name[int(row['Year-Month'].split('-')[1])]
        system_prompt += f"- {row['Area']} ({month_name} 2025): {row['Total In Count']:,} visitors, {row['Group Count']} groups, {row['Total Unique Groups']} unique groups\n"
    
    system_prompt += "\nMONTHLY SITE PERFORMANCE:\n"
    for _, row in monthly_site_metrics.iterrows():
        site = row['Site Name']
        month_name = calendar.month_name[int(row['Year-Month'].split('-')[1])]
        system_prompt += f"- {site} ({row['Area']}, {row['Region']}) ({month_name} 2025): {row['Total In Count']:,} visitors, {row['Group Count']} groups, {row['Total Unique Groups']} unique groups\n"

    
    # === TOP PERFORMERS ===
    system_prompt += "\nTOP PERFORMING SITES (by total visitors):\n"
    top_sites = monthly_site_metrics.groupby('Site Name')['Total In Count'].sum().sort_values(ascending=False).head(10)
    for site, visitors in top_sites.items():
        region = site_locations[site_locations['Site Name'] == site]['Region'].iloc[0]
        area = site_locations[site_locations['Site Name'] == site]['Area'].iloc[0]
        system_prompt += f"- {site} ({area}, {region}): {visitors:,} total visitors\n"
    
    system_prompt += "\nTOP PERFORMING REGIONS (by total visitors):\n"
    top_regions = monthly_region_metrics.groupby('Region')['Total In Count'].sum().sort_values(ascending=False)
    for region, visitors in top_regions.items():
        system_prompt += f"- {region}: {visitors:,} total visitors\n"
    
    system_prompt += "\nTOP PERFORMING AREAS (by total visitors):\n"
    top_areas = monthly_area_metrics.groupby('Area')['Total In Count'].sum().sort_values(ascending=False).head(10)
    for area, visitors in top_areas.items():
        region = daily_area_metrics[daily_area_metrics['Area'] == area]['Region'].iloc[0]
        system_prompt += f"- {area} ({region}): {visitors:,} total visitors\n"
    
    system_prompt += """
INSTRUCTIONS:
- Use this aggregated data to answer all types of queries about US Polo store performance
- For specific daily queries, combine this summary data with the detailed graph data provided
- For multi-region or calculation-heavy queries, rely primarily on the aggregated metrics above
- Calculate metrics, percentages, and comparisons using the summary data above
- Provide precise numerical answers with proper formatting (use commas for large numbers)
- When comparing regions or areas, use the performance data provided above
- Always provide context about which time period (daily, weekly, monthly) your answer refers to
"""
    
    return system_prompt
