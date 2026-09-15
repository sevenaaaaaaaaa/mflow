<?php
/**
 * CPT + Taxonomy registration for Lovart Community Showcase
 *
 * CPT: showcase (slug: showcase)
 * Taxonomies: showcase_category, showcase_industry, showcase_style
 * URL Rewrite: /showcase/{category}/{slug}/
 */

if (!defined('ABSPATH')) exit;

function lovart_register_cpt_taxonomy() {

    // ---- Custom Post Type: showcase ----
    $cpt_labels = [
        'name'               => 'Showcases',
        'singular_name'      => 'Showcase',
        'add_new'            => 'Add New Showcase',
        'add_new_item'       => 'Add New Showcase',
        'edit_item'          => 'Edit Showcase',
        'view_item'          => 'View Showcase',
        'all_items'          => 'All Showcases',
        'search_items'       => 'Search Showcases',
        'not_found'          => 'No showcases found.',
        'menu_name'          => 'Showcases',
    ];

    $cpt_args = [
        'labels'             => $cpt_labels,
        'public'             => true,
        'publicly_queryable' => true,
        'show_ui'            => true,
        'show_in_menu'       => true,
        'show_in_rest'       => true,
        'query_var'          => true,
        'capability_type'    => 'post',
        'has_archive'        => true,
        'hierarchical'       => false,
        'menu_icon'          => 'dashicons-format-gallery',
        'supports'           => ['title', 'editor', 'thumbnail', 'excerpt', 'custom-fields', 'author'],
        'rewrite'            => [
            'slug'       => 'showcase/%showcase_category%',
            'with_front' => false,
            'pages'      => true,
            'feeds'      => true,
        ],
    ];

    register_post_type('showcase', $cpt_args);

    // ---- Taxonomy: showcase_category (hierarchical) ----
    $cat_labels = [
        'name'              => 'Showcase Categories',
        'singular_name'     => 'Category',
        'search_items'      => 'Search Categories',
        'all_items'         => 'All Categories',
        'parent_item'       => 'Parent Category',
        'edit_item'         => 'Edit Category',
        'update_item'       => 'Update Category',
        'add_new_item'      => 'Add New Category',
        'menu_name'         => 'Categories',
    ];

    register_taxonomy('showcase_category', 'showcase', [
        'labels'            => $cat_labels,
        'hierarchical'      => true,
        'public'            => true,
        'show_ui'           => true,
        'show_admin_column' => true,
        'show_in_rest'      => true,
        'query_var'         => true,
        'rewrite'           => [
            'slug'         => 'showcase/category',
            'with_front'   => false,
            'hierarchical' => true,
        ],
    ]);

    // ---- Taxonomy: showcase_industry (hierarchical) ----
    $ind_labels = [
        'name'              => 'Industries',
        'singular_name'     => 'Industry',
        'search_items'      => 'Search Industries',
        'all_items'         => 'All Industries',
        'menu_name'         => 'Industries',
    ];

    register_taxonomy('showcase_industry', 'showcase', [
        'labels'            => $ind_labels,
        'hierarchical'      => true,
        'public'            => true,
        'show_ui'           => true,
        'show_admin_column' => true,
        'show_in_rest'      => true,
        'query_var'         => true,
        'rewrite'           => [
            'slug'       => 'showcase/industry',
            'with_front' => false,
        ],
    ]);

    // ---- Taxonomy: showcase_style (non-hierarchical, like tags) ----
    register_taxonomy('showcase_style', 'showcase', [
        'labels'            => [
            'name'          => 'Styles',
            'singular_name' => 'Style',
            'search_items'  => 'Search Styles',
            'menu_name'     => 'Styles',
        ],
        'hierarchical'      => false,
        'public'            => true,
        'show_ui'           => true,
        'show_admin_column' => true,
        'show_in_rest'      => true,
        'query_var'         => true,
        'rewrite'           => [
            'slug'       => 'showcase/style',
            'with_front' => false,
        ],
    ]);
}
add_action('init', 'lovart_register_cpt_taxonomy');

// ---- URL Rewrite: replace %showcase_category% with actual term ----
function lovart_showcase_post_link($post_link, $post) {
    if ('showcase' !== $post->post_type) {
        return $post_link;
    }
    if (strpos($post_link, '%showcase_category%') === false) {
        return $post_link;
    }
    $terms = wp_get_object_terms($post->ID, 'showcase_category');
    if (!empty($terms) && !is_wp_error($terms)) {
        $post_link = str_replace('%showcase_category%', $terms[0]->slug, $post_link);
    } else {
        $post_link = str_replace('%showcase_category%', 'uncategorized', $post_link);
    }
    return $post_link;
}
add_filter('post_type_link', 'lovart_showcase_post_link', 10, 2);

// ---- Add showcase to blog's main query on archive pages ----
function lovart_showcase_pre_get_posts($query) {
    if (is_admin() || !$query->is_main_query()) {
        return;
    }
    if (is_post_type_archive('showcase')) {
        $query->set('posts_per_page', 24);
        $query->set('orderby', 'meta_value_num');
        $query->set('meta_key', 'view_count');
        $query->set('order', 'DESC');
    }
}
add_action('pre_get_posts', 'lovart_showcase_pre_get_posts');
