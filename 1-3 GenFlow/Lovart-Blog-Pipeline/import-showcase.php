<?php
/**
 * CSV Import Script for Lovart Community Showcase
 *
 * Usage:
 *   wp eval-file import/import-showcase.php
 *
 * Prerequisites:
 *   - wp-cli installed on server
 *   - lovart-showcase plugin activated
 *   - ACF Pro installed (for update_field)
 *   - OPENAI_API_KEY set in wp-config.php (optional, for LLM recommendations)
 *
 * CSV columns: url, title, description, author_name, cover_url, view_count, like_count
 */

if (!defined('ABSPATH')) {
    // Running via wp-cli eval-file
    if (!defined('WP_CLI') || !WP_CLI) {
        die("Run via: wp eval-file import/import-showcase.php\n");
    }
}

// ---- Configuration ----
$csv_path = dirname(__DIR__, 4) . '/case share code url.csv';  // Adjust path to CSV
$dry_run  = false;      // Set true to preview without creating posts
$generate_recommendations = true;  // Use OpenAI to generate editor recommendations
$skip_existing = true;  // Skip if showcase with same lovart_url already exists

// OpenAI config
$openai_api_key = defined('OPENAI_API_KEY') ? OPENAI_API_KEY : getenv('OPENAI_API_KEY');
$openai_model   = 'gpt-4o-mini';  // cheap + fast for bulk

// Category mapping: extracted keywords → taxonomy slug
$category_map = [
    'magazine cover'        => 'magazine-cover',
    'poster'                => 'poster',
    'poster set'            => 'poster-set',
    'vertical poster'       => 'poster',
    'horizontal poster'     => 'poster',
    'banner'                => 'banner',
    'flyer'                 => 'flyer',
    'logo design'           => 'logo-design',
    'brand logo'            => 'logo-design',
    'corporate logo'        => 'logo-design',
    'brand design'          => 'brand-kit',
    'brand kit'             => 'brand-kit',
    'branding'              => 'brand-kit',
    'graphic design'        => 'graphic-design',
    'character design'      => 'character-design',
    'avatar'                => 'character-design',
    'emoji'                 => 'emoji',
    'meme'                  => 'meme-comic',
    'comic'                 => 'meme-comic',
    'podcast'               => 'podcast-cover',
    'album cover'           => 'cover-art',
    'book cover'            => 'cover-art',
    'cover'                 => 'cover-art',
    'packaging'             => 'packaging',
    'product showcase'      => 'product-photography',
    'product photography'   => 'product-photography',
    'fashion design'        => 'fashion',
    'interior design'       => 'interior',
    'architectural'         => 'interior',
    'web design'            => 'web-ui',
    'ui/ux'                 => 'web-ui',
    'landing page'          => 'web-ui',
    'illustration'          => 'illustration',
    'digital illustration'  => 'illustration',
    'digital artwork'       => 'illustration',
    'photo'                 => 'photography',
    'portrait'              => 'photography',
    'card'                  => 'card',
    'sticker'               => 'sticker',
    'icon'                  => 'icon',
    'invitation'            => 'invitation',
    'video'                 => 'video',
    'animation'             => 'video',
    't-shirt'               => 'merchandise',
    'merch'                 => 'merchandise',
    'infographic'           => 'infographic',
    'menu'                  => 'menu',
];

$industry_map = [
    'publishing'            => 'publishing-media',
    'media'                 => 'publishing-media',
    'fashion'               => 'fashion-apparel',
    'apparel'               => 'fashion-apparel',
    'food'                  => 'food-beverage',
    'beverage'              => 'food-beverage',
    'restaurant'            => 'food-beverage',
    'brand design'          => 'branding',
    'brand identity'        => 'branding',
    'corporate'             => 'branding',
    'creative design'       => 'creative-design',
    'creative industry'     => 'creative-design',
    'advertising'           => 'advertising-marketing',
    'marketing'             => 'advertising-marketing',
    'social media'          => 'advertising-marketing',
    'entertainment'         => 'entertainment-media',
    'music'                 => 'entertainment-media',
    'gaming'                => 'entertainment-media',
    'travel'                => 'travel-tourism',
    'tourism'               => 'travel-tourism',
    'health'                => 'health-wellness',
    'wellness'              => 'health-wellness',
    'beauty'                => 'beauty-cosmetics',
    'cosmetics'             => 'beauty-cosmetics',
    'technology'            => 'technology',
    'education'             => 'education',
    'sports'                => 'sports',
    'architecture'          => 'architecture',
    'automotive'            => 'automotive',
    'e-commerce'            => 'ecommerce-retail',
    'retail'                => 'ecommerce-retail',
    'real estate'           => 'real-estate',
    'finance'               => 'finance',
    'nonprofit'             => 'nonprofit',
    'pet'                   => 'pet-care',
    'home decor'            => 'home-decor',
];

