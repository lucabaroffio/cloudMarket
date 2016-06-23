# GENERATED_FILES = \
# 	world.json

# all: $(GENERATED_FILES)

# clean:
# 	rm -rf -- $(GENERATED_FILES)

# .PHONY: all clean

# build/ne_10m_%.zip:
# 	mkdir -p $(dir $@)
# 	curl -o $@ "http://www.nacis.org/naturalearth/10m/cultural/ne_10m_$*.zip"

# build/ne_%_admin_1_states_provinces.shp: build/ne_%_admin_1_states_provinces_shp.zip
# 	mkdir -p $(dir $@)
# 	unzip -od $(dir $@) $<
# 	for file in $(dir $@)/ne_$*_admin_1_states_provinces_shp.*; do mv $$file $(dir $@)/ne_$*_admin_1_states_provinces"$${file#*_shp}"; done
# 	touch $@

world.json: build10/ne_10m_admin_0_countries.shp build50/ne_50m_admin_1_states_provinces_shp.shp
	node_modules/.bin/topojson \
		--stitch-poles false \
		--properties parent_country=iso_a2,country_name=NAME,state_name=name,country_code=ISO_A2,state_code=postal, \
		-o $@ \
		-q 1e5 \
		--simplify-proportion .1 \
		-- countries=build10/ne_10m_admin_0_countries.shp \
		states=build50/ne_50m_admin_1_states_provinces_shp.shp
