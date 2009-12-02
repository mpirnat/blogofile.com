######################################################################
# This is the main Blogofile configuration file.
# www.Blogofile.com
#
# This file has the following ordered sections:
#  * Basic Settings
#  * Intermediate Settings
#  * Advanced Settings
#
#  You really only _need_ to change the Basic Settings.
######################################################################
import sys, os
import subprocess
import shutil
import shlex
import tempfile
import subprocess

import logging
logger = logging.getLogger("blogofile.config")

from blogofile.cache import bf

######################################################################
# Basic Settings
#  (almost all sites will want to configure these settings)
######################################################################
## site_url -- Your site's full URL
# Your "site" is the same thing as your _site directory.
#  If you're hosting a blogofile powered site as a subdirectory of a larger
#  non-blogofile site, then you would set the site_url to the full URL
#  including that subdirectory: "http://www.yoursite.com/path/to/blogofile-dir"
site_url         = "http://www.blogofile.com"

#### Blog Settings ####

## blog_enabled -- Should the blog be enabled?
#  (You don't _have_ to use blogofile to build blogs)
blog_enabled = True

## blog_path -- Blog path.
#  This is the path of the blog relative to the site_url.
#  If your site_url is "http://www.yoursite.com/~ryan"
#  and you set blog_path to "/blog" your full blog URL would be
#  "http://www.yoursite.com/~ryan/blog"
#  Leave blank "" to set to the root of site_url
blog_path = "/blog"

## blog_name -- Your Blog's name.
# This is used repeatedly in default blog templates
blog_name        = "Blogofile"

## blog_description -- A short one line description of the blog
# used in the RSS/Atom feeds.
blog_description = "A static blog engine/compiler"

## blog_timezone -- the timezone that you normally write your blog posts from
blog_timezone    = "US/Eastern"

## blog_posts_per_page -- Blog posts per page
blog_posts_per_page = 5

# Automatic Permalink
# (If permalink is not defined in post article, it's generated
#  automatically based on the following format:)
# Available string replacements:
# :year, :month, :day -> post's date
# :title              -> post's title
# :uuid               -> sha hash based on title
# :filename           -> article's filename without suffix
blog_auto_permalink_enabled = True
# This is relative to site_url
blog_auto_permalink         = "/blog/:year/:month/:day/:title"

######################################################################
# Intermediate Settings
######################################################################
#### Disqus.com comment integration ####
disqus_enabled = True
disqus_name    = "blogofile"

#### Blog post syntax highlighting ####
syntax_highlight_enabled = True
# You can change the style to any builtin Pygments style
# or, make your own: http://pygments.org/docs/styles
syntax_highlight_style   = "murphy"

#### Custom blog index ####
# If you want to create your own index page at your blog root
# turn this on. Otherwise blogofile assumes you want the
# first X posts displayed instead
blog_custom_index = False

#Post excerpts
#If you want to generate excerpts of your posts in addition to the
#full post content turn this feature on
post_excerpt_enabled     = True
post_excerpt_word_length = 25
#Also, if you don't like the way the post excerpt is generated
#You can define a new function
#below called post_excerpt(content, num_words)

#### Blog pagination directory ####
# blogofile places extra pages of your blog or category in
# a secondary directory like the following:
# http://www.yourblog.com/blog_root/page/4
# http://www.yourblog.com/blog_root/category_1/page/4
# You can rename the "page" part here:
blog_pagination_dir = "page"

#### Blog category directory ####
# blogofile places extra pages of your or categories in
# a secondary directory like the following:
# http://www.yourblog.com/blog_root/category/your-topic/4
# You can rename the "category" part here:
blog_category_dir = "category"

#### Site css directory ####
# Where to write css files generated by blogofile
# (eg, Syntax highlighter writes out a pygments.css file)
# This is relative to site_url
site_css_dir = "/css"

######################################################################
# Advanced Settings
######################################################################
# These are the default ignore patterns for excluding files and dirs
# from the _site directory
# These can be strings or compiled patterns.
# Strings are assumed to be case insensitive.
file_ignore_patterns = [
    r".*([\/]|[\\])_.*",   #All files that start with an underscore
    r".*([\/]|[\\])#.*",   #Emacs temporary files
    r".*([\/]|[\\])\.#.*", #Emacs temporary files
    r".*~$]",              #Emacs temporary files
    r".*([\/]|[\\])\.git", #Git VCS dir
    r".*([\/]|[\\])\.hg",  #Mercurial VCS dir
    r".*([\/]|[\\])\.bzr", #Bazaar VCS dir
    r".*([\/]|[\\])\.svn", #Subversion VCS dir
    r".*([\/]|[\\])CVS"    #CVS dir
    ]

#### Default post filters ####
# If a post does not specify a filter chain, use the 
# following defaults based on the post file extension:
blog_post_default_filters = {
    "markdown": "markdown, syntax_highlight",
    "textile": "textile, syntax_highlight",
    "org": "org, syntax_highlight"
}

### Pre/Post build hooks:
def pre_build():
    #Do whatever you want before the _site is built
    pass
def post_build():
    #Do whatever you want after the _site is built
    build_docs()

##############################################
### Blogofile release variables
### (These are custom vars for blogofile.com)
##############################################
release_version = "0.5"
release_download_link = "http://pypi.python.org/packages/source/B/Blogofile/"\
    "Blogofile-0.5.tar.gz#md5=841b0015719502881b550ece588fc718"

    
def build_docs():
    """Build the Blogofile sphinx based documentation"""
    #Abort if sphinx isn't installed
    try:
        import sphinx
    except ImportError:
        return
    #print "Building the docs..."
    #Configure the theme
    #Insert the rendered head, headers, and footers into the theme
    config = sys.modules[globals()['__name__']]
    from mako.template import Template
    head_t = Template(open(os.path.join("_templates","head.mako")).read())
    head = head_t.render(**{'bf':bf})
    header_t = Template(open(os.path.join("_templates","header.mako")).read())
    header = header_t.render(**{'bf':bf})
    footer_t = Template(open(os.path.join("_templates","footer.mako")).read())
    footer = footer_t.render(**{'bf':bf})

    #Create the new layout.html from preparse_layout.html
    #Insert the rendered templates appropriately
    layout = open(os.path.join("_documentation","themes","blogofile",
                               "preparse_layout.html")).read()
    layout = layout.replace("blogofile_head_goes_here",head)
    layout = layout.replace("blogofile_header_goes_here",header)
    layout = layout.replace("blogofile_footer_goes_here",footer)
    layout_f = open(os.path.join("_documentation","themes","blogofile",
                               "layout.html"),"w")
    layout_f.write(layout)
    layout_f.close()
    logger.info("Compiling HTML Documentation..")
    sphinx.main(shlex.split("sphinx-build -q -b html _documentation "+
                            os.path.join("_site","documentation")))
    #Do PDF generation if TeX is installed
    if os.path.isfile("/usr/bin/tex"):
        latex_dir = tempfile.mkdtemp()
        logger.info("Compiling PDF Documentation..")
        sphinx.main(shlex.split("sphinx-build -q -b latex _documentation "+
                                latex_dir))
        subprocess.Popen(shlex.split(
                "make -C %s all-pdf" % latex_dir),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE).communicate()
        shutil.copyfile(os.path.join(latex_dir,"Blogofile.pdf"),
                        os.path.join("_site","documentation","Blogofile.pdf"))
