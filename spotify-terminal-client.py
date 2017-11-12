import urllib.request, urllib.parse, urllib.error
import json

## this example follows the client authorization 

class spotiClient():
    import json
    # I'm going to create a client class to handle requests to spotify
    # including managing authorization.
    # This is different from Flickr where we just wrote one function
    
    def __init__(self):
        self.accessToken = None 
        self.spotifyAuth()      
        
    def spotifyAuth(self):
        """Method to actually handle authorization"""
        
        # Note: I put my client id and client secret in secrets.py 
        # and told git to ignore that file. You should too.
        from secrets import CLIENT_ID, CLIENT_SECRET
        import base64
                
        # Following documentation in https://developer.spotify.com/web-api/authorization-guide/#client_credentials_flow
        #
        # Spotify expects:
        # the Authorization in the *header*,
        # A Base 64 encoded string that contains the client ID and client secret key. The field must have the format: Authorization: Basic <base64 encoded client_id:client_secret>
        # grant_type = "client_credentials" as a parameter
    
        # build the header
        authorization =  base64.standard_b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode())
        headers = {"Authorization":"Basic "+authorization.decode()}
    
        # encode the params dictionary, note it needs to be byte encoded
        params = {"grant_type" : "client_credentials"}
        encodedparams = urllib.parse.urlencode(params).encode()
    
        # request goes to POST https://accounts.spotify.com/api/token
        request = urllib.request.Request('https://accounts.spotify.com/api/token', data=encodedparams, headers=headers)
        resp = urllib.request.urlopen(request)
    
        # I should do some error handling, but this is a quick example
        respdata = json.load(resp)
        self.accessToken = respdata['access_token']
        # Note that by default this token will expire in 60 minutes.
        # If your application will run longer, you will need a way to manage that. 
        
    def apiRequest(self,version="v1",endpoint="search",item=None,params=None):
        """Method for API calls once authorized. By default, it will execute a search.
        
        See https://developer.spotify.com/web-api/endpoint-reference/ for endpoints
        
        Items, e.g., a track ID, are passed in via the item parameter.
        Parameters, e.g., search parameters, are passed in via the params dictionary"""
        
        if self.accessToken is None:
            print("Sorry, you must have an access token for this to work.")
            return {}
        
        baseurl = "https://api.spotify.com/"
        endpointurl = "%s%s/%s"%(baseurl,version,endpoint)
        
        # are there any params we need to pass in?
        if item is not None:
            endpointurl =  endpointurl + "/" + item
        if params is not None:
            fullurl = endpointurl + "?" + urllib.parse.urlencode(params)
        
        headers = {"Authorization":"Bearer "+self.accessToken}
        request = urllib.request.Request(fullurl, headers=headers)
        resp = urllib.request.urlopen(request)
        
        # again, I should some error handling but I want to go back to making the practice exam
        return json.load(resp)
        
sclient = spotiClient()
searchresult = sclient.apiRequest(params={"type":"artist","q":"Metric"})

print(searchresult)
