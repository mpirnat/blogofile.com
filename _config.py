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
######################################################################
# Basic Settings
#  (almost all sites will want to configure these settings)
######################################################################
#Blog enabled. (You don't _have_ to use blogofile to build blogs)
blog_enabled = True
#Your Blog's name. This is used repeatedly in default blog templates
blog_name        = "Blogofile"
#Your Blog's full URL
blog_url         = "http://www.blogofile.com/blog"
#A short one line description of the blog, used in the RSS/Atom feeds.
blog_description = "A static blog engine/compiler"
#The timezone that you normally write your blog posts from
blog_timezone    = "US/Eastern"
#Blog posts per page
blog_posts_per_page = 5

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

######################################################################
# Advanced Settings
######################################################################
# These are the default ignore patterns for excluding files and dirs
# from the _site directory
# These can be strings or compiled patterns.
# Strings are assumed to be case insensitive.
ignore_patterns = [
    r".*[\/]_.*",   #All files that start with an underscore
    r".*[\/]#.*",   #Emacs temporary files
    r".*~$]",       #Emacs temporary files
    r".*[\/]\.git", #Git VCS dir
    r".*[\/]\.hg",  #Mercurial VCS dir
    r".*[\/]\.bzr", #Bazaar VCS dir
    r".*[\/]\.svn", #Subversion VCS dir
    r".*[\/]CVS"    #CVS dir
    ]

### Pre/Post build hooks:
def pre_build():
    #Do whatever you want before the _site is built
    pass
def post_build():
    #Do whatever you want after the _site is built
    build_docs()
    
def build_docs():
    """Build the Blogofile sphinx based documentation"""
    #Abort if sphinx isn't installed
    try:
        import sphinx
    except ImportError:
        return
    print "Building the docs..."
    #Configure the theme
    #Insert the rendered head, headers, and footers into the theme
    config = sys.modules[globals()['__name__']]
    from mako.template import Template
    head_t = Template(open(os.path.join("_templates","head.mako")).read())
    head = head_t.render(**{'config':config})
    header_t = Template(open(os.path.join("_templates","header.mako")).read())
    header = header_t.render(**{'config':config})
    footer_t = Template(open(os.path.join("_templates","footer.mako")).read())
    footer = footer_t.render(**{'config':config})

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
    
    sphinx.main(shlex.split("sphinx-build -b html _documentation "+
                            os.path.join("_site","documentation")))
    #Do PDF generation if TeX is installed
    if os.path.isfile("/usr/bin/tex"):
        latex_dir = tempfile.mkdtemp()
        sphinx.main(shlex.split("sphinx-build -b latex _documentation "+
                                latex_dir))
        subprocess.Popen(shlex.split(
                "make -C %s all-pdf" % latex_dir),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE).communicate()
        shutil.copyfile(os.path.join(latex_dir,"Blogofile.pdf"),
                        os.path.join("_site","documentation","Blogofile.pdf"))
