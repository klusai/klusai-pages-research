source "https://rubygems.org"

# Matches the GitHub Pages build environment so `bundle exec jekyll serve`
# reproduces production locally. GitHub Pages itself ignores this file and
# builds with its own pinned gem set.
# https://pages.github.com/versions/ (update this pin when Pages updates).
gem "github-pages", "= 232", group: :jekyll_plugins
gem "jekyll-remote-theme"
gem "jekyll-feed"
gem "jekyll-seo-tag"

# Ruby 3.x no longer bundles these.
gem "webrick"
gem "csv"
gem "base64"
gem "bigdecimal"

# CI checks the generated site without requesting external URLs.
gem "html-proofer", "~> 5.0", group: :test
