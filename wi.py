from wikiapi import WikiApi

import wikiapi

wiki = wikiapi.WikiApi()
wiki = WikiApi({ 'locale' : 'en'})
def get_info(prompt):
    article = wiki.get_article(prompt)
    return article


def get_results(prompt):
    results = wiki.find(prompt)
    return results