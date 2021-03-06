from django.db import models
from django.contrib.auth.models import User
from podcast.managers import EpisodeManager
from podcast import settings

class ParentCategory(models.Model):
    """Parent Category model."""
    name = models.CharField(max_length=50, choices=settings.PARENT_CHOICES, 
        help_text='''After saving this parent category, please map it to one 
                     or more Child Categories below.''')
    slug = models.SlugField(blank=True, unique=False, 
        help_text='''A <a href="http://docs.djangoproject.com/en/dev/ref/
                     models/fields/#slugfield">slug</a> is a URL-friendly 
                     nickname. For example, a slug for "Games & Hobbies" 
                     is "games-hobbies".''')

    class Meta:
        ordering = ['slug']
        verbose_name = 'category (iTunes parent)'
        verbose_name_plural = 'categories (iTunes parent)'

    def __unicode__(self):
        return u'%s' % (self.name)


class ChildCategory(models.Model):
    """Child Category model."""
    parent = models.ForeignKey(ParentCategory, 
        related_name='child_category_parents')
    name = models.CharField(max_length=50, blank=True, 
        choices=settings.CHILD_CHOICES, 
        help_text='''Please choose a child category that corresponds to its 
                     respective parent category (e.g., "Design" is a child 
                     category of "Arts").<br />If no such child category 
                     exists for a parent category (e.g., Comedy, Kids & 
                     Family, Music, News & Politics, or TV & Film), simply 
                     leave this blank and save.''')
    slug = models.SlugField(blank=True, unique=False, 
        help_text='''A <a href="http://docs.djangoproject.com/en/dev/ref/
                     models/fields/#slugfield">slug</a> is a URL-friendly 
                     nickname. For exmaple, a slug for "Fashion & Beauty" 
                     is "fashion-beauty".''')

    class Meta:
        ordering = ['parent', 'slug']
        verbose_name = 'category (iTunes child)'
        verbose_name_plural = 'categories (iTunes child)'

    def __unicode__(self):
        if self.name != '':
            return u'%s > %s' % (self.parent, self.name)
        else:
            return u'%s' % (self.parent)


