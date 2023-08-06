class web():
    '''
    Class to create web page

    functions:

    WebPage:
        create
        compile
    
    Layout:
        html
        label
        href
    '''
    def __init__(self):
        '''
        Defalt param(not used for users)
        '''
        self.content = []
    
    def create(self, title='py2html site', lang='pt-br', bg='white', fg='black'):
        '''
        creat: create webpage

        parameters:
            title = page title
            lang = page language
            bg = background color
            fg = text color
        '''
        self.title = title
        self.lang = lang
        self.bg = bg
        self.fg = fg
    
    #Layout Creator
    def html(self, code):
        '''
        Insert html code

        parameters:
            code = html code
        '''
        self.content.append(code)
    def header(self, text='title', n='1'):
        '''
        Isert title

        parameters:
            text = title text
            n = title level
        '''
        self.content.append('<h'+n+'>'+text+'</h'+n+'>')
    def label(self, text='label', color='black'):
        '''
        Insert label

        parameters:
            text = label text
            color = text color
        '''
        self.content.append('<p style="color:'+color+'">'+text+'</p>')
    def href(self, text, link):
        '''

        Create href(link)

        parameters:
            text = href text
            link = href link
        '''
        self.content.append('<a href='+link+'>'+text+'</a>')
    def image(self, image, caption='THIS IS A IMAGE'):
        '''
        Insert image

        parameters:
            image = image to insert
            caption = if the image does not load show caption
        '''
        self.content.append('<img src="'+image+'" alt="'+caption+'">')

    def compile(self, name='page.html'):
        '''
        Generate html code

        parameters:
            name = html file name, ex: compile(name='index.html')
        '''
        html = open(name, 'w', encoding='UTF-8')
        html.write('<DOCTYPE html>')
        html.write('<html>')

        html.write('<head lang="'+self.lang+'">')
        html.write('<title>'+self.title+'</title>')
        html.write('<meta charset="UTF-8">')
        html.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html.write('</head>')
        html.write('<body style="background-color:'+self.bg+'; color:'+self.fg+'">')

        for c in self.content:
            html.write(c)
        
        html.write('</body>')
        html.write('</html>')
        html.close()
