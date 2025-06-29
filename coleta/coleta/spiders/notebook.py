import scrapy


class NotebookSpider(scrapy.Spider):
    name = "notebook"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebook#D[A:notebook]"]
    start_page = 1
    max_pages = 10  # Limitar a quantidade de páginas para evitar bloqueios

    def parse(self, response):
        #aqui vamos pegar todos os produtos da pagina
        products = response.css("div.ui-search-result__wrapper")
        
        for product in products:
            #variavel que vai pegar o primeiro e segundo preço
            prices = product.css("span.andes-money-amount__fraction::text").getall()
            #yield retorna varios itens
            
            yield {
                "brand": product.css("span.poly-component__brand::text").get(),
                "name": product.css("a.poly-component__title::text").get(),
                #Exercicio para pegar as demais informacoes
                "seller": product.css("span.poly-component__seller::text").get(),
                "reviews_rating_number": product.css("span.poly-reviews__rating::text").get(),
                "reviews_amount": product.css("span.poly-reviews__total::text").get(),
                #O preço é mais complicado, pois tem dois precos.
                #O primeiro é o preço real e o segundo é o preço promocional
                #"price": product.css("span.andes-money-amount__fraction::text").get(),
                #vamos criar um objeto/lista que vai pegar todos os elementos que tem a classe "andes-money-amount__fraction"
                "old_money": prices[0] if len(prices) > 0 else None,
                "new_money": prices[1] if len(prices) > 1 else None,
            }
            
            
        #navegar para a proxima pagina
        #Sempre que tiver espaço na classe, coloca botão .
        next_page = response.css("li.andes-pagination__button.andes-pagination__button--next::attr(href)").get()
        
        #Agora vamos falar para o scrapy que queremos navegar para a proxima pagina até o final
        #mas podemos ter problema pegando muitas paginas (pode demorar ou podemos ser bloqueados)
        #vamos adicionar as variaiveis de controle para limitar a quantidade de paginas
        yield response.Request(url=next_page, callback=self.parse) if next_page else None