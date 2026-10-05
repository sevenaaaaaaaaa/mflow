<?php
/** @var array $attributes */
$badge = esc_html($attributes['badge'] ?? '');
$title = esc_html($attributes['title'] ?? '');
$hl = esc_html($attributes['highlightedText'] ?? '');
$desc = esc_html($attributes['description'] ?? '');
$buttons = $attributes['buttons'] ?? [];
?>
<section class="wp-block-lovart-hero-cinematic alignfull">
  <div class="lovart-hero__inner">
    <?php if ($badge): ?><p class="lovart-hero__badge"><?= $badge ?></p><?php endif; ?>
    <h1 class="lovart-hero__title"><?= $title ?> <?php if ($hl): ?><span class="lovart-hero__highlighted"><?= $hl ?></span><?php endif; ?></h1>
    <?php if ($desc): ?><p class="lovart-hero__description"><?= $desc ?></p><?php endif; ?>
    <div class="lovart-cta__buttons">
      <?php foreach ($buttons as $b): ?>
        <a class="lovart-cta__btn<?= !empty($b['ghost']) ? ' lovart-cta__btn--ghost' : '' ?>" href="<?= esc_url($b['url'] ?? '#') ?>"><?= esc_html($b['label'] ?? '') ?></a>
      <?php endforeach; ?>
    </div>
  </div>
</section>