class Show(models.Model):
    """Show model."""
    # RSS 2.0
    organization = models.CharField(max_length=255, 
        help_text='''Name of the organization, company or Web site producing 
                     the podcast.''')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, 
        help_text='Auto-generated from Title.')
    link = models.URLField(verify_exists=settings.VERIFY_URLS, 
        help_text='''URL of either the main website or the podcast section 
                     of the main website.''')
    description = models.TextField(
        help_text='''Describe subject matter, media 
                     format, episode schedule and other relevant information 
                     while incorporating keywords.''')
    language = models.CharField(max_length=5, default='en-us', blank=True,
        help_text='''Default is American English. See 
                     <a href="http://en.wikipedia.org/wiki/
                     List_of_ISO_639-1_codes">ISO 639-1</a> and 
                     <a href="http://en.wikipedia.org/wiki/
                     ISO_3166-1_alpha-2#Officially_assigned_code_elements">
                     ISO 3166-1</a> for more language codes.''')
    copyright = models.CharField(max_length=255, 
        default='All rights reserved', 
        choices=settings.COPYRIGHT_CHOICES, 
        help_text='''See <a href="http://creativecommons.org/about/license/">
                     Creative Commons licenses</a> for more information.''')
    copyright_url = models.URLField('Copyright URL', blank=True, 
        verify_exists=settings.VERIFY_URLS, 
        help_text='''A URL pointing to additional copyright information. 
                     Consider a <a href="http://creativecommons.org/
                     licenses/">Creative Commons license URL</a>.''')
    author = models.ManyToManyField(User, related_name='show_authors', 
        help_text='''Remember to save the user\'s name and e-mail address in 
                     the <a href="../../../auth/user/">User application</a>.
                     <br />''')
    webmaster = models.ForeignKey(User, related_name='webmaster', blank=True, 
        null=True, 
        help_text='''Remember to save the user\'s name and e-mail address in 
                     the <a href="../../../auth/user/">
                     User application</a>.''')
    category_show = models.CharField('Category', max_length=255, blank=True, 
        help_text='''Limited to one user-specified category for the sake 
                     of sanity.''')
    domain = models.URLField(blank=True, verify_exists=settings.VERIFY_URLS, 
        help_text='A URL that identifies a categorization taxonomy.')
    ttl = models.PositiveIntegerField('TTL', blank=True, null=True,
        help_text='''"Time to Live," the number of minutes a channel can 
                      be cached before refreshing.''')
    image = models.ImageField(upload_to='podcasts/shows/img/', blank=True, 
        help_text='''An attractive, original square JPEG (.jpg) or PNG (.png) 
                     image of 600x600 pixels. Image will be scaled down to 
                     50x50 pixels at smallest in iTunes.''')
    feedburner = models.URLField('FeedBurner URL', blank=True, 
        verify_exists=settings.VERIFY_URLS, 
        help_text='''Fill this out after saving this show and at least one 
                     episode. URL should look like 
                     "http://feeds.feedburner.com/TitleOfShow". 
                     See <a href="http://code.google.com/p/
                     django-podcast/">documentation</a> for more.''')
    # iTunes
    subtitle = models.CharField(max_length=255, blank=True,
        help_text='Looks best if only a few words, like a tagline.')
    summary = models.TextField(blank=True, 
        help_text='''Allows 4,000 characters. Description will be used if 
                     summary is blank.''')
    category = models.ManyToManyField(ChildCategory, blank=True,
        related_name='show_categories', 
        help_text='''If selecting a category group with no child category 
                     (e.g., Comedy, Kids & Family, Music, News & Politics or 
                     TV & Film), save that parent category with a blank 
                     <a href="../../childcategory/">child category</a>.<br />
                     Selecting multiple category groups makes the podcast 
                     more likely to be found by users.<br />''')
    explicit = models.CharField(max_length=255, default='No', blank=True,
        choices=settings.EXPLICIT_CHOICES, 
        help_text='''"Clean" will put the clean iTunes graphic by it.''')
    block = models.BooleanField(default=False, 
        help_text='''Check to block this show from iTunes. <br />Show will 
                     remain blocked until unchecked.''')
    redirect = models.URLField(blank=True, 
        verify_exists=settings.VERIFY_URLS, 
        help_text='''The show\'s new URL feed if changing the URL of the 
                     current show feed. Must continue old feed for at least 
                     two weeks and write a 301 redirect for old feed.''')
    keywords = models.CharField(max_length=255, blank=True, 
        help_text='''A comma-demlimited list of up to 12 words for iTunes 
                     searches. Perhaps include misspellings of the title.''')
    itunes = models.URLField('iTunes Store URL', blank=True, 
        verify_exists=settings.VERIFY_URLS, 
        help_text='''Fill this out after saving this show and at least one 
                     episode. URL should look like "http://phobos.apple.com/
                     WebObjects/MZStore.woa/wa/viewPodcast?id=000000000". 
                     See <a href="http://code.google.com/p/django-podcast/">
                     documentation</a> for more.''')

    class Meta:
        ordering = ['organization', 'slug']

    def __unicode__(self):
        return u'%s' % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('podcast_episodes', (), {'slug': self.slug})


class MediaCategory(models.Model):
    """Category model for Media RSS"""
    name = models.CharField(max_length=50, 
        choices=settings.MEDIA_CATEGORY_CHOICES)
    slug = models.SlugField(blank=True, unique=False, 
        help_text='''A <a href="http://docs.djangoproject.com/en/dev/ref/
                     models/fields/#slugfield">slug</a> is a URL-friendly 
                     nickname. For example, a slug for "Games & Hobbies" 
                     is "games-hobbies".''')

    class Meta:
        ordering = ['slug']
        verbose_name = 'category (Media RSS)'
        verbose_name_plural = 'categories (Media RSS)'

    def __unicode__(self):
        return u'%s' % (self.name)


