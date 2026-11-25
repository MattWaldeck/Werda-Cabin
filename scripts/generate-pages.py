"""Generates the static multi-page site for Werda Cabin. Run from repo root."""
import json
import os

SITE = 'https://www.werda-cabin.co.za'
AIRBNB = 'https://www.airbnb.co.za/rooms/1176834180472791861'
LEKKE = 'https://www.lekkeslaap.co.za/accommodation/werda-cabin'

# name -> (w, h) at the 1600px size
DIMS = {}
for n, (w, h) in {
    'BathroomDoor': (1466, 2200), 'BathroomMirror': (1466, 2200), 'Bed': (1466, 2200),
    'BedLightDoor': (1466, 2200), 'BedandLight': (1466, 2200), 'BedandLightSide': (1466, 2200),
    'CabinWindow': (1650, 2200), 'Chairs': (1466, 2200), 'ChairsRoom': (1466, 2200),
    'DamMountain': (1650, 2200), 'Firewood': (1466, 2200), 'FourC': (1466, 2200),
    'HotTub': (1650, 2200), 'KantvanHuis': (2200, 1466), 'Mountain': (1650, 2200),
    'OutsideTree': (1466, 2200), 'OutsideatRock': (1466, 2200), 'RockandCabin': (1650, 2200),
    'RoomOutside': (1466, 2200), 'Sunset': (1650, 2200), 'Toilet': (1466, 2200),
    'TubMat': (1466, 2200), 'VanDam': (1466, 2200), 'ViewCabin': (1650, 2200),
    'WideCabinImage': (2200, 1650), 'Window': (1650, 2200), 'opdam': (1650, 2200),
}.items():
    s = 1600 / max(w, h)
    DIMS[n] = (round(w * s), round(h * s))


# Extra photos from the Airbnb listing (already at final size, max 1600px)
DIMS.update({
    'BedKitchenWindow': (1440, 884), 'Kitchenette': (1066, 1600), 'DeckIntoBedroom': (1067, 1600),
    'FireplaceReading': (1066, 1600), 'LoungeCorner': (1440, 884), 'CabinDusk': (1440, 1080),
    'HotTubPeak': (1067, 1600), 'CabinSunsetRoad': (1440, 1080), 'FirePitSunset': (900, 1600),
    'HotTubView': (1200, 1600), 'PathToCabin': (1066, 1600), 'FarmSunsetAerial': (1200, 1600),
    'DamBlueSky': (1440, 1080), 'DamSunsetGlow': (1440, 810), 'DamReflectionTree': (1440, 810),
    'DamSilhouette': (1440, 810), 'MountainReflection': (1440, 942),
})


def img(name, alt, sizes='(max-width: 768px) 85vw, 50vw', eager=False):
    w, h = DIMS[name]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (
        f'<img src="/img/web/{name}-sm.webp" '
        f'srcset="/img/web/{name}-sm.webp 800w, /img/web/{name}.webp 1600w" '
        f'sizes="{sizes}" alt="{alt}" width="{w}" height="{h}" {load} />'
    )


NAV = [('/', 'Home'), ('/cabin/', 'The Cabin'), ('/gallery/', 'Gallery'), ('/reviews/', 'Reviews')]


def head(title, desc, path, extra_ld=None, preload=None):
    url = SITE + path
    ld = ''
    if extra_ld:
        ld = '\n'.join(
            f'    <script type="application/ld+json">\n{json.dumps(x, indent=2, ensure_ascii=False)}\n    </script>'
            for x in extra_ld
        )
    pre = ''
    if preload:
        pre = f'\n    <link rel="preload" as="image" href="/img/web/{preload}.webp" type="image/webp" />'
    return f'''<!DOCTYPE html>
<html lang="en-ZA" class="no-js">
  <head>
    <meta charset="UTF-8" />
    <script>document.documentElement.className = "js";</script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <link rel="canonical" href="{url}" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <meta name="theme-color" content="#202b20" />
    <meta name="google-site-verification" content="JKDR54Coy91tMlyXYTbReYJ8HfcUl2QYbA73Ts2CmWM" />

    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Werda Cabin" />
    <meta property="og:locale" content="en_ZA" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{SITE}/og-image.jpg" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Werda Cabin, a black tiny home on a farm dam below the Tulbagh mountains" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="{SITE}/og-image.jpg" />

    <link rel="icon" type="image/png" href="/favicon.png" />
    <link rel="apple-touch-icon" href="/apple-touch-icon.png" />{pre}
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,500&family=Inter:wght@400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="/style/stylesheet.css" />
    <link rel="stylesheet" href="/style/responsive.css" />
    <script src="https://kit.fontawesome.com/18cbcebdd2.js" crossorigin="anonymous" defer></script>
    <script src="/scripts/script.js" type="module"></script>
{ld}
  </head>
'''


