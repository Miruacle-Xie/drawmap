import plotly.graph_objects as go
import plotly.express as px
import plotly.offline
import pandas as pd
import os


statefulltoshort = {'new york': 'NY', 'puerto rico': 'PR', 'virgin islands': 'VI', 'massachusetts': 'MA',
                    'rhode island': 'RI', 'new hampshire': 'NH', 'maine': 'ME', 'vermont': 'VT', 'connecticut': 'CT',
                    'new jersey': 'NJ', 'us armed forces europe': 'AE', 'pennsylvania': 'PA', 'delaware': 'DE',
                    'washington': 'DC', 'virginia': 'VA', 'maryland': 'MD', 'west virginia': 'WV',
                    'north carolina': 'NC', 'south carolina': 'SC', 'georgia': 'GA', 'florida': 'FL', 'alabama': 'AL',
                    'tennessee': 'TN', 'mississippi': 'MS', 'kentucky': 'KY', 'ohio': 'OH', 'indiana': 'IN',
                    'michigan': 'MI', 'iowa': 'IA', 'wisconsin': 'WI', 'minnesota': 'MN', 'south dakota': 'SD',
                    'north dakota': 'ND', 'montana': 'MT', 'illinois': 'IL', 'missouri': 'MO', 'kansas': 'KS',
                    'nebraska': 'NE', 'louisiana': 'LA', 'arkansas': 'AR', 'oklahoma': 'OK', 'texas': 'TX',
                    'colorado': 'CO', 'wyoming': 'WY', 'idaho': 'ID', 'utah': 'UT', 'arizona': 'AZ', 'new mexico': 'NM',
                    'nevada': 'NV', 'california': 'CA', 'us armed forces pacific': 'AP', 'hawaii': 'HI',
                    'american samoa': 'AS', 'guam': 'GU', 'palau': 'PW', 'federated states of micronesia': 'FM',
                    'northern mariana islands': 'MP', 'marshall islands': 'MH', 'oregon': 'OR', 'washington': 'WA',
                    'alaska': 'AK'}

# print(statefulltoshort[0]['New york'])
filepath = input("请输入文件路径:\n")
filepath = filepath.replace("\"", "").replace("\'", "")
df_raw = pd.read_excel(filepath)
print(df_raw)
df_raw.columns = df_raw.iloc[0, :]
df_raw = df_raw.drop(0, axis=0)
print(df_raw["country"])
print("------------------\n")
df = df_raw[(df_raw["country"] == "US") & (df_raw["type"] == "Order")]
print(df)
# print(df.columns)
df.drop_duplicates('order id', inplace=True)
print(df)
# input("111")
# print(df.iloc[0, :])
# print(df)

# print(df)
# print(df["order state"])
df["order state"] = df["order state"].str.upper()
df["order state"] = df["order state"].apply(
    lambda x: statefulltoshort[x.lower()] if x.lower() in statefulltoshort.keys() else x)
df1 = df["order state"].value_counts()
# print(df1)
# print(type(df1))
df1 = pd.DataFrame(df1)
# print(df1)
df1 = df1.reset_index()
# print(df1)
key_list = list(statefulltoshort.keys())
val_list = list(statefulltoshort.values())
df1 = df1.set_axis(["order state", "order number"], axis=1)
print(df1)
df1["text"] = df1["order state"].apply(lambda x: key_list[val_list.index(x)] if x in val_list else x)
# df1.to_excel("df1.xlsx")
print(df1)
# '''
pxhtmlpath = os.path.splitext(filepath)[0] + "-px.html"
gohtmlpath = os.path.splitext(filepath)[0] + ".html"
fig = px.choropleth(df1,
                    locations='order state',
                    locationmode="USA-states",
                    scope="usa",
                    color='order number',
                    color_continuous_scale="blues",
                    animation_frame="order number",
                    hover_name=df1['text'].apply(str.title),
                    # range_color=(0, 200),
                    )
plotly.offline.plot(fig, filename=pxhtmlpath, auto_open=True)
# fig.show()
# '''

print(df1.columns[1])
fig = go.Figure(data=go.Choropleth(
    locations=df1['order state'],
    z=df1['order number'],
    locationmode="USA-states",
    text=df1['text'].apply(str.title),
    colorscale='blues',
    # colorscale='reds',
    colorbar_title=df1.columns[1],
))
fig.update_layout(geo_scope='usa')
plotly.offline.plot(fig, filename=gohtmlpath, auto_open=True)
