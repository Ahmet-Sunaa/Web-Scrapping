from celery import shared_task , group
from .models import Products
import requests
from bs4 import BeautifulSoup
from lxml import etree


urls_n11=[]
urls_hepsiburada=[]
urls_mediamarkt=[]
urls_trendyol=[]

head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

for i in range(1,10):
   urls_hepsiburada.append("https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa="+str(i))
   urls_n11.append("https://www.n11.com/bilgisayar/dizustu-bilgisayar?pg="+str(i))
   urls_trendyol.append("https://www.trendyol.com/laptop-x-c103108?pi="+str(i))

for i in range(1,2):
    urls_mediamarkt.append("https://www.mediamarkt.com.tr/tr/category/_laptop-504926.html?page="+str(i))



def scrape_hepsiburada(urls,head):
    feature_data=[]
    scraped_data=[]
    obj_list=[]
    for url in urls:
        req=requests.get(url,headers=head)
        soup=BeautifulSoup(req.content,"html.parser")
        items=soup.findAll("li",class_="productListContent-zAP0Y5msy8OHn5z7T_K_")
        for item in items:
            if item.find("a").get("href")[0] == '/':
                demo={
                    "title":item.find("a").get("title"),
                    "url":"https://www.hepsiburada.com"+item.find("a").get("href"),
                    }
                scraped_data.append(demo)
    for data in scraped_data:
        req_for_feature=requests.get(data['url'],headers=head)
        soup=BeautifulSoup(req_for_feature.content,"html.parser")
        dom=etree.HTML(str(soup))
        item_url=soup.find("img",class_="product-image").get("src")
        item_title=soup.find("img",class_="product-image").get("title")
        if soup.find("table",class_="data-list tech-spec") != None:
            items=soup.find("table",class_="data-list tech-spec").find_all("tr")
        for item in items:
            if item.find("a") != None and item.find("th") != None :
                obj={
                        item.find("th").text:item.find("a").text,
                        "price":dom.xpath('//*[@id="offering-price"]/span[1]')[0].text.replace(".",""),
                        "url":data['url'],
                        "image_url":item_url,
                        "brand":item_title[ : item_title.index(" ")],
                        "title":item_title,
                        "model":"Belirtilmemiş",
                        "seller_name":"HepsiBurada"
                    }
                obj_list.append(obj)
        data={}
        for ob in obj_list:
            for key , value in ob.items():
                data[key]=value
        feature_data.append(data)        
    return feature_data

def scrape_n11(urls,head):
    scraped_data=[]
    feature_data=[]
    obj_list=[]
    for url in urls:
        req=requests.get(url,headers=head)
        soup=BeautifulSoup(req.content,"html.parser")
        items=soup.find_all("li",class_="column")
        for item in items:
            obj={
                "title":item.find("a",class_="plink").get("title").strip(),
                "price":item.find("input",class_="productRealPrice").get("value"),
                "url":item.find("a",class_="plink").get("href"),
                "image_url":item.find("img",class_="lazy cardImage").get("data-original")
                }
            scraped_data.append(obj)
        for data in scraped_data:
            req_for_feature=requests.get(data['url'],headers=head)
            soup=BeautifulSoup(req_for_feature.content,"html.parser")
            item_rating=soup.find("div",class_="ratingCont").find("strong").text
            items=soup.find_all("li",class_="unf-prop-list-item")
            for item in items:
                demo={
                    item.find("p",class_="unf-prop-list-title").text:item.find("p",class_="unf-prop-list-prop").text,
                    "title":data['title'],
                    "price":data['price'],
                    "url":data['url'],
                    "image_url":data['image_url'],
                    "seller_name":"N11",
                    "rating":item_rating
                    }
                obj_list.append(demo)
            data={}
            for ob in obj_list:
                for key , value in ob.items():
                    data[key]=value
            feature_data.append(data)
    return feature_data

