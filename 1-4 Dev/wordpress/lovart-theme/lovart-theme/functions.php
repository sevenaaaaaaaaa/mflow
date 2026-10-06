<?php
/**
 * Lovart theme — block auto-registrar + real site header/footer + assets.
 */
add_action('init', function () {
    $base = get_theme_file_path('blocks');
    foreach (glob($base . '/*/block.json') ?: [] as $meta_file) {
        $type_dir = dirname($meta_file);
        $meta = json_decode((string) file_get_contents($meta_file), true);
        if (!$meta) continue;
        $render = $type_dir . '/render.php';
        $args = [];
        if (file_exists($render)) {
            $args['render_callback'] = function ($attributes, $content, $block) use ($render) {
                ob_start();
                include $render;
                return ob_get_clean();
            };
        }
        register_block_type($type_dir, $args);
    }
});

/** Styles: block theme does NOT auto-load style.css — explicit enqueue. */
add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style('lovart-base', get_theme_file_uri('style.css'), [], '0.2.0');
    wp_enqueue_style('lovart-site', get_theme_file_uri('assets/lovart-site.css'), [], '1.0.0');
    wp_enqueue_style('lovart-fonts', 'https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Noto+Serif+SC:wght@400;600&family=Inter:wght@400;500;600&family=Noto+Sans+SC:wght@400;500&family=Barlow+Condensed:wght@500;600&display=swap', [], null);
});

/** Header scroll effect: shrink on scroll (replicates lovart.ai sticky header behavior). */
add_action('wp_footer', function () {
    ?>
    <script>
    (function () {
      var last = null;
      function update() {
        var h = document.querySelector('.lovart-site-header');
        if (!h) return;
        var on = (window.scrollY || document.documentElement.scrollTop) > 24;
        if (on !== last) { h.classList.toggle('is-scrolled', on); last = on; }
      }
      window.addEventListener('scroll', update, { passive: true });
      update();
    })();
    </script>
    <?php
}, 99);

/** Replica pages: output the real lovart.ai header / footer (extracted SSR HTML). */
function lovart_site_header() {
    echo file_get_contents(get_theme_file_path('assets/site-header.html'));
}
function lovart_site_footer() {
    echo file_get_contents(get_theme_file_path('assets/site-footer.html'));
}

/** Dark mode: composite replica pages render with the site's dark token set. */
add_filter('body_class', function ($classes) {
    if (is_page('composite-replica-all')) { $classes[] = 'dark'; }
    return $classes;
});
