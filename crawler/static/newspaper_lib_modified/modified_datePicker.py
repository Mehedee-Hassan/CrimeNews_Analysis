# modified date picker for
# a very popular Bangladeshi online newspaper blog
# http://en.prothom-alo.com
# date content taken from "<span itemprop="datePublished" content="2017-04-12T20:45:00+06:00">20:46, Apr 12, 2017</span>"



from dateutil import parser
from newspaper import urls
import re


def getElementsByTag(
         node, tag=None, attr=None, value=None, childs=False):
    NS = "http://exslt.org/regular-expressions"
    # selector = tag or '*'
    selector = 'descendant-or-self::%s' % (tag or '*')
    if attr and value:
        selector = '%s[re:test(@%s, "%s", "i")]' % (selector, attr, value)
    elems = node.xpath(selector, namespaces={"re": NS})
    # remove the root node
    # if we have a selection tag
    if node in elems and (tag or childs):
        elems.remove(node)

    return elems



def     get_publishing_date( url, doc):
    """3 strategies for publishing date extraction. The strategies
    are descending in accuracy and the next strategy is only
    attempted if a preferred one fails.

    1. Pubdate from URL
    2. Pubdate from metadata
    3. Raw regex searches in the HTML + added heuristics
    """

    def parse_date_str(date_str):
        try:

            datetime_obj = parser.parse(date_str)
            return datetime_obj
        except:
            # near all parse failures are due to URL dates without a day
            # specifier, e.g. /2014/04/
            return None



    date_match = re.search(urls.DATE_REGEX, url)
    if date_match:
        date_str = date_match.group(0)
        datetime_obj = parse_date_str(date_str)
        if datetime_obj:
            return datetime_obj

    PUBLISH_DATE_TAGS = [
        {'attribute': 'itemprop', 'value': 'datePublished', 'content': 'datetime'}
    ]


    for known_meta_tag in PUBLISH_DATE_TAGS:
        meta_tags = getElementsByTag(
            node=doc,
            attr=known_meta_tag['attribute'],
            value=known_meta_tag['value'],
            tag="meta"
        )


        print(meta_tags)

        if meta_tags:
            print("metat tags", meta_tags[0].xpath("//meta[@itemprop='datePublished']/@content"))
            test_date =  meta_tags[0].xpath("//meta[@itemprop='datePublished']/@content")[0]

            datetime_obj = parse_date_str(test_date)
            if datetime_obj:
                return datetime_obj

    return None


