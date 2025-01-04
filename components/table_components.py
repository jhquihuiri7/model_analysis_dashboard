import dash_mantine_components as dmc

def main_table(client, cols):
    
    last_day = client.df.index.max().date()
    df = client.df[client.df.index.date == last_day]

    rows = [
        dmc.TableTr(
            [dmc.TableTd(col)]+
            [
             dmc.TableTd(round(value, 2)) for value in df[col]
            ]
        )
        for col in cols
    ]
    
    head = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("Model"),
               *[dmc.TableTh(hour) for hour in range(0, 24)]
            ]
        )
    )
    body = dmc.TableTbody(rows)
    
    return dmc.Table(
        [head, body], 
        withTableBorder=True, 
        highlightOnHover=True,
        className="rounded-lg border border-separate border-tools-table-outline"
        )