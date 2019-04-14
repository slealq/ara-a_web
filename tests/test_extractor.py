#!/usr/bin/env python3

from datetime import date
from oddcrawler.webpage_extractors import monumental_extractor
from logging import (getLogger, FileHandler, StreamHandler, Formatter, DEBUG,
                     ERROR)


def test_get_news_urls(webpage_extractor):
    urls = webpage_extractor.get_news_urls(date.today())
    assert isinstance(urls, list)

    return urls

def test_extract_text_from_news(webpage_extractor):
    """Needs `get_news_urls` to have been run first. Otherwise, assertion
    of news_urls will fails.

    It's expected that the result is a dictionary, and it contains urls
    as keys and text of the news as values.
    """

    webpage_extractor.news_urls = ['http://www.monumental.co.cr/2019/04/12/contraloria-duda-de-solvencia-financiera-de-esph-y-senala-debilidades-de-control-interno/', 'http://www.monumental.co.cr/2019/04/12/recope-solicita-aumento-de-%c2%a273-por-litro-en-gasolina-super-y-%c2%a267-en-la-regular/', 'http://www.monumental.co.cr/2019/04/12/autoridades-activan-operativo-para-disminuir-accidentes-y-muertes-violentas-en-semana-santa/', 'http://www.monumental.co.cr/2019/04/12/operativo-contra-piques-en-pavas-dejo-vehiculos-alcohol-y-droga-decomisados/', 'http://www.monumental.co.cr/2019/04/12/pais-declara-estado-de-emergencia-por-listas-de-espera-de-donacion-y-trasplante-de-organos/', 'http://www.monumental.co.cr/2019/04/12/exdiputada-alexandra-loria-presenta-recurso-de-amparo-contra-camiseta-de-la-ucr-favor-del-aborto/', 'http://www.monumental.co.cr/2019/04/12/ctp-autorizo-25-empresas-de-buses-para-aumentar-flotilla-durante-semana-santa/', 'http://www.monumental.co.cr/2019/04/12/el-detalle-del-bano-de-mujeres-del-estadio-del-liverpool-que-esta-recorriendo-el-mundo/', 'http://www.monumental.co.cr/2019/04/12/zidane-contaria-con-keylor-navas-para-la-proxima-temporada/', 'http://www.monumental.co.cr/2019/04/12/los-mensajes-del-ex-general-chavista-hugo-carvajal-que-buscaban-un-acuerdo-con-la-justicia-de-eeuu-antes-de-ser-arrestado/', 'http://www.monumental.co.cr/2019/04/12/fuerte-sequia-por-el-fenomeno-del-nino-ocasiona-que-el-pais-cuente-con-un-55-menos-de-agua/', 'http://www.monumental.co.cr/2019/04/12/decomisan-armas-en-casa-de-extranjero-que-hirio-de-bala-a-dos-policias-en-bagaces/', 'http://www.monumental.co.cr/2019/04/12/visitara-la-playa-en-semana-santa-tenga-precaucion-con-las-fuertes-mareas-que-se-presentan-en-esta-epoca/', 'http://www.monumental.co.cr/2019/04/12/conapam-pide-incluir-adultos-mayores-en-actividades-familiares-durante-semana-santa/', 'http://www.monumental.co.cr/2019/04/12/exsacerdote-mauricio-viquez-entre-los-mas-buscados-de-la-interpol/', 'http://www.monumental.co.cr/2019/04/12/masiva-visitacion-a-zonas-protegidas-atenta-contra-fauna-silvestre-durante-semana-santa/', 'http://www.monumental.co.cr/2019/04/12/fuerte-respaldo-encuesta-revela-que-solo-el-4-de-los-ticos-se-opone-las-vacunas/', 'http://www.monumental.co.cr/2019/04/12/avanza-en-el-congreso-plan-que-prohibe-casas-de-empeno-abrir-en-horario-nocturno/', 'http://www.monumental.co.cr/2019/04/12/banco-de-sangre-requiere-120-donadores-por-dia-para-atender-demanda-de-semana-santa/', 'http://www.monumental.co.cr/2019/04/12/diputada-cuestiona-publicidad-de-evento-que-promueve-bodas-entre-parejas-del-mismo-sexo/', 'http://www.monumental.co.cr/2019/04/12/usuarios-podran-hacer-propuestas-para-agilizar-los-servicios-de-la-ccss/', 'http://www.monumental.co.cr/2019/04/12/jair-bolsonaro-anuncio-un-aguinaldo-para-los-beneficiarios-de-subsidios-estatales-en-brasil/', 'http://www.monumental.co.cr/2019/04/12/tragedia-en-rio-de-janeiro-al-menos-dos-personas-murieron-por-el-derrumbe-de-dos-edificios/']

    assert isinstance(webpage_extractor.news_urls, list) \
        and webpage_extractor.news_urls

    text = webpage_extractor.extract_text_from_news()

    assert isinstance(text, dict)

    return text


if __name__ == "__main__":
    # Configure logger: oddcrawler needsd to be the top logger
    logger = getLogger('oddcrawler')
    logger.setLevel(DEBUG)
    # create file file handler
    fh = FileHandler('extractor_test.log')
    fh.setLevel(DEBUG)
    # create console handler
    ch = StreamHandler()
    ch.setLevel(ERROR)
    # create formatter and add it to handlers
    formatter = Formatter('%(levelname)s %(asctime)-15s %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    # Begin first test
    logger.info('Begin Monumental get_news_urls test')
    monumental_extractor = monumental_extractor()
    # urls = test_get_news_urls(monumental_extractor)
    # print(urls)

    # Test the text extraction
    test_extract_text_from_news(monumental_extractor)

    # Test for other extractors might go here
