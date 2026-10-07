<?php
/** Lovart review-grid-3col — 1:1 SSR replica from composite-page-all. Content edits: edit section.html. */
$lovart_section_html = file_get_contents(get_theme_file_path('blocks/review-grid-3col/section.html'));
echo $lovart_section_html;
