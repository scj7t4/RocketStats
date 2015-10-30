import urllib
import urllib2
import logging
import requests
import urlparse
import sys

#logging.basicConfig(level=logging.DEBUG)

AUTH_CODE = "140000002B1B5F00ED94A49A636E2702010010014ACB2F561800000001000000020000006C5AE5D8000000003D2C7B0002000000B80000003800000004000000636E27020100100116DC03006C5AE5D88A01A8C00000000079B02756F95F43560100E4780000010000FA050000000000504A208C1DF2FE18DDFDEBE1F75F9431A9224F2DF08E4ED869F4AF570D2E2978AF9A2835189D6D3AFEF45E53B98703E917197D31C559323EC7E242564944984486F066D96083D8179DDBA7FD2702A367D00593E8DCE03C70E9889051B177E7D25E46BE2AD58B72AA24B7DCFCCFE16085BECE098471CE5712196C37BABD251668"
SECRET_KEY = "dUe3SE4YsR8B0c30E6r7F2KqpZSbGiVx"
PLAYER_NAME = "Bamans"
PLAYER_ID = 76561197996404323
CALL_PROC_KEY = "pX9pn8F4JnBpoO8Aa219QC6N7g18FJ0F"

class RocketLeagueAPI(object):
    db = 'BattleCars_Prod'
    db_version = '00.03.0011-00.01.0011'
    API_URL = "https://psyonix-rl.appspot.com/callproc105/"
    LOGIN_URL = "https://psyonix-rl.appspot.com/login105/"
    KEEP_ALIVE_URL = "https://psyonix-rl.appspot.com/Population/UpdatePlayerCurrentGame/"
    BUILD_ID = 144580275


    def __init__(self, call_proc_key):
        self.call_proc_key = call_proc_key
        pass

    def UseSession(self, call_proc_key, session_id):
        self.session_id = session_id

    def Login(self, secret_key, player_name, player_id, auth_code, call_proc_key):
        """
        Doesn't work -- auth code changes every time the program is launched, don't know how to generate.
        """
        hdrs = {
            'User-Agent': 'UE3-TA,UE3Ver(10897)',
            'DB': self.db,
            'DBVersion': self.db_version,
            'LoginSecretKey': secret_key,
        }
        payload = {
            'PlayerName': player_name,
            'PlayerID': player_id,
            'Platform': 'Steam',
            'BuildID': self.BUILD_ID,
        }
        req = requests.post(self.LOGIN_URL, data=payload, headers=hdrs)
        if req.text != "1" or req.status_code != 200:
            raise ValueError("Server didn't respond with 1 (Login Step 1)")
        self.session_id = req.headers['SessionID']
        print "Got session ID {}".format(self.session_id)
        """
        hdrs['SessionID'] = self.session_id
        payload['AuthCode'] = self.auth_code
        payload['IssuerID'] = 0
        req = requests.post(self.LOGIN_URL, data=payload, headers=hdrs)
        print req.text
        if req.text != "1" or req.status_code != 200:
            raise ValueError("Server didn't respond with 1 (Login Step 2)")
        """
        self.KeepAlive()

    def KeepAlive(self):
        hdrs = self.MakeHeaders()
        payload = {
            'PlaylistID': 0,
            'NumLocalPlayers': 1
        }
        req = requests.post(self.KEEP_ALIVE_URL, data=payload, headers=hdrs)
        if req.text != "" or req.status_code != 200:
            print "KA rsp {}".format(req.text)
            raise ValueError("Server didn't like keep alive message")
         
    def MakeHeaders(self):
        hdrs = {
            'User-Agent': 'UE3-TA,UE3Ver(10897)',
            'CallProcKey': self.call_proc_key,
            'DB': self.db,
            'DBVersion': self.db_version,
            'SessionID': self.session_id,
        }
        return hdrs

    def MakePayload(self, commands):
        """
        Commands is a list of dictionaries. Each dictionary contains two keys:
        proc: the procedure to call.
        args: the list of arguments for each procedure.
        """
        d = {
            'Proc[]': []
        }
        for i, c in enumerate(commands):
            d['Proc[]'].append(c['proc'])
            args = c.get('args', [])
            if args:
               d['P{}P[]'.format(i)] = args
        return d

    def MakeRequest(self, commands):
        payload = self.MakePayload(commands)
        hdrs = self.MakeHeaders()
        req = requests.post(self.API_URL, data=payload, headers=hdrs)
        resp = req.text
        print resp
        cmd_keys = [ k['proc'] for k in commands ]
        response = {}
        resp_chunks = resp.split("\r\n\r\n")
        proc_n_response = zip(cmd_keys, resp_chunks)
        print proc_n_response
        for p,r in proc_n_response:
            response[p] = map(urlparse.parse_qs, r.split("\r\n"))
        return response

    def __getattr__(self, name):
        if name.find('Get') == 0:
            return lambda *args: self.MakeRequest([{'proc': name, 'args': list(args)}])
        raise AttributeError("RocketStatsAPI doesn't have attribute {}".format(name))

    def GetRegionList(self):
        cmd = [{
            'proc': sys._getframe().f_code.co_name, #Gets function name
            'args': ["INTv2"]
        }]
        return self.MakeRequest(cmd)
 
    def GetNetworkAttribute(self, proc, network, user=[]):
        cmd = [{
            'proc': proc+network,
            'args': ident
        }]
        return self.MakeRequest(cmd)

    def GetPlayerSkillAndRankPoints(self, network, user):
        return GetNetworkAttribute(self, sys._getframe().f_code.co_name, network, user)
        
    def GetPlayerTitles(self, network, user):
        return GetNetworkAttribute(self, sys._getframe().f_code.co_name, network, user)
       
    def GetSkillLeaderboard(self, skilltype):
        cmd = [{
            'proc': sys._getframe().f_code.co_name, #Gets function name
            'args': [skilltype]
        }]
        return self.MakeRequest(cmd)
    
    def GetPlayerProductAwards(self, network, user):
        return GetNetworkAttribute(self, sys._getframe().f_code.co_name, network, user)
        
"""
&Proc[]=GetSeasonalRewards
&Proc[]=GetGenericDataAll
&Proc[]=GetRegionList&P2P[]=INTv2
&Proc[]=GetDLCSteam
&Proc[]=GetPlayerSkillAndRankPointsSteam&P4P[]=76561197996404323
&Proc[]=GetPlayerTitlesSteam&P5P[]=76561197996404323
&Proc[]=GetSkillLeaderboard&P6P[]=10
&Proc[]=GetSkillLeaderboard&P7P[]=11
&Proc[]=GetSkillLeaderboard&P8P[]=12
&Proc[]=GetSkillLeaderboard&P9P[]=13
&Proc[]=GetPlayerProductAwardsSteam
&P10P[]=76561197996404323
"""

"""

&Proc[]=GetLeaderboard&P0P[]=Wins&P0P[]=100&Proc[]=GetLeaderboardValueForUserSteam&P1P[]=76561197996404323&P1P[]=Wins

"""

#req = requests.post("https://psyonix-rl.appspot.com/callproc105/", data=payload, headers=hdrs)

rkt = RocketLeagueAPI(CALL_PROC_KEY)
rkt.Login(SECRET_KEY, PLAYER_NAME, PLAYER_ID, AUTH_CODE, CALL_PROC_KEY)
#rkt.UseSession("da05f2d2eb515488f18bc839b89e5f5a")

print rkt.GetLeaderboardValueForUserSteam(PLAYER_ID, "Wins")
