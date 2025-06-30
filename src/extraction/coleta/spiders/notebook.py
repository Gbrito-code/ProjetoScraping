import scrapy


class NotebookSpider(scrapy.Spider):
    name = "notebook"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebook#D[A:notebook]"]
    page_count = 1
    max_page = 10 # Limitar a quantidade de páginas para evitar bloqueios

    def parse(self, response):
        #aqui vamos pegar todos os produtos da pagina
        products = response.css("div.ui-search-result__wrapper")
        
        for product in products:
            #variavel que vai pegar o primeiro e segundo preço
            prices = product.css("span.andes-money-amount__fraction::text").getall()
            #yield retorna varios itens
            
            yield {
                "marca": product.css("span.poly-component__brand::text").get(),
                "nome": product.css("a.poly-component__title::text").get(),
                #Exercicio para pegar as demais informacoes
                "vendedor": product.css("span.poly-component__seller::text").get(),
                "avaliacao": product.css("span.poly-reviews__rating::text").get(),
                "quantidade_de_avaliacao": product.css("span.poly-reviews__total::text").get(),
                #O preço é mais complicado, pois tem dois precos.
                #O primeiro é o preço real e o segundo é o preço promocional
                #"price": product.css("span.andes-money-amount__fraction::text").get(),
                #vamos criar um objeto/lista que vai pegar todos os elementos que tem a classe "andes-money-amount__fraction"
                "preço_antigo": prices[0] if len(prices) > 0 else None,
                "preço_promocional": prices[1] if len(prices) > 1 else None,
            }
        #proxima pagina até 10 paginas
        #se a pagina atual for menor que a pagina maxima, vamos pegar a proxima pagina
        #Respeite o robots.txt – o Mercado Livre não permite scraping excessivo.
        #trocar para False para não respeitar o robots.txt em settings.py
        if self.page_count < self.max_page:
            self.page_count += 1
            offset = 48 * (self.page_count - 1)
            next_page_url = f"https://lista.mercadolivre.com.br/informatica/portateis-acessorios/notebooks/notebook_Desde_{offset}_NoIndex_True"
            yield scrapy.Request(url=next_page_url, callback=self.parse)