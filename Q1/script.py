import html, urllib
import time, requests, re, json, csv

# API_KEY = ""

# Collect top 300 comedies with primary release since 2000
# This needs to be called 15 times (20 results/page) 

def req_comedies(API_KEY):
    comedies = []
    page_num = 1
    with open('movie_ID_name.csv','w') as csvfile:
        m_write = csv.writer(csvfile, delimiter=',',quotechar='"')
        while page_num <16:
            response = requests.get("https://api.themoviedb.org/3/discover/movie?language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page={}&primary_release_date.gte=2000-01-01&with_genres=35&api_key={}".format(page_num,API_KEY))
            decoded = json.loads(response.text)
            for movie in decoded['results']:
                m_write.writerow([int(movie["id"]), movie["title"]])
                comedies.append(int(movie["id"]))
            page_num = page_num + 1
            time.sleep(.25)
    
    return(comedies)

def find_similar(comdey,API_KEY):
    with open('movie_ID_sim_movie_ID.csv','w') as csvfile:
        m_write = csv.writer(csvfile, delimiter=',',quotechar='"')
        similar = []
        for mov_id in comdey:
            try:
                sim_mov = 0
                response = requests.get("https://api.themoviedb.org/3/movie/{}/similar?language=en-US&page=1&sort_by=popularity.desc&include_adult=false&api_key={}".format(mov_id,API_KEY))
                decoded = json.loads(response.text)
                for movie in decoded['results']:
                    if sim_mov < 5:
                        pair_id = int(movie["id"])
                        if mov_id < pair_id:
                            pair = [mov_id,pair_id]
                        else:
                            pair = [mov_id,pair_id]
                        if (pair and [pair_id,mov_id]) not in similar:
                            similar.append(pair)
                            m_write.writerow(pair)
                            sim_mov = sim_mov + 1
                    else:
                        break
                time.sleep(.25)
            except KeyError:
                print(mov_id)
    
def main(args):
    # start = time.time()
    # Collect Data and Write to CSV
    movis = req_comedies(args[1])
    # Find Similar Movies and Write to CSV
    find_similar(movis,args[1])
    # print("Runtime: {} seconds".format(time.time()-start))
if __name__ == "__main__":
    import sys
    main(sys.argv)