class Episode(models.Model):
    """Episode model."""
    # RSS 2.0
    show = models.ForeignKey(Show)
    author = models.ManyToManyField(User, related_name='episode_authors', 
        help_text='''Remember to save the user\'s name and e-mail address in 
                     the <a href="../../../auth/user/">
                     User application</a>.''')
    title_type = models.CharField('Title type', max_length=255, blank=True, 
        default='Plain', choices=settings.TYPE_CHOICES)
    title = models.CharField(max_length=255, 
        help_text='''Make it specific but avoid explicit language. Limit to 
                     100 characters for a Google video sitemap.''')
    slug = models.SlugField(unique=True, 
        help_text='Auto-generated from Title.')
    description_type = models.CharField('Description type', max_length=255, 
        blank=True, default='Plain', choices=settings.TYPE_CHOICES)
    description = models.TextField(
        help_text='''Avoid explicit language. Google video sitempas allow 
                     2,048 characters.''')
    captions = models.FileField(upload_to='podcasts/episodes/captions/', 
        blank=True, 
        help_text='''For video podcasts. Good captioning choices include 
                    <a href="http://en.wikipedia.org/wiki/SubViewer">
                    SubViewer</a>, <a href="http://en.wikipedia.org/wiki/
                    SubRip">SubRip</a> or <a href="http://www.w3.org/TR/
                    ttaf1-dfxp/">TimedText</a>.''')
    category = models.CharField(max_length=255, blank=True, 
        help_text='''Limited to one user-specified category for the sake 
                     of sanity.''')
    domain = models.URLField(blank=True, verify_exists=settings.VERIFY_URLS, 
        help_text='A URL that identifies a categorization taxonomy.')
    frequency = models.CharField(max_length=10, default='never', 
        choices=settings.FREQUENCY_CHOICES, blank=True, 
        help_text='''The frequency with which the episode\'s 
                     data changes. For sitemaps.''')
    priority = models.DecimalField(max_digits=2, decimal_places=1, 
        blank=True, null=True, default='0.5', 
        help_text='''The relative priority of this episode compared to 
                     others. 1.0 is the most important. For sitemaps.''')
    status = models.IntegerField(choices=settings.STATUS_CHOICES, default=2)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    # iTunes
    subtitle = models.CharField(max_length=255, blank=True, 
        help_text='Looks best if only a few words like a tagline.')
    summary = models.TextField(blank=True, 
        help_text='''Allows 4,000 characters. Description will be used if 
                     summary is blank.''')
    minutes = models.PositiveIntegerField(blank=True, null=True)
    seconds = models.CharField(max_length=2, blank=True, null=True, 
        choices=settings.SECONDS_CHOICES)
    keywords = models.CharField(max_length=255, blank=True, null=True, 
        help_text='''A comma-delimited list of words for searches, up to 12; 
                     perhaps include misspellings.''')
    explicit = models.CharField(max_length=255, default='No', 
        choices=settings.EXPLICIT_CHOICES, 
        help_text='"Clean" will put the clean iTunes graphic by it.')
    block = models.BooleanField(default=False, 
        help_text='''Check to block this episode from iTunes because <br />
                     its content might cause the entire show to be <br />
                     removed from iTunes.''')
    # Media RSS
    role = models.CharField(max_length=255, blank=True, 
        choices=settings.ROLE_CHOICES, 
        help_text='''Role codes provided by the <a href="http://www.ebu.ch/
                     en/technical/metadata/specifications/role_codes.php">
                     European Broadcasting Union</a>.''')
    media_category = models.ManyToManyField(MediaCategory, 
        related_name='episode_categories', blank=True)
    standard = models.CharField(max_length=255, blank=True, 
        choices=settings.STANDARD_CHOICES, default='Simple')
    rating = models.CharField(max_length=255, blank=True, default='Nonadult', 
        choices=settings.RATING_CHOICES, 
        help_text='''If used, selection must match respective 
                     Scheme selection.''')
    image = models.ImageField(upload_to='podcasts/episodes/img/', 
        blank=True, 
        help_text='''A still image from a video file, but for episode artwork 
                     to display in iTunes, image must be <a href="http://
                     answers.yahoo.com/question/
                     index?qid=20080501164348AAjvBvQ">saved to file\'s 
                     <strong>metadata</strong></a> before episode 
                     uploading!''')
    text = models.TextField(blank=True, 
        help_text='''Media RSS text transcript. Must use <media:text> tags. 
                     Please see the <a href="https://www.google.com/
                    webmasters/tools/video/en/video.html#tagMediaText">
                    Media RSS 2.0</a> specification for syntax.''')
    deny = models.BooleanField(default=False, 
        help_text='''Check to deny episode to be shown to users from 
                     specified countries.''')
    restriction = models.CharField(max_length=255, blank=True, 
        help_text='''A space-delimited list of <a href="http://
                     en.wikipedia.org/wiki/ISO_3166-1_alpha-2#
                     Officially_assigned_code_elements">ISO 3166-1-coded 
                     countries</a>.''')
    # Dublin Core
    start = models.DateTimeField(blank=True, null=True, 
        help_text='Start date and time that the media is valid.')
    end = models.DateTimeField(blank=True, null=True, 
        help_text='End date and time that the media is valid.')
    scheme = models.CharField(max_length=255, blank=True, default='W3C-DTF')
    name = models.CharField(max_length=255, blank=True, 
        help_text='Any helper name to distinguish this time period.')
    # Google Media
    preview = models.BooleanField(default=False, 
        help_text='''Check to allow Google to show a preview of your media 
                     in search results.''')
    preview_start_mins = models.PositiveIntegerField(
        'Preview start (minutes)', blank=True, null=True, 
        help_text='''Start time (minutes) of the media\'s preview, <br />
        shown on Google.com search results before <br />clicking through 
        to see full video.''')
    preview_start_secs = models.CharField('Preview start (seconds)', 
        max_length=2, blank=True, null=True, 
        choices=settings.SECONDS_CHOICES, 
        help_text='Start time (seconds) of the media\'s preview.')
    preview_end_mins = models.PositiveIntegerField('Preview end (minutes)', 
        blank=True, null=True, 
        help_text='''End time (minutes) of the media\'s preview, <br />shown 
                     on Google.com search results before <br />clicking 
                     through to see full video.''')
    preview_end_secs = models.CharField('Preview end (seconds)', 
        max_length=2, blank=True, null=True, 
        choices=settings.SECONDS_CHOICES, 
        help_text='''End time (seconds) of the media\'s preview.''')
    host = models.BooleanField(default=False, 
        help_text='''Check to allow Google to host your media after it 
                     expires. Must set expiration date in Dublin Core.''')
    # Behind the scenes
    objects = EpisodeManager()

    class Meta:
        ordering = ['-date', 'slug']

    def __unicode__(self):
        return u'%s' % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('podcast_episode', (), 
                {'show_slug': self.show.slug, 
                 'episode_slug': self.slug})

    def seconds_total(self):
        try:
            return (((float(self.minutes)) * 60) + (float(self.seconds)))
        except:
            return 0