// ---- Helper: parse description into structured data ----
function parse_description($desc) {
    $data = [
        'author'   => '',
        'title'    => '',
        'keywords' => [],
        'industry' => '',
        'workflow' => '',
        'category' => '',
        'style'    => [],
    ];

    // Pattern: "{author} created on Lovart.ai {title}, exclusively created and shared about {keywords}, {industry}, {workflow} AI design agent workflow."
    if (preg_match('/^(.+?) created on Lovart\.ai (.+?), exclusively created and shared about (.+?), (.+?), (.+?) AI design agent workflow\./', $desc, $m)) {
        $data['author']   = trim($m[1]);
        $data['title']    = trim($m[2]);
        $data['keywords'] = array_map('trim', explode(',', $m[3]));
        $data['industry'] = trim($m[4]);
        $data['workflow'] = trim($m[5]);
    }

    // Determine category from keywords and workflow
    foreach ($data['keywords'] as $kw) {
        $lw = strtolower($kw);
        foreach ($GLOBALS['category_map'] as $key => $slug) {
            if (strpos($lw, $key) !== false || strpos($lw, $key . ' design') !== false) {
                $data['category'] = $slug;
                break 2;
            }
        }
    }
    if (empty($data['category'])) {
        // Fallback: extract from workflow
        $lw = strtolower($data['workflow']);
        foreach ($GLOBALS['category_map'] as $key => $slug) {
            if (strpos($lw, $key) !== false) {
                $data['category'] = $slug;
                break;
            }
        }
    }
    if (empty($data['category'])) {
        $data['category'] = 'graphic-design';
    }

    // Determine industry
    $lw = strtolower($data['industry']);
    foreach ($GLOBALS['industry_map'] as $key => $slug) {
        if (strpos($lw, $key) !== false) {
            $data['industry_slug'] = $slug;
            break;
        }
    }
    if (empty($data['industry_slug'])) {
        $data['industry_slug'] = 'creative-design';
    }

    // Extract style tags from keywords
    $style_keywords = ['vintage', 'retro', 'modern', 'minimalist', 'surreal', 'cyberpunk', 'futuristic',
        'pixel art', '3d', 'watercolor', 'sketch', 'collage', 'photorealistic', 'vogue', 'y2k',
        'gothic', 'anime', 'manga', 'cartoon', 'abstract', 'typography', 'minimal', 'luxury',
        'cute', 'kawaii', 'dark', 'bright', 'pastel', 'hand-drawn', 'digital', 'cinematic',
        'comic', 'pop art', 'memphis', 'bauhaus', 'brutalist', 'renaissance', 'impressionist',
    ];
    foreach ($data['keywords'] as $kw) {
        $lw = strtolower($kw);
        foreach ($style_keywords as $sk) {
            if (strpos($lw, $sk) !== false) {
                $data['style'][] = $sk;
            }
        }
    }
    $data['style'] = array_unique($data['style']);

    return $data;
}

// ---- Helper: categorize keywords into simpler style list ----
function extract_style_from_keywords($keywords) {
    $style_map = [
        'vintage'     => ['vintage', 'retro', 'old', 'classic', 'nostalgia'],
        'high-fashion'=> ['vogue', 'fashion', 'editorial', 'couture', 'glamour'],
        'futuristic'  => ['futuristic', 'cyberpunk', 'sci-fi', 'future', 'tech'],
        'surreal'     => ['surreal', 'dream', 'fantasy', 'magical'],
        'minimalist'  => ['minimalist', 'minimal', 'clean', 'simple'],
        'pixel-art'   => ['pixel art', 'pixel', '8-bit', '16-bit'],
        '3d-render'   => ['3d', 'render', 'cgi', 'blender'],
        'illustration'=> ['illustration', 'drawing', 'sketch', 'watercolor', 'hand-drawn'],
        'photoreal'   => ['photorealistic', 'realistic', 'photo-real', 'hyperrealistic'],
        'anime-manga' => ['anime', 'manga', 'chibi', 'kawaii'],
        'collage'     => ['collage', 'mixed-media'],
        'dark'        => ['dark', 'gothic', 'horror', 'noir', 'grunge'],
        'cute'        => ['cute', 'kawaii', 'adorable', 'chibi'],
        'luxury'      => ['luxury', 'premium', 'elegant', 'high-end'],
        'y2k'         => ['y2k', '2000s', 'millennium'],
    ];

    $styles = [];
    foreach ($keywords as $kw) {
        $lw = strtolower($kw);
        foreach ($style_map as $style => $triggers) {
            foreach ($triggers as $t) {
                if (strpos($lw, $t) !== false) {
                    $styles[] = $style;
                    break 2;
                }
            }
        }
    }
    return array_unique($styles);
}

