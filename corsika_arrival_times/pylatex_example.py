import numpy as np

from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, \
    Plot, Figure, Package
from pylatex.numpy import Matrix
from pylatex.utils import italic, escape_latex

doc = Document()
doc.packages.append(Package('geometry', options=['tmargin=1cm',
                                                 'lmargin=2,5cm']))

with doc.create(Section('The simple stuff')):
    doc.append('Some regular text and some ' + italic('italic text. '))
    doc.append(escape_latex('\nAlso some crazy characters: $&#{}'))
    with doc.create(Subsection('Math that is incorrect')) as math:
        doc.append(Math(data=['2*3', '=', 9]))

for k in range(5):
    with doc.create(Figure(position='h!')) as kitten_pic:
        kitten_pic.add_image('overview.png', width=r'\textwidth')
        kitten_pic.add_caption('figure number... '+str(k))

doc.generate_pdf()