class Enclosure(models.Model):
    """Enclosure model."""
    title = models.CharField(max_length=255, blank=True, 
        help_text='''Title is generally only useful with multiple 
                     enclosures.''')
    file = models.FileField(upload_to='podcasts/episodes/files/', 
        blank=True, null=True, 
        help_text='''Either upload or use the "Player" text box below. 
                     If uploading, file must be less than or equal to 30 MB 
                     for a Google video sitemap.''')
    mime = models.CharField('Format', max_length=255, 
        choices=settings.MIME_CHOICES, default='video/mp4', blank=True)
    medium = models.CharField(max_length=255, blank=True, 
        choices=settings.MEDIUM_CHOICES)
    expression = models.CharField(max_length=25, blank=True, 
        choices=settings.EXPRESSION_CHOICES, default='Full')
    frame = models.CharField('Frame rate', max_length=5, blank=True, 
        help_text='Measured in frames per second (fps), often 29.97.')
    bitrate = models.CharField('Bit rate', max_length=5, blank=True, 
        help_text='Measured in kilobits per second (kbps), often 128 or 192.')
    sample = models.CharField('Sample rate', max_length=5, blank=True, 
        help_text='Measured in kilohertz (kHz), often 44.1.')
    channel = models.CharField(max_length=5, blank=True, 
        help_text='Number of channels; 2 for stereo, 1 for mono.')
    algo = models.CharField('Hash algorithm', max_length=50, blank=True, 
        choices=settings.ALGO_CHOICES)
    hash = models.CharField(max_length=255, blank=True, 
        help_text='MD-5 or SHA-1 file hash.')
    player = models.URLField(blank=True, verify_exists=settings.VERIFY_URLS, 
        help_text='''URL of the player console that plays the media. Could 
                     be your own .swf, but most likely a YouTube URL, such 
                    as <a href="http://www.youtube.com/v/UZCfK8pVztw">
                    http://www.youtube.com/v/UZCfK8pVztw</a> (not the 
                    permalink, which looks like <a href="http://
                    www.youtube.com/watch?v=UZCfK8pVztw">
                    http://www.youtube.com/watch?v=UZCfK8pVztw</a>).''')
    embed = models.BooleanField(blank=True, 
        help_text='''Check to allow Google to embed your external player in 
                     search results on <a href="http://video.google.com">
                     Google Video</a>.''')
    width = models.PositiveIntegerField(blank=True, null=True, 
        help_text='''Width of the browser window in <br />which the URL 
                     should be opened. <br />YouTube\'s default is 425.''')
    height = models.PositiveIntegerField(blank=True, null=True, 
        help_text='''Height of the browser window in <br />which the URL 
                     should be opened. <br />YouTube\'s default is 344.''')
    episode = models.ForeignKey(Episode, 
        help_text='''Include any number of media files; for example, perhaps 
                     include an iPhone-optimized, AppleTV-optimized and 
                     Flash Video set of video files. Note that the iTunes 
                     feed only accepts the first file. More uploading is 
                     available after clicking "Save and continue editing."''')

    class Meta:
        ordering = ['mime', 'file']

    def __unicode__(self):
        return u'%s' % (self.file)
