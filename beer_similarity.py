import pandas
import numpy

def get_review_metrics_by_id(df, beer1, beer2):
    reviews1 = df[df.beerid == beer1][['userid', 'look', 'smell', 'taste', 'feel', 'overall']]
    reviews2 = df[df.beerid == beer2][['userid', 'look', 'smell', 'taste', 'feel', 'overall']]
    reviews = pandas.merge(reviews1, reviews2, how='inner', on='userid')
    if len(reviews) > 0:
        return reviews
    else:
        return None

def calc_similarity(df, beer1, beer2):
    dfreviews = get_review_metrics_by_id(df, beer1, beer2)

    # get correlations
    correl = []
    correl.append(dfreviews['look_x'].corr(dfreviews['look_y']))
    correl.append(dfreviews['smell_x'].corr(dfreviews['smell_y']))
    correl.append(dfreviews['taste_x'].corr(dfreviews['taste_y']))
    correl.append(dfreviews['feel_x'].corr(dfreviews['feel_y']))
    correl.append(dfreviews['overall_x'].corr(dfreviews['overall_y']))

    # weighted average
    weights = [0,1,1,1,2]
    wcorrel = (numpy.array(correl) * numpy.array(weights))/numpy.sum(weights)
    avg = round(float((numpy.sum(wcorrel))),3)
    return [beer2, avg]

