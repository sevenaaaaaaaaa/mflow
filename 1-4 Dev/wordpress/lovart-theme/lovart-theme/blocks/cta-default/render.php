<?php
/** @var array $attributes */
?>
<section class="wp-block-lovart-cta-default">
  <h2 class="lovart-cta__title"><?= esc_html($attributes['title'] ?? '') ?></h2>
  <p class="lovart-cta__description"><?= esc_html($attributes['description'] ?? '') ?></p>
  <div class="lovart-cta__buttons">
    <?php foreach (($attributes['buttons'] ?? []) as $b): ?>
      <a class="lovart-cta__btn" href="<?= esc_url($b['url'] ?? '#') ?>"><?= esc_html($b['label'] ?? '') ?></a>
    <?php endforeach; ?>
  </div>
</section>
