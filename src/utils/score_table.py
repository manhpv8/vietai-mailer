import pandas as pd


ROW_HTML = '''
    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    </tr>
    '''

def postprocessing_content_html(template_html, row_ranking_content, name, ranking, score):  
    html = template_html.replace("<ROW_RANKING_SCORE>", str(row_ranking_content))
    html = html.replace("<STUDENT_NAME>", str(name))
    html = html.replace("<RANKING_ORDER>", str(ranking))
    html = html.replace("<SCORE_RANKING>", str(score))
    return html

def generate_content_ranking_html(data_df: pd.DataFrame, curr_email: str, template_html: str):
    content_ranking_html = None
    row_list = []
    current_score, current_name, current_rank =  None, None, None
    # create html content:
    for row in data_df.itertuples():
        if curr_email == row.email:
            current_rank = row.ranking
            current_name = row.name
            current_score = row.score
            # show current name
            row_content = ROW_HTML % (row.ranking, row.name, row.score)
        else:
            # hide other names
            row_content = ROW_HTML % (row.ranking, "XXX", row.score)
        row_list.append(row_content)


    if current_score is not None  and current_name is not None and current_rank is not None:
        # Post procesing
        content_ranking_html = postprocessing_content_html(
            template_html, 
            row_ranking_content= "\n".join(row_list),
            ranking=current_rank,
            name = current_name, 
            score = current_score

            )
    return content_ranking_html