def header(active, hero_html, hero_class='hero'):
    cur = ' aria-current="page"'
    links = '\n'.join(
        f'            <a href="{href}"{cur if href == active else ""}>{label}</a>'
        for href, label in NAV
    )
    return f'''
  <body>
    <a class="skip-link" href="#main">Skip to content</a>

    <header class="{hero_class}" id="home">
      <nav class="navbar" id="navbar" aria-label="Main">
        <div class="container navbar-inner">
          <a href="/" class="logo" aria-label="Werda Cabin home">
            <img src="/img/CabinLogo.jpg" alt="" width="38" height="38" />
            <span>Werda Cabin</span>
          </a>

          <div class="navbar-option" id="navbar-option">
{links}
            <a href="#book-now-section" class="bookNow bookNow--mobile">Book Now</a>
          </div>

          <div class="navbar-actions">
            <a href="#book-now-section" class="bookNow">Book Now</a>
            <button
              type="button"
              class="hamburger"
              id="hamburger"
              aria-label="Toggle navigation menu"
              aria-expanded="false"
              aria-controls="navbar-option"
            >
              <span></span>
              <span></span>
              <span></span>
            </button>
          </div>
        </div>
      </nav>
{hero_html}
    </header>
'''


def page_hero(kicker, title, sub):
    return f'''
      <div class="hero-contents">
        <p class="hero-kicker" data-aos="fade-up">{kicker}</p>
        <h1 data-aos="fade-up" data-aos-delay="100">{title}</h1>
        <p class="hero-sub" data-aos="fade-up" data-aos-delay="200">{sub}</p>
      </div>'''


BOOK = f'''
      <section id="book-now-section" class="book-now-section">
        <div class="container">
          <p class="eyebrow">Book Now</p>
          <h2>Ready to book your stay?</h2>
          <p>
            Choose your preferred booking platform below to view the
            calendar and reserve your stay.
          </p>
          <div class="book-now-actions">
            <a href="{AIRBNB}" target="_blank" rel="noopener" class="btn btn-primary">Book on Airbnb</a>
            <a href="{LEKKE}" target="_blank" rel="noopener" class="btn btn-outline">Book on LekkeSlaap</a>
          </div>
          <p class="house-rules">
            Check-in 2:00 PM – 7:00 PM &nbsp;·&nbsp; Checkout before
            10:00 AM &nbsp;·&nbsp; 2 guests maximum
          </p>
        </div>
      </section>

      <section class="more-information-section" aria-label="Contact">
        <div class="container contact-inner">
          <div class="contact-item">
            <a href="mailto:werdacabin@gmail.com">
              <span class="fa fa-envelope-o icon" aria-hidden="true"></span>
              <span>werdacabin@gmail.com</span>
            </a>
          </div>
          <div class="contact-item">
            <span class="fa fa-map-marker icon" aria-hidden="true"></span>
            Tulbagh, Western Cape, South Africa
          </div>
        </div>
      </section>
    </main>
'''

