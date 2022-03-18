def get_html(card):
    output = (
        str(
            """
            <html>

              <head>

                <meta name="twitter:card" content="__CARD__" />
                <meta name="twitter:title" content="__TITLE__" />
                <meta name="twitter:description" content="__DESCRIPTION__" />
                <meta name="twitter:image" content="__IMAGE__" />

                <meta property="og:title" content="__TITLE__" />
                <meta property="og:description" content="__DESCRIPTION__" />
                <meta property="og:image" content="__IMAGE__" />

                __twitter:image:alt__
                __twitter:site__
                __twitter:site:id__
                __twitter:player__
                __twitter:player:stream__
                __twitter:player:width__
                __twitter:player:height__

                __twitter:app:id:iphone__
                __twitter:app:name:iphone__
                __twitter:app:url:iphone__

                __twitter:app:id:ipad__
                __twitter:app:name:ipad__
                __twitter:app:url:ipad__

                __twitter:app:id:googleplay__
                __twitter:app:name:googleplay__
                __twitter:app:url:googleplay__

                __twitter:app:country__

                __REDIRECT__

              </head>
               <body >
                    &nbsp;
              </body>
            </html>
            """
        )
    )

    output = output.replace('__CARD__', card.twitter_card)
    output = output.replace('__TITLE__', card.title)
    output = output.replace('__DESCRIPTION__', card.description)
    output = output.replace('__IMAGE__', card.image)

    output = output.replace('__twitter:site__',
                            replace_tag('twitter:site', card.twitter_site))
    output = output.replace('__twitter:site:id__',
                            replace_tag('twitter:site:id', card.twitter_site_id))

    output = output.replace('__twitter:creator__',
                            replace_tag('twitter:creator', card.twitter_creator))
    output = output.replace('__twitter:creator:id__',
                            replace_tag('twitter:creator:id', card.twitter_creator_id))

    output = output.replace('__twitter:image:alt__',
                            replace_tag('twitter:image:alt', card.twitter_image_alt))
    output = output.replace('__twitter:player__',
                            replace_tag('twitter:player', card.twitter_player))
    output = output.replace('__twitter:player:stream__',
                            replace_tag('twitter:player:stream', card.twitter_player_stream))
    output = output.replace('__twitter:player:width__',
                            replace_tag('twitter:player:width', card.twitter_player_width))
    output = output.replace('__twitter:player:height__',
                            replace_tag('twitter:player:height', card.twitter_player_height))

    output = output.replace('__twitter:app:id:iphone__',
                            replace_tag('twitter:app:id:iphone', card.twitter_app_id_iphone))
    output = output.replace('__twitter:app:name:iphone__',
                            replace_tag('twitter:app:name:iphone', card.twitter_app_name_iphone))
    output = output.replace('__twitter:app:url:iphone__',
                            replace_tag('twitter:app:url:iphone', card.twitter_app_url_iphone))

    output = output.replace('__twitter:app:id:ipad__',
                            replace_tag('twitter:app:id:ipad', card.twitter_app_id_ipad))
    output = output.replace('__twitter:app:name:ipad__',
                            replace_tag('twitter:app:name:ipad', card.twitter_app_name_ipad))
    output = output.replace('__twitter:app:url:ipad__',
                            replace_tag('twitter:app:url:ipad', card.twitter_app_url_ipad))

    output = output.replace('__twitter:app:id:googleplay__',
                            replace_tag('twitter:app:id:googleplay', card.twitter_app_id_googleplay))
    output = output.replace('__twitter:app:name:googleplay__',
                            replace_tag('twitter:app:name:googleplay', card.twitter_app_name_googleplay))
    output = output.replace('__twitter:app:url:googleplay__',
                            replace_tag('twitter:app:url:googleplay', card.twitter_app_url_googleplay))

    output = output.replace('__twitter:app:country__',
                            replace_tag('twitter:app:country', card.twitter_app_country))

    # replace with meta REFRESH
    output = output.replace('__REDIRECT__',
                            '<meta http-equiv="refresh" content="0; url=' + card.url + '" />')

    return output


def replace_tag(tag_name, tag_value):
    if tag_value is not None:
        res = f'<meta name="{tag_name}" content="{tag_value}" />'
    else:
        res = ''

    return res
