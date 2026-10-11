SITE_DEST ?= _site

.PHONY: check
check:
	ruby -c Gemfile
	bundle exec ruby -ryaml -e 'ARGV.each { |path| YAML.load_file(path) }' _config.yml _config_ci.yml .github/workflows/*.yml
	JEKYLL_ENV=production bundle exec jekyll build --safe --trace --config _config.yml,_config_ci.yml --destination "$(SITE_DEST)"
	bundle exec htmlproofer "$(SITE_DEST)" --disable-external