FOOTER = f'''
    <div class="mobile-book-bar" id="mobile-book-bar">
      <div class="mobile-book-bar__info">
        <strong><span class="fa fa-star" aria-hidden="true"></span> 4.96</strong>
        <span>Guest Favorite · 2 guests</span>
      </div>
      <a href="#book-now-section" class="btn btn-primary btn-sm">Check dates</a>
    </div>

    <dialog class="lightbox" id="lightbox" aria-label="Photo viewer">
      <button type="button" class="lightbox__close" aria-label="Close photo viewer">
        <span class="fa fa-times" aria-hidden="true"></span>
      </button>
      <button type="button" class="lightbox__nav lightbox__nav--prev" aria-label="Previous photo">
        <span class="fa fa-chevron-left" aria-hidden="true"></span>
      </button>
      <figure class="lightbox__figure">
        <img class="lightbox__img" alt="" />
        <figcaption class="lightbox__caption"></figcaption>
      </figure>
      <button type="button" class="lightbox__nav lightbox__nav--next" aria-label="Next photo">
        <span class="fa fa-chevron-right" aria-hidden="true"></span>
      </button>
    </dialog>

    <footer>
      <div class="container footer-inner">
        <div class="footer-brand">
          <a href="/" class="footer-logo">Werda Cabin</a>
          <p>A cosy tiny home on a working farm in the Tulbagh Valley, Western Cape.</p>
        </div>
        <nav class="footer-nav" aria-label="Footer">
          <a href="/">Home</a>
          <a href="/cabin/">The Cabin</a>
          <a href="/gallery/">Gallery</a>
          <a href="/reviews/">Reviews</a>
        </nav>
        <div class="social-media">
          <a href="{AIRBNB}" target="_blank" rel="noopener" aria-label="Werda Cabin on Airbnb"
            ><span class="fab fa-airbnb" aria-hidden="true"></span
          ></a>
          <a href="https://www.facebook.com/people/Werda-Cabin/61561799012008/" target="_blank" rel="noopener" aria-label="Werda Cabin on Facebook"
            ><span class="fa fa-facebook" aria-hidden="true"></span
          ></a>
        </div>
      </div>
      <div class="container footer-bottom">
        <p>© 2026 Werda Cabin. All rights reserved.</p>
        <a href="https://www.linkedin.com/in/matthew-waldeck-a77884255/" target="_blank" rel="noopener" class="developer-link">Developed by Matthew</a>
      </div>
    </footer>
  </body>
</html>
'''

QUICK_FACTS = '''
      <section class="quick-facts" aria-label="Stay details">
        <div class="container quick-facts-inner">
          <div class="quick-fact"><span class="fa fa-user-o" aria-hidden="true"></span><span>2 Guests</span></div>
          <div class="quick-fact"><span class="fa fa-bed" aria-hidden="true"></span><span>1 Bedroom</span></div>
          <div class="quick-fact"><span class="fa fa-moon-o" aria-hidden="true"></span><span>1 Queen Bed</span></div>
          <div class="quick-fact"><span class="fa fa-bath" aria-hidden="true"></span><span>1 Bathroom</span></div>
          <div class="quick-fact"><span class="fa fa-key" aria-hidden="true"></span><span>Self Check-In</span></div>
        </div>
      </section>
'''

REVIEWS = [
    ('Justine', 'Stayed a few nights', "Our stay at Werda Cabin exceeded our expectations! Simoné is an amazing host and the cabin is beautiful, extremely clean and has everything you'll need. The location and views are breathtaking, it was serene and relaxing."),
    ('Caleb', 'Stayed a few nights', 'It was so relaxing and felt like home. It was nice to spend cold winter evenings in the wood fire hot tub — exactly what we needed. Simoné was so helpful and friendly. This place is truly a gem.'),
    ('Micheline', 'Cape Town, South Africa', "Felt right at home the minute we arrived, celebrated our anniversary and we loved every second of it. The most beautiful place we've ever been. Simoné's amazing!"),
    ('Noma', 'Stayed a few nights', 'The cabin was clean, cozy, and beautifully designed, with stunning mountain views. We really appreciated the generous supply of firewood, and hiking the nearby trail followed by local wine farms made it the perfect mix of relaxation and adventure.'),
    ('Zeenat', 'Cape Town, South Africa', 'We had such a wonderful stay! The cabin was clean, cozy, and beautifully maintained. Everything we needed was provided, and it truly felt like a home away from home.'),
]


def review_cards(items):
    out = []
    for i, (name, meta, text) in enumerate(items):
        delay = f' data-aos-delay="{(i % 3) * 100}"' if i % 3 else ''
        out.append(f'''            <figure class="review-card" data-aos="fade-up"{delay}>
              <span class="fa fa-quote-left" aria-hidden="true"></span>
              <blockquote><p>{text}</p></blockquote>
              <figcaption class="reviewer">
                <span class="reviewer-avatar" aria-hidden="true">{name[0]}</span>
                <span>
                  <span class="reviewer-name">{name}</span>
                  <span class="reviewer-meta">{meta}</span>
                </span>
              </figcaption>
            </figure>''')
    return '\n'.join(out)


