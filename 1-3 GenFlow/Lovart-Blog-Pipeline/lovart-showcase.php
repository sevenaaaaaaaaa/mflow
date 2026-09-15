<?php
/**
 * Plugin Name: Lovart Community Showcase
 * Description: Custom Post Type + Taxonomies for UGC community showcase. Includes [showcase_grid] shortcode, REST API endpoints for blog→showcase linking, and ACF field definitions.
 * Version: 1.0.0
 * Author: Lovart SEO Team
 */

if (!defined('ABSPATH')) exit;

define('LOVART_SHOWCASE_VERSION', '1.0.0');
define('LOVART_SHOWCASE_DIR', plugin_dir_path(__FILE__));
define('LOVART_SHOWCASE_URL', plugin_dir_url(__FILE__));

require_once LOVART_SHOWCASE_DIR . 'includes/cpt-taxonomy.php';
require_once LOVART_SHOWCASE_DIR . 'includes/shortcodes.php';
require_once LOVART_SHOWCASE_DIR . 'includes/rest-api.php';

register_activation_hook(__FILE__, 'lovart_showcase_activate');
function lovart_showcase_activate() {
    lovart_register_cpt_taxonomy();
    flush_rewrite_rules();
}

register_deactivation_hook(__FILE__, 'lovart_showcase_deactivate');
function lovart_showcase_deactivate() {
    flush_rewrite_rules();
}
