from kingfisher_scrapy.base_spider import CompressedFileSpider, PeriodicSpider, browser_user_agent
from kingfisher_scrapy.util import components


class UruguayHistorical(CompressedFileSpider, PeriodicSpider):
    """
    Domain
      Agencia Reguladora de Compras Estatales (ARCE)
    Spider arguments
      from_date
        Download only data from this month onward (YYYY format). Defaults to '2002'.
      until_date
        Download only data until this month (YYYY format). Defaults to '2017'.
    Bulk download documentation
      https://www.gub.uy/agencia-compras-contrataciones-estado/datos-y-estadisticas/datos/open-contracting
    """
    name = 'uruguay_historical'
    data_type = 'release_package'

    # the files takes too long to be downloaded, so we increase the download timeout
    download_timeout = 1000
    user_agent = browser_user_agent

    # PeriodicSpider variables
    date_format = 'year'
    default_from_date = '2002'
    default_until_date = '2017'
    pattern = 'https://www.gub.uy/agencia-compras-contrataciones-estado/sites' \
              '/agencia-compras-contrataciones-estado/files/2019-04/OCDS-{}.zip'

    def get_formatter(self):
        return components(-1)