RATINGS = '''
          <div class="rating-bars" data-aos="fade-up">
''' + '\n'.join(
    f'''            <div class="rating-bar"><span>{c}</span><div class="bar" aria-hidden="true"><span style="width: 100%"></span></div><span>5.0</span></div>'''
    for c in ['Cleanliness', 'Accuracy', 'Check-in', 'Communication', 'Location', 'Value']
) + '''
          </div>
'''


def gallery_grid(items, cls='plan-contents', card='plan-card'):
    return f'<div class="{cls}">\n' + '\n'.join(
        f'            <div class="{card}">{img(n, a)}</div>' for n, a in items
    ) + '\n          </div>'


INSIDE = [
    ('FourC', 'Open-plan cabin interior with a velvet armchair by the full-height window'),
    ('BedLightDoor', 'Queen bed with warm wall lights and the sliding barn door'),
    ('ChairsRoom', 'Reading chair, kitchenette and dam view through the corner window'),
    ('Bed', 'Queen bed with grey throw and a patterned rug on timber floors'),
    ('BedandLight', 'Comfortable queen bed with plush bedding and pendant lights'),
    ('BedandLightSide', 'Crisp white pillows under a long picture window'),
    ('RoomOutside', 'View of the farm and dam from inside the cabin'),
    ('BathroomDoor', 'Bedroom looking towards the open doors and the deck'),
    ('BathroomMirror', 'Bathroom with a round mirror and a window onto the farm'),
    ('VanDam', 'Bathroom vanity and basin with a timber wall'),
    ('Toilet', 'Clean, modern bathroom with timber cladding'),
    ('FireplaceReading', 'Reading by the wood-burning fireplace with mountain views through the window'),
    ('BedKitchenWindow', 'Queen bed, kitchenette and picture window in the open-plan cabin'),
    ('DeckIntoBedroom', 'Looking from the deck through the open doors into the bedroom'),
    ('Kitchenette', 'Kitchenette with open shelves, sink and bar fridge'),
    ('LoungeCorner', 'Armchair and kitchenette corner looking out to the farm'),
]
OUTSIDE = [
    ('WideCabinImage', 'Werda Cabin and its deck beside the farm dam'),
    ('Window', 'Black cabin with mirror-glass windows and mountains glowing at sunset'),
    ('CabinWindow', 'Cabin exterior with a stone path and the mountains behind'),
    ('OutsideTree', 'Covered deck with an outdoor dining table and boulder garden'),
    ('OutsideatRock', 'Werda Cabin among natural rock formations'),
    ('KantvanHuis', 'Side view of the cabin, deck and hot tub shelter under the peaks'),
    ('Chairs', 'Two chairs on the deck overlooking the valley'),
    ('HotTub', 'Wood-fired hot tub ready for guests'),
    ('TubMat', 'Soaking in the wood-fired hot tub with a view of the dam'),
    ('Firewood', 'Firewood stacked for the fireplace and hot tub'),
    ('CabinDusk', 'Werda Cabin lit up at dusk'),
    ('CabinSunsetRoad', 'The cabin and farm road at sunset with clouds over the mountains'),
    ('HotTubView', 'Wood-fired hot tub under its reed shelter with mountain and vineyard views'),
    ('HotTubPeak', 'Hot tub shelter beneath a towering mountain peak'),
    ('FirePitSunset', 'Fire pit glowing at sunset below the mountains'),
    ('PathToCabin', 'Stone path leading to the cabin with the mountains behind'),
]
VIEWS = [
    ('Sunset', 'Sunset over the Tulbagh mountains'),
    ('DamMountain', 'The farm dam reflecting the Tulbagh mountains'),
    ('Mountain', 'View of the mountains from the cabin deck'),
    ('opdam', 'View over the tranquil farm dam towards the cabin'),
    ('ViewCabin', 'Expansive valley view from Werda Cabin'),
    ('RockandCabin', 'Cabin nestled between boulders and farmland'),
    ('FarmSunsetAerial', 'Aerial view of the cabin and farm under a pink sunset'),
    ('MountainReflection', 'Jagged mountains mirrored in the still farm dam'),
    ('DamReflectionTree', 'Mountains and a lone tree reflected in the dam'),
    ('DamBlueSky', 'Blue sky and clouds reflected in the dam with the cabin in the distance'),
    ('DamSunsetGlow', 'Pink and orange sunset over the dam'),
    ('DamSilhouette', 'Mountain silhouette and golden sky reflected in the dam at dusk'),
]

