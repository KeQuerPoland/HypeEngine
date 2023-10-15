        
def add_watermark(response):
    if response.mimetype == 'text/html':
                response.set_data(response.get_data(as_text=True) + '''
    <div style="position: fixed; right: 0; bottom: 0; font-size: 30px; opacity: 0.4;filter: alpha(opacity=40); ">
        <div style="position: relative; width: 100px; height: 100px; background-color: black; border-radius: 50%;">
            <a href="https://github.com/KeQuerPoland/HypeEngine/">
                <img src="https://media.discordapp.net/attachments/1157331303256039485/1157676120263635014/HypeEngine_smaller-removebg-preview.png?ex=65197967&is=651827e7&hm=b6e01f294152a5530fe70f6409f047b8bfc85cbf5e86d18160f45e7bf1fdd6e6&=" alt="Logo" style="width: 100%; height: 100%;">
            </a>
        </div>
    </div>
    ''')
    
    return response