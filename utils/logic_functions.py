def assign_color(client, col1, col2, base_zero=False):
    colors = []
    for i, row in client.df.iterrows():
        if row[col1] > (0 if base_zero else row[col2]):
            colors.append('rgba(0, 255, 0, 0.7)')
        elif (0 if base_zero else row[col2]) > row[col1]:
            colors.append('rgba(255, 0, 0, 0.7)')
        else:
            colors.append('rgba(0, 0, 0, 0)')
    return colors