LODGING_LD = {
    '@context': 'https://schema.org',
    '@type': 'LodgingBusiness',
    '@id': SITE + '/#lodging',
    'name': 'Werda Cabin',
    'description': 'A cosy tiny home for two on a working farm in the Tulbagh Valley, with a wood-fired hot tub, indoor fireplace, and mountain and dam views.',
    'url': SITE + '/',
    'image': [SITE + '/og-image.jpg'],
    'email': 'werdacabin@gmail.com',
    'address': {
        '@type': 'PostalAddress',
        'addressLocality': 'Tulbagh',
        'addressRegion': 'Western Cape',
        'addressCountry': 'ZA',
    },
    'checkinTime': '14:00',
    'checkoutTime': '10:00',
    'numberOfRooms': 1,
    'petsAllowed': False,
    'amenityFeature': [
        {'@type': 'LocationFeatureSpecification', 'name': n, 'value': True}
        for n in ['Wood-fired hot tub', 'Indoor fireplace', 'Fully equipped kitchen', 'Free parking', 'Self check-in', 'Mountain view', 'Waterfront']
    ],
    'aggregateRating': {'@type': 'AggregateRating', 'ratingValue': '4.96', 'bestRating': '5', 'reviewCount': '108'},
    'sameAs': [AIRBNB, LEKKE, 'https://www.facebook.com/people/Werda-Cabin/61561799012008/'],
}


def crumbs(name, path):
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': name, 'item': SITE + path},
        ],
    }


# ---------------------------------------------------------------- Home
home_hero = '''
      <div class="hero-contents">
        <p class="hero-kicker" data-aos="fade-up">Tulbagh Valley, South Africa</p>
        <h1 data-aos="fade-up" data-aos-delay="100">A cosy farm-stay hideaway</h1>
        <p class="hero-sub" data-aos="fade-up" data-aos-delay="200">
          Tiny home living beside a dam, framed by mountains — with a
          crackling fireplace and a wood-fired hot tub for two.
        </p>

        <div class="trust-badges" data-aos="fade-up" data-aos-delay="300">
          <span class="badge">
            <span class="fa fa-star" aria-hidden="true"></span>
            4.96
            <span class="badge-muted">(108 reviews)</span>
          </span>
          <span class="badge-divider" aria-hidden="true">·</span>
          <span class="badge">Guest Favorite</span>
          <span class="badge-divider" aria-hidden="true">·</span>
          <span class="badge">Superhost</span>
        </div>

        <div class="hero-actions" data-aos="fade-up" data-aos-delay="400">
          <a href="#book-now-section" class="btn btn-primary">Book your escape</a>
          <a href="/cabin/" class="btn btn-ghost">Explore the cabin</a>
        </div>
      </div>

      <a href="#main" class="scroll-down-arrow" aria-label="Scroll down">
        <span class="fa fa-chevron-down" aria-hidden="true"></span>
      </a>'''

HIGHLIGHTS = [
    ('HotTub', 'Wood-fired hot tub', 'Light the fire, sink in and watch the stars come out over the valley.'),
    ('FourC', 'Fireplace &amp; timber interior', 'A warm, considered tiny home with a queen bed and an indoor fireplace.'),
    ('DamMountain', 'Dam &amp; mountain views', 'Wake up to still water, vineyards and the mountain peaks that ring the valley.'),
]

