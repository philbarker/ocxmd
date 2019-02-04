import markdown, unittest
from ocxmd import OCXMetadata
TESTINPUT = '''---
"@id": "#lesson1"
name: "Test Lesson 1"
"@type":
    - oer:Lesson
    - CreativeWork
learningResourceType: LessonPlan
hasPart: {
  "@id": "#activity1"
}
author:
    "@type": Person
    name: Fred Blogs
---
#YAML to JSON-LD test
I started with some YAML and turned it into JSON-LD

Here is some more YAML

---
"@id": "#activity1"
"@type":
    - oer:Activity
    - CreativeWork
name: "Test Activity 1.1"
learningResourceType: Activity
---
'''
HTMLEXPECTED = '''<script type="application/ld+json">{"@context": ["http://schema.org", {"oer": "http://oerschema.org/"}, {"ocx": "https://github.com/K12OCX/k12ocx-specs/"}], "@id": "#lesson1", "name": "Test Lesson 1", "@type": ["oer:Lesson", "CreativeWork"], "learningResourceType": "LessonPlan", "hasPart": {"@id": "#activity1"}, "author": {"@type": "Person", "name": "Fred Blogs"}}</script>

<h1>YAML to JSON-LD test</h1>
<p>I started with some YAML and turned it into JSON-LD</p>
<p>Here is some more YAML</p>
<script type="application/ld+json">{"@context": ["http://schema.org", {"oer": "http://oerschema.org/"}, {"ocx": "https://github.com/K12OCX/k12ocx-specs/"}], "@id": "#activity1", "@type": ["oer:Activity", "CreativeWork"], "name": "Test Activity 1.1", "learningResourceType": "Activity"}</script>'''

METADATAEXPECTED = {1: {'@context': ['http://schema.org', {'oer': 'http://oerschema.org/'}, {'ocx': 'https://github.com/K12OCX/k12ocx-specs/'}], '@id': '#lesson1', 'name': 'Test Lesson 1', '@type': ['oer:Lesson', 'CreativeWork'], 'learningResourceType': 'LessonPlan', 'hasPart': {'@id': '#activity1'}, 'author': {'@type': 'Person', 'name': 'Fred Blogs'}}, 2: {'@context': ['http://schema.org', {'oer': 'http://oerschema.org/'}, {'ocx': 'https://github.com/K12OCX/k12ocx-specs/'}], '@id': '#activity1', '@type': ['oer:Activity', 'CreativeWork'], 'name': 'Test Activity 1.1', 'learningResourceType': 'Activity'}}
class TestOCXMD(unittest.TestCase):
    md = markdown.Markdown(extensions = ['ocxmd'])
    html = md.convert(TESTINPUT)
    print(md.meta)
    print(html)
    def test_html(self):
        self.assertEqual(self.html, HTMLEXPECTED)
    def test_md(self):
        self.assertEqual(self.md.meta, METADATAEXPECTED)

if '__main__' == __name__:
    unittest.main()