def scrape_trendyol(urls,head):
    feature_data=[]
    obj_list=[]
    scraped_data=[]
    for url in urls:
        req=requests.get(url,headers=head)
        soup=BeautifulSoup(req.content,"html.parser")
        items=soup.findAll("div",class_="p-card-wrppr with-campaign-view")
        for item in items:
            demo={
                    "brand":item.find("span",class_="prdct-desc-cntnr-ttl").text,
                    "title":item.find("span",class_="prdct-desc-cntnr-name").text,
                    "price":item.find("div",class_="prc-box-dscntd").text.replace(" TL","").replace(".","").replace(",","."),
                    "url":"https://www.trendyol.com"+item.find("a").get("href"),
                    "image_url":"https://www.trendyol.com"+item.find("img",class_="p-card-img").get("src")
                }
            scraped_data.append(demo)
    for data in scraped_data:
        req_for_feature=requests.get(data['url'],headers=head)
        soup=BeautifulSoup(req_for_feature.content,"html.parser")
        items=soup.find_all("li",class_="detail-attr-item")
        for item in items:
            obj={
                    item.find("span").text:item.find("b").text,
                    "Sabit Disk Tipi":"SSD",
                    "brand":data['brand'],
                    "title":data['title'],
                    "price":data['price'],
                    "url":data['url'],
                    "image_url":data['image_url'],
                    "seller_name":"Trendyol"
                }
            obj_list.append(obj)
        data={}
        for ob in obj_list:
            for key , value in ob.items():
                data[key]=value
        feature_data.append(data)
    return feature_data

def  scrape_mediamarkt(urls,head):
    scraped_data=[]
    feature_data=[]
    for url in urls:
        req=requests.get(url,headers=head)
        soup=BeautifulSoup(req.content,"html.parser")
        items=soup.find_all("div",class_="product-wrapper")
        for item in items:
            demo={
                "title":item.find("img").get("alt"),
                "brand":item.find("div",class_="content").find("img").get("alt"),
                "url":"https://www.mediamarkt.com.tr"+item.find("span").get("data-clickable-href"),
                }
            scraped_data.append(demo)
        for data in scraped_data:
            req=requests.get(data['url'],headers=head)
            soup=BeautifulSoup(req.content,"html.parser")
            item_image="https:"+soup.find("a",class_="zoom").get("href")
            dom=etree.HTML(str(soup))
            if dom.xpath('//*[@id="features"]/section[8]/dl/dt[1]')[0].text != 'Ön Kamera:' and dom.xpath('//*[@id="features"]/section[3]/dl/dt[3]')[0].text != 'İşlemci Sayısı:' and dom.xpath('//*[@id="features"]/section[8]/dl/dt[1]')[0].text != 'Boyutlar (GxYxD) / Ağırlık:' and dom.xpath('//*[@id="product-details"]/div[2]/dl/dt[4]')[0].text != 'Çözünürlük:' :
                 demo={
                        dom.xpath('//*[@id="features"]/section[1]/dl/dt[1]')[0].text.replace(":",""):dom.xpath('//*[@id="features"]/section[1]/dl/dd[1]')[0].text.split("/")[1],
                        dom.xpath('//*[@id="features"]/section[2]/dl/dt[2]')[0].text.replace(":",""):dom.xpath('//*[@id="features"]/section[2]/dl/dd[2]')[0].text,
                        dom.xpath('//*[@id="features"]/section[3]/dl/dt[3]')[0].text.replace(":",""):dom.xpath('//*[@id="features"]/section[3]/dl/dd[3]')[0].text,
                        "İşlemci Nesli":"Belirtilmemiş",
                        dom.xpath('//*[@id="features"]/section[8]/dl/dt[1]')[0].text.replace(":",""):dom.xpath('//*[@id="features"]/section[8]/dl/dd[1]')[0].text,
                        dom.xpath('//*[@id="product-details"]/div[2]/dl/dt[4]')[0].text.replace(":",""):dom.xpath('//*[@id="product-details"]/div[2]/dl/dd[4]')[0].text,
                        "Disk Tipi":"SSD",
                         "title":data['title'],
                        "brand":data['brand'],
                        "url":data['url'],
                        "image_url":item_image,
                        "seller_name":"MediaMarkt",
                        "price":dom.xpath('//*[@id="product-details"]/div[3]/div[1]/meta[2]/@content')[0]
                    }
            feature_data.append(demo)
    return feature_data