home = head(
    'Werda Cabin | Cosy Farm-Stay Tiny Home in Tulbagh',
    'Guest Favorite tiny home for two on a working farm in Tulbagh. Wood-fired hot tub, fireplace, dam and mountain views. Rated 4.96 from 108 reviews.',
    '/',
    [LODGING_LD],
    preload='WideCabinImage',
) + header('/', home_hero) + f'''
    <main id="main">
{QUICK_FACTS}
      <section class="about-section" aria-labelledby="intro-title">
        <div class="container">
          <div class="about-contents">
            <div class="image-about" data-aos="fade-up">
              {img('Window', 'Werda Cabin at sunset with the Tulbagh mountains behind', '(max-width: 992px) 100vw, 50vw')}
            </div>
            <div class="box-about" data-aos="fade-up" data-aos-delay="100">
              <p class="eyebrow">Welcome</p>
              <h2 id="intro-title">A working farm, a tiny home, a slower pace</h2>
              <p>
                Werda Cabin sits on a working farm in the heart of the
                Tulbagh Valley, where the rhythm of nature sets the pace.
                Relax by the crackling indoor fireplace, soak in the
                wood-fired hot tub, and take in mountain and valley views
                from your own private deck.
              </p>
              <p>
                Designed as a romantic getaway for two, with a complimentary
                late Sunday checkout for weekend guests.
              </p>
              <a href="/cabin/" class="link-arrow">Discover the cabin <span aria-hidden="true">→</span></a>
            </div>
          </div>
        </div>
      </section>

      <section class="highlights" aria-labelledby="highlights-title">
        <div class="container">
          <div class="section-title" data-aos="fade-up">
            <p class="eyebrow">Why guests love it</p>
            <h2 id="highlights-title">Made for slow weekends</h2>
          </div>
          <div class="highlight-grid">
''' + '\n'.join(
    f'''            <article class="highlight-card" data-aos="fade-up"{(' data-aos-delay="%d"' % (i * 100)) if i else ''}>
              <div class="highlight-card__img">{img(n, '', '(max-width: 768px) 100vw, 33vw')}</div>
              <h3>{t}</h3>
              <p>{d}</p>
            </article>''' for i, (n, t, d) in enumerate(HIGHLIGHTS)
) + f'''
          </div>
        </div>
      </section>

      <section class="best-plans" aria-labelledby="gallery-title">
        <div class="container">
          <div class="heading-blog" data-aos="fade-up">
            <p class="eyebrow">Gallery</p>
            <h2 id="gallery-title">Inside &amp; out</h2>
            <p>Step into the cabin's warm interior and the farmland that surrounds it.</p>
          </div>
          {gallery_grid([VIEWS[6], INSIDE[11], OUTSIDE[10], INSIDE[0], VIEWS[7], OUTSIDE[12]])}
          <div class="section-cta">
            <a href="/gallery/" class="btn btn-outline">View all photos</a>
          </div>
        </div>
      </section>

      <section class="reviews-section" aria-labelledby="reviews-title">
        <div class="container">
          <div class="section-title" data-aos="fade-up">
            <p class="eyebrow">Reviews</p>
            <h2 id="reviews-title">Loved by 108 guests</h2>
            <p class="reviews-sub">
              Rated 4.96 out of 5 — a Guest Favorite in the top 1% of homes on Airbnb.
            </p>
          </div>
          <div class="review-grid review-grid--three">
{review_cards(REVIEWS[:3])}
          </div>
          <div class="section-cta">
            <a href="/reviews/" class="link-arrow">Read more reviews <span aria-hidden="true">→</span></a>
          </div>
        </div>
      </section>
{BOOK}''' + FOOTER

# ---------------------------------------------------------------- Cabin
FEATURES = [
    ('fa-tree', 'Mountain &amp; valley views'), ('fa-tint', 'Waterfront dam'),
    ('fa-swimmer', 'Private wood-fired hot tub'), ('fa-fire', 'Indoor fireplace'),
    ('fa-cutlery', 'Fully equipped kitchen'), ('fa-car', 'Free parking on-site'),
    ('fa-key', 'Self check-in'), ('fa-hiking', 'Hiking trails nearby'),
]
GOOD_TO_KNOW = [
    ('fa-clock-o', 'Check-in &amp; checkout', 'Check in between 2:00 PM and 7:00 PM, check out before 10:00 AM. Weekend guests get a complimentary late Sunday checkout.'),
    ('fa-users', 'Built for two', 'The cabin sleeps two guests in a queen bed — ideal for couples.'),
    ('fa-signal', 'Limited signal', 'Mobile reception is patchy, which makes it perfect for a digital detox.'),
    ('fa-shopping-basket', 'Self-catering', 'Bring your own food — the kitchen has everything you need to cook.'),
    ('fa-fire', 'Firewood on-site', 'Firewood for the fireplace and hot tub is available on the farm.'),
    ('fa-tint', 'Natural water', 'We rely on natural water sources, so dam levels vary with the seasons.'),
]

