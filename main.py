# -*- coding: utf-8 -*-

from icalendar import Calendar, Event, FixedOffset
from datetime import datetime
import urllib2
import re

months = {
	u'janvier' : 1,
	u'février' : 2,
	u'mars' : 3,
	u'avril' : 4,
	u'mai' : 5,
	u'juin' : 6,
	u'juillet' : 7,
	u'aout' : 8,
	u'septembre' : 9,
	u'octobre' : 10,
	u'novembre' : 11,
	u'décembre' : 12
}

titlere = re.compile(r'<h1>([^<]*)', re.U)
eventre = re.compile(r'<tr><td align=["\']right["\']>(?:\w+) (?P<day>\d+) (?P<month>[é\w]+) (?P<year>\d+)</td><td>(?P<starth>\d+):(?P<startm>\d+) - (?P<endh>\d+):(?P<endm>\d+)</td><td><b>(?P<descr>[^<]*)</b></td></tr>', re.U)

def getEvents(code):

	url = 'http://sgs.ensmp.fr/prod/sgs/ensmp/catalog/course/detail.php?type=PROGRAM&lang=FR&code=' + code
	page = unicode(urllib2.urlopen(url).read(), 'latin-1')
	title = titlere.search(page).groups()[0]
	for m in eventre.finditer(page):
		evt = Event()
		descr = m.group('descr')
		evt.add('summary', title + (' - ' + descr if descr else ''))
		evt.add('dtstart', datetime(int(m.group('year')), months[m.group('month')], int(m.group('day')), int(m.group('starth')),int(m.group('startm')), tzinfo=FixedOffset(60, 'GMT+1')))
		evt.add('dtend', datetime(int(m.group('year')), months[m.group('month')], int(m.group('day')), int(m.group('endh')),int(m.group('endm')), tzinfo=FixedOffset(60, 'GMT+1')))
		yield evt



if __name__ == '__main__':
	print 'Entrer les codes des différents cours, séparés par des espaces:'
	codes = raw_input().split()
	cal = Calendar()
	for code in codes:
		for evt in getEvents(code):
			cal.add_component(evt)

	f = open('cal.ics', 'wb')
	f.write(str(cal))
	f.close()

