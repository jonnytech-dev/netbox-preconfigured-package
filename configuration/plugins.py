# Add your plugins and plugin settings here.
# Of course uncomment this file out.

# To learn how to build images with your required plugins
# See https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

PLUGINS = ["netbox_topology_views", "netbox_secrets", "netbox_floorplan"]

PLUGINS_CONFIG = {
    'netbox_secrets': {
        'apps': ['dcim.device', 'virtualization.virtualmachine'],
        'display_default': 'tab_view',
        'display_setting': {
            'dcim.device': 'full_width_page',
            'virtualization.virtualmachine': 'right_page',
        },
    },
    'netbox_topology_views': {
        'static_image_directory': 'netbox_topology_views/img',
        'allow_coordinates_saving': True,
        'always_save_coordinates': True
    },
}