cabin = head(
    'The Cabin | Amenities &amp; House Info | Werda Cabin, Tulbagh',
    'Inside Werda Cabin: a tiny home for two with a queen bed, indoor fireplace, fully equipped kitchen, wood-fired hot tub and self check-in on a Tulbagh farm.',
    '/cabin/',
    [crumbs('The Cabin', '/cabin/')],
    preload='KantvanHuis',
) + header('/cabin/', page_hero(
    'The Cabin', 'A tiny home with a big view',
    "Everything you need for a slow weekend for two — and nothing you don't.",
), 'hero page-hero page-hero--cabin') + f'''
    <main id="main">
{QUICK_FACTS}
      <section class="about-section" aria-labelledby="story-title">
        <div class="container">
          <div class="about-contents">
            <div class="image-about" data-aos="fade-up">
              {img('ChairsRoom', 'Reading chair and kitchenette inside Werda Cabin with a view of the dam', '(max-width: 992px) 100vw, 50vw')}
            </div>
            <div class="box-about" data-aos="fade-up" data-aos-delay="100">
              <p class="eyebrow">Our Story</p>
              <h2 id="story-title">Life at the pace of the farm</h2>
              <p>
                Werda Cabin sits on a working farm in the heart of the
                Tulbagh Valley, where the rhythm of nature sets the pace.
                Relax by the crackling indoor fireplace, soak in the
                wood-fired hot tub, and take in mountain and valley views
                from your own private deck.
              </p>
              <h3>Built for two</h3>
              <p>
                Designed as a romantic getaway for couples, the cabin sleeps
                two in a queen bed. Weekend guests enjoy a complimentary late
                Sunday checkout, so there's no rush to leave.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="our-services" aria-labelledby="amenities-title">
        <div class="container">
          <div class="services-contents">
            <div class="box-description" data-aos="fade-up">
              <p class="eyebrow">Amenities</p>
              <h2 id="amenities-title">What the cabin offers</h2>
              <p>
                A self-catering tiny home with everything you need for a
                comfortable stay, from a cosy fireplace to a fully equipped kitchen.
              </p>
              <ul class="features-list">
''' + '\n'.join(
    f'                <li><span class="fa {i}" aria-hidden="true"></span>{t}</li>' for i, t in FEATURES
) + f'''
              </ul>
            </div>
            <div class="image-services" data-aos="fade-up">
              {gallery_grid([VIEWS[5], VIEWS[2], OUTSIDE[7], VIEWS[1], VIEWS[4], OUTSIDE[9]], 'grid-images', 'image-card')}
            </div>
          </div>
        </div>
      </section>

      <section class="good-to-know" aria-labelledby="gtk-title">
        <div class="container">
          <div class="section-title" data-aos="fade-up">
            <p class="eyebrow">Good To Know</p>
            <h2 id="gtk-title">Before you arrive</h2>
          </div>
          <div class="info-grid">
''' + '\n'.join(
    f'''            <div class="info-card" data-aos="fade-up">
              <span class="fa {i}" aria-hidden="true"></span>
              <h3>{t}</h3>
              <p>{d}</p>
            </div>''' for i, t, d in GOOD_TO_KNOW
) + '''
          </div>
        </div>
      </section>

      <section class="host-section" aria-labelledby="host-title">
        <div class="container host-inner" data-aos="fade-up">
          <div class="host-avatar" aria-hidden="true">S</div>
          <div class="host-details">
            <p class="eyebrow">Meet Your Host</p>
            <h2 id="host-title">Simoné</h2>
            <p class="host-tagline">Superhost · 2 Years Hosting</p>
            <p>
              Simoné hosts Werda Cabin on her family's working farm in
              Tulbagh, and is known for going out of her way to make every
              stay feel effortless.
            </p>
            <ul class="host-stats">
              <li><strong>100%</strong> response rate</li>
              <li>Usually responds <strong>within an hour</strong></li>
              <li>Speaks <strong>Afrikaans &amp; English</strong></li>
            </ul>
          </div>
        </div>
      </section>
''' + BOOK + FOOTER

