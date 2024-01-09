import pandas as pd
import plotly.express as px




df=pd.read_csv('data/ebmnlp_evaluated.csv').fillna('')

types=['Participants','Intervention/Control', 'Outcomes']
if True:
    complete = []
    partial = []
    incorrect = []
    typess=[]
    outdf=pd.DataFrame()

    #filtered=df[df['Study domain (defined in advance)']==t]
    filtered=df
    for t in types:
        comp=0
        part=0
        inc=0
        for i,row in filtered.iterrows():
                    if row[t]=='C':
                        comp+=1
                    if row[t]=='I':
                        inc += 1
                    if row[t]=='P':
                        part += 1
        complete.append(comp)
        partial.append(part)
        incorrect.append(inc)
        typess.append(t)
    outdf['Type']=typess
    outdf['Complete'] = complete
    outdf['Partial'] = partial
    outdf['Incorrect'] = incorrect

    outdf.to_csv('outputs/ebmnlp.csv')


    #
    fig = px.bar(outdf, title=t,x="Type", y=["Complete", "Partial", "Incorrect"], color_discrete_map = {'Complete': '#34BD2F', 'Partial': '#EBDE34', 'Incorrect': '#EB4034'}).update_layout(
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)',
            legend_title="Results",
                            )
    fig.update_xaxes(showline=False)
    fig.update_yaxes(showline=False)
    fig.show()














