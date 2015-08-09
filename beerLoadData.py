import sys
import pandas
import psycopg2

# method to connect to database
def connect():
    conn = psycopg2.connect(database="beerdb", user="postgres", password="postgres",
                            host="localhost")
    return conn

# load all reviews
def load_all_reviews():
    conn = connect()

    df = pandas.read_sql(
        '''
        SELECT revid, beerid, beername, breweryid, breweryname,
        userid, styleid, stylename, look, smell, taste, feel, overall, note
        FROM review
        ''', conn)
    conn.close()
    return df

# load reviews
def load_reviews(list_id):
    conn = connect()
    list_id = tuple([(str(x),) for x in list_id])

    df = pandas.read_sql(
        '''
        SELECT revid, beerid, beername, breweryid, breweryname,
        userid, styleid, stylename, look, smell, taste, feel, overall, note
        FROM review
        WHERE beerid IN %(list_id)s
        ''', conn, params={'list_id':list_id})
    conn.close()
    return df

# load beer info
def load_beers_in_style(style, n):
    conn = connect()
    style = (style,)
    n = (n,)
    df = pandas.read_sql(
        '''
        SELECT beerid, beername, breweryid, breweryname,
        styleid, stylename, abv, avail, ratings, reviews,
        ravg, pdev, wants, gots, ft
        FROM beer
        WHERE styleid = %(style)s
        ORDER BY ratings DESC
        LIMIT %(n)s
        ''', conn, params={'style':style, 'n':n})
    conn.close()
    return df

# load beer info
def load_all_beers():
    conn = connect()
    df = pandas.read_sql(
        '''
        SELECT beerid, beername, breweryid, breweryname,
        styleid, stylename, abv, avail, ratings, reviews,
        ravg, pdev, wants, gots, ft
        FROM beer
        ORDER BY ratings DESC
        ''', conn)
    conn.close()
    return df

# load single beer info
def load_one_beer(id):
    conn = connect()
    id = (id,)
    df = pandas.read_sql(
        '''
        SELECT beerid, beername, breweryid, breweryname,
        styleid, stylename, abv, avail, ratings, reviews,
        ravg, pdev, wants, gots, ft
        FROM beer
        WHERE beerid = %(id)s
        ''', conn, params={'id':id})
    conn.close()
    return df

# get style_name from style_id
def get_style_name(styleid):
    conn = connect()
    c = conn.cursor()
    styleid = (styleid,)
    c.execute(
        '''
        SELECT stylename
        FROM style
        WHERE style.styleid = %s
        ''', styleid)
    stylename = c.fetchall()[0][0]
    conn.close()
    return stylename

# get style_id from style_name
def get_style_id(stylename):
    conn = connect()
    c = conn.cursor()
    stylename = (stylename,)
    c.execute(
        '''
        SELECT styleid
        FROM style
        WHERE style.stylename = %s
        ''', stylename)
    styleid = c.fetchall()[0][0]
    conn.close()
    return styleid

# get beer_id from beer_name and brewery_name
def get_beer_id(beername, breweryname):
    conn = connect()
    c = conn.cursor()
    beername = (beername,)
    breweryname = (breweryname,)
    c.execute(
        '''
        SELECT beerid
        FROM beer
        WHERE beer.beername = %s AND beer.breweryname = %s
        ''', (beername, breweryname))
    beerid = c.fetchall()[0][0]
    conn.close()
    return beerid

# get beer_name and brewery_name from list of beer_ids
def get_beer_names(beerids):
    conn = connect()
    c = conn.cursor()
    list_id = tuple([(str(x),) for x in beerids])
    c.execute(
        '''
        SELECT beername, breweryname
        FROM beer
        WHERE beer.beerid IN %(list_id)s
        ''', {'list_id':list_id})
    beers = c.fetchall()
    conn.close()
    return beers

# convert result to pandas
def to_pd_table(list_sim):
    df1 = pandas.DataFrame(list_sim, columns=['beerid', 'sim'])

    ids = df1['beerid'].tolist()
    beers = get_beer_names(ids)
    df2 = pandas.DataFrame(beers, columns=['beername','breweryname'])

    df = df1.join(df2, how='inner')
    return df

def main(argv):
    df = load_all_reviews()
    df.to_csv(argv[1], index=False, encoding='utf-8')
    return

if __name__ == "__main__":
    main(sys.argv)

