import wikipedia
def get_wiki_article(article):
    wikipedia.set_lang("ru")
    try:
        return f'{wikipedia.summary(article)} {wikipedia.page(article).links}'[:4096]
    except wikipedia.WikipediaException:
        return "Не удалось найти информацию по этому запросу"