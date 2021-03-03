from bidhive_tendersearch.tender.scrape import perform_scrape


def run(*args):
    perform_scrape(
        clean="clean" in args, today="today" in args, scrape="scrape" in args
    )
