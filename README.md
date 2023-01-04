# Tweesky

Tweesky is a Python library for extracting **HTML**, **OpenGraph** and **Twitter** metadata from URLs, HTML pages and 
Spotify links.

* Check [Tweesky Web Site](https://tweesky.online/): example of what Tweesky can do
* Read [Intro on Medium](https://medium.com/@beppe.catanese/tweesky-dont-miss-the-twitter-card-preview-19c95f3417d9) 

## How to use it

Install the module: [PyPi Tweesky page](https://pypi.org/project/tweesky/)

Grab attributes from a URL
```
    import tweesky.main as tweesky
    
    website = 'https://www.nike.com/'
    card = tweesky.generate_card(url=website)
    
    print(card.title)
    print(card.image)
```

Grab attributes from an HTML document
```
    import tweesky.main as tweesky

    with open('doc.html', 'r') as reader:
        doc = reader.readlines()
    card = tweesky.generate_card(html=doc)
    
    print(card.title)
    print(card.image)
```

## Output options

There are different options to format the card:
* Card object (default): access the Python object to obtain the metadata
* JSON output: the Card content is provided as JSON
* HTML file: an HTML file is provided including the metadata necessary for creating the Social Media preview

### HTML format

When using `main.generate_card_as_html()` method the output is an HTML document which can be shared **as-is** on Social Media.

The HTML document provides all necessary OpenGraph/Twitter tags as well as the Javascript code to redirect the users to
the original page: save the file on an accessible location and distribute the link through the Social Media channels.

```
<html>
    <head>
        <meta name="twitter:card" content="summary" />
        <meta name="twitter:title" content="Python Tutorials – Real Python" />
        <meta name="twitter:description" content="Learn Python online" />
        <meta name="twitter:image" content="https://cdn.realpython.com/static/logo.png" />
        <meta name="twitter:site" content="@realpython" />
        
        <meta property="og:title" content="Python Tutorials – Real Python" />
        <meta property="og:description" content="Learn Python online" />
        <meta property="og:image" content="https://cdn.realpython.com/static/logo.png" />
        
        <meta http-equiv="refresh" content="0; url=https://realpython.com/" /> 
    </head>
    <body >
        &nbsp;
    </body>
</html>  
```


## Images

When finding the image for the Preview the library will search the following:
* Twitter Card metadata
* OpenGraph metadata
* JSON LD

