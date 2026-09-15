<?php
/**
 * REST API enhancements for Lovart Community Showcase
 *
 * - GET  /wp-json/lovart/v1/showcase/related?post_id=X&type=blog|page|showcase
 * - GET  /wp-json/lovart/v1/showcase/author-tops
 * - GET  /wp-json/lovart/v1/showcase/trending
 */

if (!defined('ABSPATH')) exit;

add_action('rest_api_init', function () {

    // ---- Related content endpoint ----
    register_rest_route('lovart/v1', '/showcase/related', [
        'methods'  => 'GET',
        'callback' => 'lovart_rest_related_content',
        'args'     => [
            'post_id' => ['required' => true, 'type' => 'integer'],
            'type'    => ['default' => 'blog', 'enum' => ['blog', 'page', 'showcase']],
            'limit'   => ['default' => 6, 'type' => 'integer'],
        ],
    ]);

    // ---- Top authors endpoint ----
    register_rest_route('lovart/v1', '/showcase/author-tops', [
        'methods'  => 'GET',
        'callback' => 'lovart_rest_top_authors',
        'args'     => ['limit' => ['default' => 10, 'type' => 'integer']],
    ]);

    // ---- Trending endpoint ----
    register_rest_route('lovart/v1', '/showcase/trending', [
        'methods'  => 'GET',
        'callback' => 'lovart_rest_trending',
        'args'     => [
            'limit'    => ['default' => 12, 'type' => 'integer'],
            'category' => ['default' => '', 'type' => 'string'],
        ],
    ]);
});

function lovart_rest_related_content(WP_REST_Request $request) {
    $post_id = $request->get_param('post_id');
    $type    = $request->get_param('type');
    $limit   = $request->get_param('limit');

    $post = get_post($post_id);
    if (!$post || 'showcase' !== $post->post_type) {
        return new WP_Error('invalid_post', 'Not a showcase post', ['status' => 404]);
    }

    // Get showcase taxonomy terms
    $cat_terms      = wp_get_post_terms($post_id, 'showcase_category', ['fields' => 'slugs']);
    $industry_terms = wp_get_post_terms($post_id, 'showcase_industry', ['fields' => 'slugs']);
    $style_terms    = wp_get_post_terms($post_id, 'showcase_style', ['fields' => 'slugs']);

    if ('showcase' === $type) {
        // Related showcases: same category or same author
        $author = get_field('author_name', $post_id);
        $args = [
            'post_type'      => 'showcase',
            'posts_per_page' => $limit,
            'post__not_in'   => [$post_id],
            'meta_query'     => $author ? [['key' => 'author_name', 'value' => $author, 'compare' => '=']] : [],
        ];
        if (!empty($cat_terms)) {
            $args['tax_query'] = [['taxonomy' => 'showcase_category', 'field' => 'slug', 'terms' => $cat_terms]];
        }
    } elseif ('blog' === $type) {
        // Related blog posts: match showcase category/industry/style to blog categories/tags
        $search_terms = array_unique(array_merge($cat_terms, $industry_terms, $style_terms));
        $args = [
            'post_type'      => 'post',
            'posts_per_page' => $limit,
            'tax_query'      => [[
                'taxonomy' => 'category',
                'field'    => 'slug',
                'terms'    => $search_terms,
            ]],
        ];
    } else {
        // Related pages: match showcase industry to page keywords/title
        $args = [
            'post_type'      => 'page',
            'posts_per_page' => $limit,
            's'              => implode(' ', $industry_terms),
        ];
    }

    $query = new WP_Query($args);
    $posts = array_map(function ($p) {
        return [
            'id'        => $p->ID,
            'title'     => $p->post_title,
            'permalink' => get_permalink($p),
            'thumbnail' => get_the_post_thumbnail_url($p, 'medium'),
        ];
    }, $query->posts);

    return new WP_REST_Response($posts, 200);
}

function lovart_rest_top_authors(WP_REST_Request $request) {
    global $wpdb;
    $limit = $request->get_param('limit');

    $authors = $wpdb->get_results($wpdb->prepare("
        SELECT meta_value AS author_name, COUNT(*) AS work_count, AVG(CAST(pm2.meta_value AS UNSIGNED)) AS avg_views
        FROM {$wpdb->postmeta} pm
        JOIN {$wpdb->posts} p ON p.ID = pm.post_id AND p.post_type = 'showcase' AND p.post_status = 'publish'
        JOIN {$wpdb->postmeta} pm2 ON pm2.post_id = p.ID AND pm2.meta_key = 'view_count'
        WHERE pm.meta_key = 'author_name'
        GROUP BY pm.meta_value
        ORDER BY work_count DESC, avg_views DESC
        LIMIT %d
    ", $limit));

    return new WP_REST_Response($authors, 200);
}

function lovart_rest_trending(WP_REST_Request $request) {
    $limit    = $request->get_param('limit');
    $category = $request->get_param('category');

    $args = [
        'post_type'      => 'showcase',
        'posts_per_page' => $limit,
        'meta_key'       => 'view_count',
        'orderby'        => 'meta_value_num',
        'order'          => 'DESC',
    ];

    if ($category) {
        $args['tax_query'] = [[
            'taxonomy' => 'showcase_category',
            'field'    => 'slug',
            'terms'    => $category,
        ]];
    }

    $query = new WP_Query($args);
    $posts = array_map(function ($p) {
        return [
            'id'          => $p->ID,
            'title'       => $p->post_title,
            'permalink'   => get_permalink($p),
            'cover_url'   => get_field('cover_url', $p->ID),
            'author_name' => get_field('author_name', $p->ID),
            'view_count'  => get_field('view_count', $p->ID),
            'like_count'  => get_field('like_count', $p->ID),
        ];
    }, $query->posts);

    return new WP_REST_Response($posts, 200);
}