# ---------------------------------------------------------------- Gallery
def gallery_section(sid, eyebrow, title, items, alt_bg=False):
    alt = ' gallery-section--alt' if alt_bg else ''
    return f'''
      <section class="gallery-section{alt}" id="{sid}" aria-labelledby="{sid}-title">
        <div class="container">
          <div class="gallery-section__head" data-aos="fade-up">
            <p class="eyebrow">{eyebrow}</p>
            <h2 id="{sid}-title">{title}</h2>
            <span class="gallery-count">{len(items)} photos</span>
          </div>
          {gallery_grid(items)}
        </div>
      </section>'''


total = len(INSIDE) + len(OUTSIDE) + len(VIEWS)
gallery = head(
    'Photo Gallery | Werda Cabin, Tulbagh',
    f'Browse {total} photos of Werda Cabin: the timber interior, wood-fired hot tub, private deck and the dam and mountain views of the Tulbagh Valley.',
    '/gallery/',
    [crumbs('Gallery', '/gallery/')],
    preload='FarmSunsetAerial',
) + header('/gallery/', page_hero(
    'Gallery', 'Every corner of the cabin',
    f'{total} photos of the interior, the deck and hot tub, and the valley views. Tap any photo to see it full size.',
), 'hero page-hero page-hero--gallery') + f'''
    <main id="main">
      <nav class="gallery-tabs" aria-label="Gallery sections">
        <div class="container">
          <a href="#inside">Inside</a>
          <a href="#outside">Outside</a>
          <a href="#views">The views</a>
        </div>
      </nav>
{gallery_section('inside', 'Inside', 'The interior', INSIDE)}
{gallery_section('outside', 'Outside', 'Deck, hot tub &amp; garden', OUTSIDE, True)}
{gallery_section('views', 'The Views', 'Dam, mountains &amp; sunsets', VIEWS)}
''' + BOOK + FOOTER

# ---------------------------------------------------------------- Reviews
reviews = head(
    'Guest Reviews | 4.96 Stars from 108 Guests | Werda Cabin',
    'Read what guests say about Werda Cabin in Tulbagh: rated 4.96 out of 5 from 108 reviews, a Guest Favorite in the top 1% of homes on Airbnb.',
    '/reviews/',
    [crumbs('Reviews', '/reviews/')],
    preload='Chairs',
) + header('/reviews/', page_hero(
    'Reviews', 'Loved by 108 guests',
    'Rated 4.96 out of 5 — a Guest Favorite in the top 1% of homes on Airbnb.',
), 'hero page-hero page-hero--reviews') + f'''
    <main id="main">
      <section class="reviews-section" aria-labelledby="ratings-title">
        <div class="container">
          <div class="rating-summary" data-aos="fade-up">
            <div class="rating-summary__score">
              <span class="rating-summary__num">4.96</span>
              <span class="rating-summary__stars" aria-label="5 stars">★★★★★</span>
              <span class="rating-summary__count">108 reviews</span>
            </div>
            <div>
              <h2 id="ratings-title" class="visually-hidden">Ratings by category</h2>
{RATINGS}
            </div>
          </div>

          <div class="review-grid">
{review_cards(REVIEWS)}
          </div>
          <div class="section-cta">
            <a href="{AIRBNB}#reviews" target="_blank" rel="noopener" class="btn btn-outline">Read all 108 reviews on Airbnb</a>
          </div>
        </div>
      </section>
''' + BOOK + FOOTER

os.makedirs('cabin', exist_ok=True)
os.makedirs('gallery', exist_ok=True)
os.makedirs('reviews', exist_ok=True)
for path, html in [('index.html', home), ('cabin/index.html', cabin), ('gallery/index.html', gallery), ('reviews/index.html', reviews)]:
    with open(path, 'w') as f:
        f.write(html)
    print('wrote', path, len(html))
