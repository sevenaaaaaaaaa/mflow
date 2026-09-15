<?php
/**
 * Shortcodes for Lovart Community Showcase
 *
 * [showcase_grid] - Display a grid of showcase items
 * [showcase_author_works] - Display works by a specific author
 * [showcase_stats] - Display aggregate stats
 */

if (!defined('ABSPATH')) exit;

// ---- [showcase_grid] - main grid shortcode ----
function lovart_showcase_grid($atts) {
    $atts = shortcode_atts([
        'category'   => '',
        'industry'   => '',
        'style'      => '',
        'author'     => '',
        'limit'      => 6,
        'columns'    => 3,
        'orderby'    => 'views',
        'show_views' => 'yes',
        'show_likes' => 'yes',
    ], $atts, 'showcase_grid');

    $args = [
        'post_type'      => 'showcase',
        'posts_per_page' => intval($atts['limit']),
        'post_status'    => 'publish',
    ];

    // Build tax query
    $tax_query = [];

    if (!empty($atts['category'])) {
        $tax_query[] = ['taxonomy' => 'showcase_category', 'field' => 'slug', 'terms' => explode(',', $atts['category'])];
    }
    if (!empty($atts['industry'])) {
        $tax_query[] = ['taxonomy' => 'showcase_industry', 'field' => 'slug', 'terms' => explode(',', $atts['industry'])];
    }
    if (!empty($atts['style'])) {
        $tax_query[] = ['taxonomy' => 'showcase_style', 'field' => 'slug', 'terms' => explode(',', $atts['style'])];
    }
    if (!empty($tax_query)) {
        $tax_query['relation'] = 'AND';
        $args['tax_query'] = $tax_query;
    }

    // Author filter
    if (!empty($atts['author'])) {
        $args['meta_query'] = [[
            'key'     => 'author_name',
            'value'   => $atts['author'],
            'compare' => 'LIKE',
        ]];
    }

    // Ordering
    if ('views' === $atts['orderby']) {
        $args['orderby']  = 'meta_value_num';
        $args['meta_key'] = 'view_count';
        $args['order']    = 'DESC';
    } elseif ('likes' === $atts['orderby']) {
        $args['orderby']  = 'meta_value_num';
        $args['meta_key'] = 'like_count';
        $args['order']    = 'DESC';
    } elseif ('newest' === $atts['orderby']) {
        $args['orderby'] = 'date';
        $args['order']   = 'DESC';
    }

    $query = new WP_Query($args);
    if (!$query->have_posts()) return '<p>No showcases found.</p>';

    $cols = intval($atts['columns']);
    $cols = max(1, min(5, $cols));
    $gap  = 20;

    ob_start();
    ?>
    <div class="lovart-showcase-grid" style="display:grid; grid-template-columns: repeat(<?php echo $cols; ?>, 1fr); gap: <?php echo $gap; ?>px; margin: 30px 0;">
        <?php while ($query->have_posts()): $query->the_post();
            $cover_url  = get_field('cover_url');
            $author     = get_field('author_name');
            $views      = get_field('view_count');
            $likes      = get_field('like_count');
            $lovart_url = get_field('lovart_url');
        ?>
        <div class="showcase-card" style="border-radius:8px; overflow:hidden; background:#fff; box-shadow:0 2px 12px rgba(0,0,0,0.08);">
            <a href="<?php the_permalink(); ?>">
                <?php if ($cover_url): ?>
                    <img src="<?php echo esc_url($cover_url); ?>" alt="<?php the_title_attribute(); ?>" style="width:100%; aspect-ratio:4/3; object-fit:cover;" loading="lazy">
                <?php else: ?>
                    <div style="width:100%; aspect-ratio:4/3; background:#f0f0f0; display:flex; align-items:center; justify-content:center; color:#aaa;">No Image</div>
                <?php endif; ?>
            </a>
            <div style="padding: 12px 14px 16px;">
                <a href="<?php the_permalink(); ?>" style="text-decoration:none; color:inherit;">
                    <h3 style="font-size:15px; font-weight:600; margin:0 0 6px; line-height:1.4;"><?php the_title(); ?></h3>
                </a>
                <?php if ($author): ?>
                    <div style="font-size:12px; color:#666; margin-bottom:4px;">by <?php echo esc_html($author); ?></div>
                <?php endif; ?>
                <?php if ('yes' === $atts['show_views'] || 'yes' === $atts['show_likes']): ?>
                <div style="font-size:11px; color:#999; display:flex; gap:12px;">
                    <?php if ('yes' === $atts['show_views']): ?><span>👁 <?php echo esc_html(lovart_format_count($views)); ?></span><?php endif; ?>
                    <?php if ('yes' === $atts['show_likes']): ?><span>❤️ <?php echo esc_html(lovart_format_count($likes)); ?></span><?php endif; ?>
                </div>
                <?php endif; ?>
            </div>
        </div>
        <?php endwhile; ?>
    </div>
    <?php
    wp_reset_postdata();
    return ob_get_clean();
}
add_shortcode('showcase_grid', 'lovart_showcase_grid');

// ---- [showcase_author_works] - author portfolio ----
function lovart_showcase_author_works($atts) {
    $atts = shortcode_atts(['author' => '', 'limit' => 8], $atts, 'showcase_author_works');
    if (empty($atts['author'])) return '';
    return lovart_showcase_grid([
        'author'  => $atts['author'],
        'limit'   => $atts['limit'],
        'columns' => 4,
        'orderby' => 'views',
    ]);
}
add_shortcode('showcase_author_works', 'lovart_showcase_author_works');

// ---- [showcase_stats] - aggregate stats ----
function lovart_showcase_stats($atts) {
    global $wpdb;
    $count       = wp_count_posts('showcase')->publish ?? 0;
    $total_views = $wpdb->get_var("SELECT SUM(meta_value) FROM {$wpdb->postmeta} WHERE meta_key = 'view_count'");
    $total_likes = $wpdb->get_var("SELECT SUM(meta_value) FROM {$wpdb->postmeta} WHERE meta_key = 'like_count'");

    ob_start();
    ?>
    <div class="showcase-stats" style="display:flex; gap:30px; flex-wrap:wrap; margin:20px 0;">
        <div style="text-align:center; padding:16px 24px; background:#f9f9f9; border-radius:8px;">
            <div style="font-size:24px; font-weight:700;"><?php echo number_format_i18n(intval($count)); ?></div>
            <div style="font-size:12px; color:#666;">Community Works</div>
        </div>
        <div style="text-align:center; padding:16px 24px; background:#f9f9f9; border-radius:8px;">
            <div style="font-size:24px; font-weight:700;"><?php echo esc_html(lovart_format_count(intval($total_views))); ?></div>
            <div style="font-size:12px; color:#666;">Total Views</div>
        </div>
        <div style="text-align:center; padding:16px 24px; background:#f9f9f9; border-radius:8px;">
            <div style="font-size:24px; font-weight:700;"><?php echo esc_html(lovart_format_count(intval($total_likes))); ?></div>
            <div style="font-size:12px; color:#666;">Total Likes</div>
        </div>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('showcase_stats', 'lovart_showcase_stats');

// ---- Utility: format large numbers ----
function lovart_format_count($num) {
    if ($num >= 1000000) return round($num / 1000000, 1) . 'M';
    if ($num >= 1000) return round($num / 1000, 1) . 'K';
    return number_format_i18n(intval($num));
}
