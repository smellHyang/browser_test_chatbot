class KaKaoWorkBlockBuiler:
    def __init__(self):
        self.items = []
        self.headerTitle = ''
        self.headerColor = ''

    def setHeaderBlock(self, title, color = 'blue'):
        self.headerTitle = title
        self.headerColor = color

    def addTextBlock(self, text, isMarkDown = True):
        self.items.append({
            'type': 'text',
            'text': text,
            'markdown': isMarkDown  
        })

    def addDividerBlock(self):
        self.items.append({
            'type': 'divider'
        })

    def addImageLinkBlock(self, imgUrl):
        self.items.append({
            'type': 'image_link',
            'url' : imgUrl
        })

    def addSectionBlock(self, text, imgUrl, isMarkDown = True):
        self.items.append({
            'type': 'section',
            'content': {
                'type': 'text',
                'text': text,
                'markdown': isMarkDown  
            },
            'accessory': {
                'type': 'image_link',
                'url' : imgUrl
            }
        })

    def addContextBlock(self, text, imageUrl = "https://t1.kakaocdn.net/kakaowork/resources/block-kit/context/xls@3x.png", isMarkDown = True):
        self.items.append({
            'type': 'context',
            'content': {
                'type': 'text',
                'text': text,
                'markdown': isMarkDown
            },
            'image': {
                'type': 'image_link',
                'url' : imageUrl
            }
        })

    def addDescriptionBlock(self, term, text, isMarkDown = True, isAccent = True):
        self.items.append({
            'type': 'description',
            'term': term,
            'content': {
                'type': 'text',
                'text': text,
                'markdown': isMarkDown  
            },
            'accent': isAccent
        })

    def toBlock(self):
        blocks = self.items if self.headerTitle == '' else [{
            'type': 'header',
            'text': self.headerTitle,
            'style': self.headerColor
        }] + self.items
        return blocks