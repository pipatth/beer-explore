import beerLoadData
import beer_similarity

def find_similar_beers(beerid, styleid):
    # get top 20 beers in style
    list_beer = [beerid]
    list_beer2 = beerLoadData.load_beers_in_style(styleid, 20)['beerid'].tolist()
    list_beer.extend(list_beer2)

    df = beerLoadData.load_reviews(list_beer)

    # get correlations
    list_sim = [beer_similarity.calc_similarity(df, beerid, x) for x in list_beer2]
    list_sim.sort(key = lambda x: x[1], reverse=True)

    # convert to pandas df
    df = beerLoadData.to_pd_table(list_sim)
    return df

def find_similar_beers_from_name(beername, breweryname, styleid):
    beerid = beerLoadData.get_beer_id(beername, breweryname)
    return find_similar_beers(beerid, styleid)
