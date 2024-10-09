import pandas as pd
import streamlit as st
import plotly.express as px
import re




# Initialize a list to store dictionaries of extracted data
data = []

# Define the regex pattern to match the desired line format
pattern = r"\| Block: (\d+) \| Stake: (\d+\.\d+) \| Trust: (\d+\.\d+) \| Consensus: (\d+\.\d+) \| Incentive: (\d+\.\d+) \| Emission: (\d+\.\d+) \|"

# Open the log file in read mode with UTF-8 encoding
with open('smaller log file.log.txt', 'r', encoding='utf-8') as file:
    # Iterate over each line in the file
    for line in file:
        # Search for the pattern in the line
        match = re.search(pattern, line)

        # If the pattern is found, extract the datetime and block-related information
        if match:
            # Extract the datetime
            datetime_str = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}", line).group()

            # Extract the block-related information
            block_index, stake, trust, consensus, incentive, emission = match.groups()

            # Append the extracted data to the list of dictionaries
            data.append({
                'Date': datetime_str,
                'Block': block_index,
                'Stake': stake,
                'Trust': trust,
                'Consensus': consensus,
                'Incentive': incentive,
                'Emission': emission
            })

# Assuming you have 'data' as a list of dictionaries containing your data

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime (including time)

# Main function
st.title('Server Logs Dashboard')

# Sidebar controls
st.sidebar.header('Filter Data')

# Get min and max dates
min_date = df['Date'].min()
max_date = df['Date'].max()

# Set default values
default_end_date = max_date
default_start_date = max(default_end_date - pd.Timedelta(days=7), min_date)

# Corrected sidebar widgets (including date and time separately)
start_date = st.sidebar.date_input("Start Date", value=default_start_date,
                                   min_value=min_date, max_value=max_date)
start_time = st.sidebar.time_input("Start Time", value=pd.Timestamp("08:00:00"))

end_date = st.sidebar.date_input("End Date", value=default_end_date,
                                 min_value=min_date, max_value=max_date)
end_time = st.sidebar.time_input("End Time", value=pd.Timestamp("17:00:00"))
# Filter data
start_datetime = pd.to_datetime(str(start_date) + ' ' + str(start_time))
end_datetime = pd.to_datetime(str(end_date) + ' ' + str(end_time))

filtered_df = df[(df['Date'] >= start_datetime) & (df['Date'] <= end_datetime)]



# Multi-select for Y-axis variables
variables = ['Stake', 'Trust', 'Consensus', 'Incentive', 'Emission']
selected_vars = st.sidebar.multiselect('Select Variables', variables, default=variables)

# Plot
fig = px.line(filtered_df, x='Date', y=selected_vars, title='Server Logs')
st.plotly_chart(fig)


