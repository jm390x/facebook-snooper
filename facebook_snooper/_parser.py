from lxml import html, \
                 etree
import re


def strip_ml(text):
    return re.sub(r'<[^<]+?>', '', text)


def get_profile_id(uri):
    chunk = uri.split('/')[3]
    if 'profile.php?id=' in uri:
         chunk = chunk.split('?')[1].split('=')[1]
    return chunk

def parse_followers(html_text):
    followers = ''
    matches = re.findall(r'Follower:.+?<', html_text)
    if matches:
        followers = matches[0][10:-1]
    return followers


def parse_intro(html_text):
    items = []
    ul_html = None

    matches = re.findall(r'intro_container_id.+?</ul', html_text)
    if matches:
        ul_html = matches[0][20:-4]

    if ul_html:
        tree = html.fromstring(ul_html)
        for intro in tree.xpath('//li/*[1]/div/div/div'):
            fragment = etree.tostring(intro).decode("utf-8")
            items.append(strip_ml(fragment))           
    return items


def parse_search_result(html_text):
    profiles = []

    profileURIs = re.findall(r'profileURI:".+?"', html_text)

    for profileURI in profileURIs:
        profile_uri = profileURI[12:-1]
        if not '/groups/' in profile_uri and \
           not '/events/' in profile_uri:
            profile_id = get_profile_id(profile_uri)
            profiles.append((profile_id, profile_uri))
    return profiles