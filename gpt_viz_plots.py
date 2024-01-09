import pandas as pd
import plotly.express as px



# wide_df = px.data.medals_wide()
# print(wide_df.head())
# fig = px.bar(wide_df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")
# fig.show()

df=pd.read_csv('data/gpt.csv').fillna('')
df['Study domain (defined in advance)']=[x.strip() for x in df['Study domain (defined in advance)']]
types=list(df['Study domain (defined in advance)'].unique())
print(types)
columns=list(df.columns)
columns.remove('Short Title')
columns.remove('Study domain (defined in advance)')
print(columns)

for c in columns:
    df[c] = [x.strip() for x in df[c]]

#for t in types:#use this with the evaluation of the 30 papers to make a plot for each study type
if True:#use this when plotting the ebm-nlp results
    t='All Papers'
    complete = []
    partial = []
    incorrect = []
    col=[]
    outdf=pd.DataFrame()

    filtered=df[df['Study domain (defined in advance)']==t]
    filtered=df
    print(filtered.shape)
    for c in columns:
            #print(filtered[c])
        #if 'Complete' in list(filtered[c]) or 'Incorrect' in filtered[c]:
            #print('found')
            col.append(c)
            comp=0
            part=0
            inc=0
            for res in filtered[c]:
                if 'Complete' in res:
                    comp+=1
                if 'Incorrect' in res:
                    inc += 1
                if 'Partial' in res:
                    part += 1
            complete.append(comp)
            partial.append(part)
            incorrect.append(inc)
    outdf['Type']=col
    outdf['Complete'] = complete
    outdf['Partial'] = partial
    outdf['Incorrect'] = incorrect
    todel=[]
    for i,row in outdf.iterrows():
        if row['Complete']==0 and row['Partial']==0 and row['Incorrect']==0:
            todel.append(i)
    outdf.drop(index=todel, inplace=True)
    outdf.to_csv('outputs/{}.csv'.format(t))


    #
    fig = px.bar(outdf, title=t,x="Type", y=["Complete", "Partial", "Incorrect"], color_discrete_map = {'Complete': '#34BD2F', 'Partial': '#EBDE34', 'Incorrect': '#EB4034'}).update_layout(
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)',
            legend_title="Results",
                            )
    fig.update_xaxes(showline=False)
    fig.update_yaxes(showline=False)
    fig.show()