// ---- Helper: generate Editor's Recommendation via OpenAI ----
function generate_recommendation($title, $author, $parsed, $workflow) {
    global $openai_api_key, $openai_model;

    if (empty($openai_api_key)) {
        return generate_recommendation_fallback($title, $author, $parsed, $workflow);
    }

    $prompt = sprintf(
        "You are the editor of the Lovart.ai community blog. Write a 2-3 sentence editorial recommendation in English for this community showcase work. Tone: witty, enthusiastic, and slightly journalistic — like a cool magazine editor curating their favorite AI-generated designs. Mention the author, the AI workflow used, the industry it serves, and what makes this design impressive. Keep it under 250 characters. Do NOT use markdown or emojis.\n\nTitle: %s\nAuthor: %s\nCategory: %s\nKeywords: %s\nIndustry: %s\nAI Workflow: %s",
        $title, $author, $parsed['category'], implode(', ', $parsed['keywords']), $parsed['industry'], $workflow
    );

    $response = wp_remote_post('https://api.openai.com/v1/chat/completions', [
        'headers' => [
            'Authorization' => 'Bearer ' . $openai_api_key,
            'Content-Type'  => 'application/json',
        ],
        'body'      => json_encode([
            'model'       => $openai_model,
            'messages'    => [['role' => 'user', 'content' => $prompt]],
            'max_tokens'  => 200,
            'temperature' => 0.8,
        ]),
        'timeout'   => 15,
    ]);

    if (is_wp_error($response)) {
        return generate_recommendation_fallback($title, $author, $parsed, $workflow);
    }

    $body = json_decode(wp_remote_retrieve_body($response), true);
    $text = $body['choices'][0]['message']['content'] ?? '';

    if (empty($text)) {
        return generate_recommendation_fallback($title, $author, $parsed, $workflow);
    }

    return trim($text);
}

// ---- Fallback: rules-based recommendation (no API key) ----
function generate_recommendation_fallback($title, $author, $parsed, $workflow) {
    $templates = [
        "%s pushed the boundaries of AI-powered design with their stunning %s. Created using Lovart's %s, this work shows what's possible when creative vision meets MCoT-powered workflows in the %s space.",
        "What happens when %s fires up Lovart's %s? This %s. A perfect example of AI-assisted creativity for the %s industry — and proof that great design is now accessible to everyone.",
        "We're loving this %s from %s. Built with the %s, it combines professional polish with creative flair — exactly the kind of work that makes the Lovart community so exciting for the %s industry.",
        "From concept to creation: %s used the %s to produce this eye-catching %s. It's a masterclass in AI-assisted design that %s professionals can learn from.",
    ];

    $template = $templates[array_rand($templates)];
    $category_label = ucwords(str_replace('-', ' ', $parsed['category']));
    $industry_label = ucwords(str_replace('-', ' ', $parsed['industry_slug']));

    return sprintf($template, $author, $category_label, $workflow, $industry_label);
}

// ---- Helper: download image and attach to post ----
function attach_image_to_post($image_url, $post_id, $title) {
    if (empty($image_url)) return false;

    // Check if already downloaded
    $existing = get_posts([
        'post_type'   => 'attachment',
        'post_parent' => $post_id,
        'numberposts' => 1,
    ]);
    if (!empty($existing)) return $existing[0]->ID;

    // Download image
    $tmp = download_url($image_url);
    if (is_wp_error($tmp)) return false;

    $file_array = [
        'name'     => sanitize_file_name($title) . '.png',
        'tmp_name' => $tmp,
    ];

    $attachment_id = media_handle_sideload($file_array, $post_id, $title);
    if (is_wp_error($attachment_id)) {
        @unlink($tmp);
        return false;
    }

    set_post_thumbnail($post_id, $attachment_id);
    return $attachment_id;
}

// ---- Helper: ensure taxonomy term exists ----
function ensure_term($name, $taxonomy, $slug = null) {
    $slug = $slug ?: sanitize_title($name);
    $term = term_exists($slug, $taxonomy);
    if (!$term) {
        $term = wp_insert_term($name, $taxonomy, ['slug' => $slug]);
    }
    return $term;
}

