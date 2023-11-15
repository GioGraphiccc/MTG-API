class Card:
    def __init__(self, id, card_name, card_type, set_name,  price, priceF, rarity, colors, keywords,
             cmc, mana_cost, legalityC, legalityS, power_toughness, tcgplayer_id, img_url, desc, desc2):
        
        self.id = id
        self.card_name = card_name
        self.card_type = card_type
        self.set_name = set_name
        self.price = price
        self.priceF = priceF
        self.rarity = rarity
        self.colors = colors
        self.keywords = keywords
        self.cmc = cmc
        self.mana_cost = mana_cost
        self.legalityC = legalityC
        self.legalityS = legalityS
        self.power_toughness = power_toughness
        self.tcgplayer_id = tcgplayer_id
        self.img_url = img_url
        self.desc = desc
        self.desc2 = desc2

    def __str__(self):
        return f"{self.card_name} ({self.cmc}) - {self.card_type}"
    
    def setCardInformation(response):
        colors = []
        if 'card_faces' in response:
            try:
                colors.append(str(response['card_faces'][0]['colors'])) #collect each char and add to a new array
                colors.append("/")
                colors.append(str(response['card_faces'][1]['colors']))
            except:
                colors.append(str(response['colors']))

            mana_cost = response['card_faces'][0]['mana_cost']
            try:
                img_url = response['card_faces'][0]['image_uris']['normal']
                img_url = img_url + "/" + response['card_faces'][1]['image_uris']['normal']
            except:
                img_url = response['image_uris']['normal']
        else:
            #print(response)
            colors = response['colors']
            mana_cost = response['mana_cost']
            img_url = response['image_uris']['normal'] 

        id = response['id']
        card_name = response['name']
        card_type = response['type_line']
        set_name  = response['set_name']                                  
        keywords = response['keywords']
        
        price = response['prices']['usd']               
        priceF = response['prices']['usd_foil']      
        rarity = response['rarity']                    
        cmc = response['cmc']                         
        
        legalityS = response['legalities']['standard'] 
        legalityC = response['legalities']['commander']
        try:             
            power_toughness = response['power'] + '/' + response['toughness']
        except:
            power_toughness = "N/A"
        
        try:
            tcgplayer_id = response['tcgplayer_id']
        except KeyError:
            tcgplayer_id = "N/A"

        try:
            desc = response['oracle_text']
            desc2 = 'N/A'
        except KeyError:
            try:
                desc = response['card_faces'][0]['oracle_text']
                desc2 = response['card_faces'][0]['oracle_text']
            except KeyError:
                desc = 'N/A'
                desc2 = 'N/A'
        card = Card(id, card_name, card_type, set_name,  price, priceF, rarity, colors, keywords,
                    cmc, mana_cost, legalityC, legalityS, power_toughness, tcgplayer_id, img_url, desc, desc2)
        
        return card
    
    def getCardInfo(card):
        info = []
        info.append(card.id)
        info.append(card.card_name)
        info.append(card.card_type)
        info.append(card.set_name)
        info.append(card.price)
        info.append(card.priceF)
        info.append(card.rarity)
        info.append(card.colors)
        info.append(card.keywords)
        info.append(card.cmc)
        info.append(card.mana_cost)
        info.append(card.legalityS)
        info.append(card.legalityC)
        info.append(card.power_toughness)
        info.append(card.tcgplayer_id)
        info.append(card.img_url)
        info.append(card.desc)
        info.append(card.desc2)
        return info

    def getBestPrice(card):
        if not card.price and not card.priceF: #price and priceF are N/A
            return "N/A"
        elif not card.price and card.priceF: #only price is N/A
            return "$"+str(card.priceF)
        elif card.price and not card.priceF: #only priceF is N/A
            return "$"+str(card.price)
        else:
            if(card.price > card.priceF):
                return "$"+str(card.priceF)
            else:
                return "$"+str(card.price)
            
    
    