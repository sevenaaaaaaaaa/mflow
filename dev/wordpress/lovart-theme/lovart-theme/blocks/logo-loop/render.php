<?php
/** Lovart logo-loop — 1:1 SSR replica from composite-page-all. Content edits: edit section.html. */
$lovart_section_html = file_get_contents(get_theme_file_path('blocks/logo-loop/section.html'));
echo $lovart_section_html;
