<?php
/** Lovart prompt-launcher — 1:1 SSR replica from composite-page-all. Content edits: edit section.html. */
$lovart_section_html = file_get_contents(get_theme_file_path('blocks/prompt-launcher/section.html'));
echo $lovart_section_html;
