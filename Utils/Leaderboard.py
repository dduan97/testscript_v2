"""
I'm guessing this should end up being a "library" of functions that
interact with the leaderboard

Current functions:

leaderboard class that can be initialized with the api url, which has methods:
    print_leaderboard(num) prints the leaderboard
"""
import requests
import json
from SetupParser import ascii_encode_dict

class Leaderboard:
    def __init__(self, url, net_id):
        self.url = url
        self.net_id = net_id

    def print_leaderboard(self, week):
        """
        Takes in an assignment number and prints the leaderboard for that
        week. On success, it returns true, otherwise returns false
        """
        response = requests.get(self.url.format(week))
        if response.status_code != 200:
            print "Looks like the API done goofed!"
            return False
        else:
            rankings = map(ascii_encode_dict, response.json())
            print "\n"
            print "    NetId        Time"
            print "    -----        ----"
            for item in rankings:
                print "    {}".format(item["net_id"]) + " "*(13-len(item["net_id"])) + "{:2.3f}".format(item["time"])
            print "\n"
            return True

    def submit_time(self, week, time, username, net_id=None):
        """
        Takes in assignment number, time, username, and optionally net id, and 
        makes a post request to the API. Returns false on failure, true on 
        success
        """

        if not net_id:
            net_id = self.net_id

        post_url = self.url.format(week)
        data = {
            "net_id": net_id,
            "name": username,
            "time": time
        }
        data = json.dumps(data)
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(post_url, headers=headers, data=data)
        
        if response.status_code != 200:
            print "looks like the API request done goofed (response code {})".format(response.status_code)
            print response.json()
            return False

        return True