@shared_task
def start_task():
   data_hepsi=scrape_hepsiburada(urls_hepsiburada,head)
   for data in data_hepsi:
      obj=Products()
      obj.title=data['title']
      obj.brand=data['brand'].upper().replace(" ","")
      obj.url=data['url']
      obj.picture_url=data['image_url']
      obj.price=data['price']
      obj.model=data['model']
      obj.screen_size=data['Ekran Boyutu'].replace(" ","").replace(".",",").replace("inç","inc")
      obj.ram=data['Ram (Sistem Belleği)'].replace(" ","").replace(" ","")
      obj.operating_system="FreeDos" if data['İşletim Sistemi'].upper().__contains__("DOS") else data['İşletim Sistemi']
      obj.processor_model=data['İşlemci Tipi']
      obj.processor_generation=data['İşlemci Nesli']
      obj.seller_name=data['seller_name']
      obj.disk_size=data['SSD Kapasitesi']
      obj.disk_type="SSD"
      obj.save()
   data_n11=scrape_n11(urls_n11,head)
   for data in data_n11:
      obj=Products()
      obj.title=data['title']
      obj.brand=data['Marka'].upper().replace(" ","")
      obj.url=data['url']
      obj.picture_url=data['image_url']
      obj.price=data['price']
      obj.model=data['Model']
      obj.screen_size=data['Ekran Boyutu'].replace('"','inc').replace(".",",").replace(" ","")
      obj.ram=data['Bellek Kapasitesi'].replace(" ","").replace(" ","")
      obj.operating_system="FreeDos" if data['İşletim Sistemi'].upper().__contains__("DOS") else data['İşletim Sistemi']
      obj.processor_model=data['İşlemci Modeli']
      obj.processor_generation="Belirtilmemiş"
      obj.seller_name=data['seller_name']
      obj.disk_size=data['Disk Kapasitesi']
      obj.disk_type=data['Disk Türü']
      obj.save()
   data_trendyol=scrape_trendyol(urls_trendyol,head)
   for data in data_trendyol:
      obj=Products()
      obj.title=data['title']
      obj.brand=data['brand'].upper().replace(" ","")
      obj.url=data['url']
      obj.picture_url=data['image_url']
      obj.price=data['price']
      obj.model="Belirtilmemiş"
      obj.screen_size=data['Ekran Boyutu'].replace(" ","").replace("inç","inc").replace(".",",")
      obj.ram=data['Ram (Sistem Belleği)'].replace(" ","")
      obj.operating_system="FreeDos" if data['İşletim Sistemi'].upper().__contains__("DOS") else data['İşletim Sistemi']
      obj.processor_model=data['İşlemci Tipi']
      obj.processor_generation=data['İşlemci Nesli']
      obj.seller_name=data['seller_name']
      obj.disk_size=data['SSD Kapasitesi']
      obj.disk_type="SSD"
      obj.save()
   data_mediamarkt=scrape_mediamarkt(urls_mediamarkt,head)
   for data in data_mediamarkt:
      obj=Products()
      obj.title=data['title']
      obj.brand=data['brand'].upper().replace(" ","")
      obj.url=data['url']
      obj.picture_url=data['image_url']
      obj.price=data['price']
      obj.model="Belirtilmemiş"
      obj.screen_size=data['Ekran Boyutu'].replace(" ","").replace("inç","inc").replace(".",",")
      obj.ram=data['RAM Bellek Boyutu'].replace(" ","").upper()
      obj.operating_system="FreeDos" if data['İşletim Sistemi'].upper().__contains__("DOS") else data['İşletim Sistemi']
      obj.processor_model=data['İşlemci Modeli']
      obj.processor_generation=data['İşlemci Nesli']
      obj.seller_name=data['seller_name']
      obj.disk_size=data['Sabit disk kapasitesi']
      obj.disk_type=data['Disk Tipi']
      obj.save()
   
    