// ---- Main import loop ----
function import_showcases_from_csv($csv_path) {
    global $dry_run, $generate_recommendations, $skip_existing;

    if (!file_exists($csv_path)) {
        WP_CLI::error("CSV file not found: $csv_path");
        return;
    }

    $handle = fopen($csv_path, 'r');
    if (!$handle) {
        WP_CLI::error("Cannot open CSV file: $csv_path");
        return;
    }

    $headers = fgetcsv($handle); // Read header row
    WP_CLI::log("CSV headers: " . implode(', ', $headers));

    $count    = 0;
    $imported = 0;
    $skipped  = 0;
    $errors   = 0;
    $start    = microtime(true);

    while (($row = fgetcsv($handle)) !== false) {
        $count++;
        $data = array_combine($headers, $row);

        $url         = $data['url'] ?? '';
        $title       = $data['title'] ?? 'Untitled';
        $description = $data['description'] ?? '';
        $author_name = $data['author_name'] ?? '';
        $cover_url   = $data['cover_url'] ?? '';
        $view_count  = intval($data['view_count'] ?? 0);
        $like_count  = intval($data['like_count'] ?? 0);

        // Skip empty rows
        if (empty($title) || 'Untitled' === $title) {
            continue;
        }

        // Skip if already exists
        if ($skip_existing) {
            $existing = get_posts([
                'post_type'  => 'showcase',
                'meta_key'   => 'lovart_url',
                'meta_value' => $url,
                'numberposts' => 1,
            ]);
            if (!empty($existing)) {
                $skipped++;
                continue;
            }
        }

        // Parse description
        $parsed = parse_description($description);
        $styles = extract_style_from_keywords($parsed['keywords']);
        $workflow_text = $parsed['workflow'] ?: 'AI Design Agent';

        // Generate editor recommendation
        $recommendation = '';
        if ($generate_recommendations) {
            $recommendation = generate_recommendation($title, $author_name, $parsed, $workflow_text);
            // Rate-limit: sleep 100ms between API calls
            usleep(100000);
        }

        if ($dry_run) {
            WP_CLI::log(sprintf(
                "[DRY RUN] #%d: %s | Author: %s | Cat: %s | Industry: %s | Styles: %s | Views: %d",
                $count, $title, $author_name, $parsed['category'], $parsed['industry_slug'],
                implode(', ', $styles), $view_count
            ));
            $imported++;
            continue;
        }

        // Create showcase post
        $post_data = [
            'post_type'    => 'showcase',
            'post_title'   => wp_strip_all_tags($title),
            'post_content' => $description,
            'post_excerpt' => mb_substr($description, 0, 200),
            'post_status'  => 'publish',
            'post_author'  => 1,
        ];

        $post_id = wp_insert_post($post_data, true);

        if (is_wp_error($post_id)) {
            WP_CLI::warning(sprintf("Failed to create post for '%s': %s", $title, $post_id->get_error_message()));
            $errors++;
            continue;
        }

        // Set taxonomy terms
        // Category
        $cat_slug = $parsed['category'];
        $cat_name = ucwords(str_replace('-', ' ', $cat_slug));
        ensure_term($cat_name, 'showcase_category', $cat_slug);
        wp_set_object_terms($post_id, $cat_slug, 'showcase_category');

        // Industry
        ensure_term($parsed['industry'], 'showcase_industry', $parsed['industry_slug']);
        wp_set_object_terms($post_id, $parsed['industry_slug'], 'showcase_industry');

        // Styles
        if (!empty($styles)) {
            foreach ($styles as $style) {
                ensure_term($style, 'showcase_style', sanitize_title($style));
            }
            wp_set_object_terms($post_id, $styles, 'showcase_style');
        }

        // Set ACF fields
        if (function_exists('update_field')) {
            update_field('author_name', $author_name, $post_id);
            update_field('cover_url', $cover_url, $post_id);
            update_field('view_count', $view_count, $post_id);
            update_field('like_count', $like_count, $post_id);
            update_field('lovart_url', $url, $post_id);
            update_field('ai_workflow', $workflow_text, $post_id);
            if (!empty($recommendation)) {
                update_field('editor_recommendation', $recommendation, $post_id);
            }
        }

        // Download and attach featured image
        if (!empty($cover_url)) {
            attach_image_to_post($cover_url, $post_id, $title);
        }

        $imported++;

        // Progress indicator every 50 posts
        if ($imported % 50 === 0) {
            $elapsed = round(microtime(true) - $start, 1);
            WP_CLI::log(sprintf("Progress: %d imported, %d skipped, %d errors (%s elapsed)",
                $imported, $skipped, $errors, $elapsed . 's'));
        }
    }

    fclose($handle);

    $elapsed = round(microtime(true) - $start, 1);
    WP_CLI::success(sprintf(
        "Import complete! %d total rows, %d imported, %d skipped, %d errors (%s elapsed)",
        $count, $imported, $skipped, $errors, $elapsed . 's'
    ));
}

// ---- Run ----
if (defined('WP_CLI') && WP_CLI) {
    import_showcases_from_csv($csv_path);
}
