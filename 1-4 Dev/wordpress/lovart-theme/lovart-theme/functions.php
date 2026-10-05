<?php
/**
 * Lovart theme — block auto-registrar.
 * Any blocks/{type}/block.json is registered automatically;
 * render callback = blocks/{type}/render.php (receives $attributes).
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

function lovart_part($name) { echo get_theme_file_path('parts/' . $name . '.php'); }
