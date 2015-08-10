import beerLoadData
import beerSimilarity
import sys

def find_similar_beers(beerid, styleid):
    # get top 20 beers in style
    list_beer = [beerid]
    list_beer2 = beerLoadData.load_beers_in_style(styleid, 20)['beerid'].tolist()
    list_beer.extend(list_beer2)

    df = beerLoadData.load_reviews(list_beer)

    # get correlations
    list_sim = [beerSimilarity.calc_similarity(df, beerid, x) for x in list_beer2]
    list_sim.sort(key = lambda x: x[1], reverse=True)

    # convert to pandas df
    df = beerLoadData.to_pd_table(list_sim)
    return df

def find_similar_beers_from_name(beername, breweryname, stylename):
    beerid = beerLoadData.get_beer_id(beername, breweryname)
    return find_similar_beers(beerid, beerLoadData.get_style_id(stylename))

def main(argv):
    print argv[3]
    print find_similar_beers_from_name(argv[1], argv[2], argv[3])
    return

if __name__ == '__main__':
    main(sys.argv)