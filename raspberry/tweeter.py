from TwitterAPI import TwitterAPI, TwitterResponse


class Tweeter:

    def __init__(self,
                 consumer_key='DEn9Nj15tvfBqwPSzIeuT2ODh',
                 consumer_secret='VMmNzvPhEokH2fU7piLynB5zLBFv6rhDK7cfh39pMLehdCzFAM',
                 access_token_key='992144513924812801-guuVhQnFlB6lU27FmEF5vMxPmyt3FrE',
                 access_token_secret='EAqH6F8z2kWcTPK0ffKn7CIsz6Dj7rOqEcgEQQ1fGv6k3'):

        self.api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

    def tweet(self, status, picture_filename=None):
        data = None
        try:
            with open(picture_filename, 'rb') as file:
                data = file.read()
        except Exception as e:
            print(e)

        if data:
            response = self.api.request('statuses/update_with_media',
                                    {'status': status},
                                    {'media[]': data}
                                    )
        else:
            response = self.api.request('statuses/update', {'status': status})

        return response

    @staticmethod
    def extract_media_url(response: TwitterResponse):
        try:
            return response.json()['entities']['media'][0]['media_url']
        except Exception:
            return ""
