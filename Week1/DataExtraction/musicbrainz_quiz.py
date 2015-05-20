

# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at,
# but you will not be able to run any queries through our UI.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    name_query = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    name_results = [artist["name"] for artist in name_query["artists"] if artist["name"] == "First Aid Kit"]    
    print "First Aid Kit occurrences: ", len(name_results)    

    area_query = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    queen_begin_area = area_query["artists"][0]["begin-area"]["name"]
    print "Queen begin area is: ", queen_begin_area
     
    beatles_query = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    aliases = [alias["name"] for alias in beatles_query["artists"][0]["aliases"] if alias["locale"] == "es"]
    print "Beatles Spanish alias is: ", aliases

    nirvana_query = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    disambiguation = nirvana_query["artists"][0]["disambiguation"]
    print "Nirva disambigution:  ", disambiguation

    one_direction_query = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    form_date = one_direction_query["artists"][0]["life-span"]["begin"]
    print "One Direction was formed in: ", form_date

if __name__ == '__main__':
    main()

