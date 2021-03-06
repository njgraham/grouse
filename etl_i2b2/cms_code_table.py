'''
>>> from urllib2 import build_opener
>>> web = build_opener()
>>> content = web.open(url1).read()
>>> print "'" + _claim_type(content).replace("'", "''") + "'"
... #doctest: +ELLIPSIS
'<table><item code="10" value="HHA claim" />
<item code="20" value="Non swing bed SNF claim" />
<item code="30" value="Swing bed SNF claim" />
...
<item code="82" value="RIC M DMERC DMEPOS claim" />
</table>'

'''

from xml.etree import ElementTree as ET

url1 = 'https://www.resdac.org/cms-data/variables/medpar-nch-claim-type-code'


def _claim_type(content):
    return _markup(_items(content))


def _items(content):
    _skip, content = content.split('<table ', 1)
    content, _skip = content.split('</table>', 1)
    content = '<table ' + content + '</table>'
    table = ET.fromstring(content)
    trs = table.findall('.//tr')
    rows = [[''.join(cell.itertext())
             for cell in tr.findall('.//td')]
            for tr in trs]
    items = [(code, value)
             for row in rows if row
             for (code, value) in [row]]
    return items


def _markup(items):
    table = ET.Element('table')
    for code, value in items:
        item = ET.SubElement(table, 'item',
                             code=code, value=value)
        item.tail = '\n'
    return ET.tostring(table)
