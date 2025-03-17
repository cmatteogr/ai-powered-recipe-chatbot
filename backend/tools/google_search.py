from serpapi import GoogleSearch


class SerpAPIClient:
    _instance = None

    def __new__(cls, api_key=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.api_key = api_key
        return cls._instance

    def search_by_query(self, query: str, engine: str = 'google', location: str = 'United States',
                        google_domain: str = 'google.com', gl: str = 'us', hl: str = 'en') -> dict:
        """
        Search Google Search API
        :param query: User query
        :param engine: Engine for search
        :param location: location for search
        :param google_domain: google domain for search
        :param gl: global language for search
        :param hl: historical language for search
        :return: results dictionary
        """
        print('Searching Google Search API, query: {}'.format(query))
        # define the search parameters
        search_params = {
            "engine": engine,
            "q": query,
            "location": location,
            "google_domain": google_domain,
            "gl": gl,
            "hl": hl,
            "api_key": self.api_key
        }
        # search via Google Search
        search = GoogleSearch(search_params)
        # get search results
        results = search.get_dict()

        # check search result
        if 'error' in results.keys():
            raise Exception(results['error'])

        # return results
        return results
