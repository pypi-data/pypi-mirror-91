# The So-What
*consultify* allows users to turn analyses on python into PowerPoint slides, following the conventions of standard management consulting slides.

# Installation
```
pip install consultify
```

# Usage
```
from consultify import consultify

prs = consultify.make_deck()

add_slide(prs, slide_title='Title', image_filepath='sample.jpg', slide_text=
"""Bullet 1
Bullet 2
Bullet 3""",)

add_marvin_table_slide(prs, df, slide_title = 'Title')

save_deck(prs)
```

# #plsfix
Email ryu@mba2021.hbs.edu for feedback.