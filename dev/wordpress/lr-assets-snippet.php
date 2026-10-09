/**
 * Lovart Replica — Assets（常驻）
 *
 * 复刻页作用域化资产的正规 enqueue 通道：
 *   - 仅 _lr_replica 标记的 Elementor 页面加载（历史页面零影响，反向亦然）
 *   - CSS: lovart-replica.css（已作用域化到 .lr / .lr.dark，明暗由包裹类决定）
 *   - JS:  lovart-replica.js（footer + defer + data-cfasync="false"，
 *          规避 Cloudflare Rocket Loader 劫持导致的交互失效）
 *   - body class lr-replica-page；隐藏 Elementor Pro 主题构建器的站点页头/页脚
 *     （历史页用 elementor_canvas 不含该位置；复刻页自带 lovart.ai 站头，叠层会重复）
 *
 * _lr_replica 由迁移通道（lr-elem-bridge）写入，Elementor 编辑器保存不会清除该标记。
 */
add_action( 'wp_enqueue_scripts', function () {
	$pid = get_queried_object_id();
	if ( ! $pid || ! get_post_meta( $pid, '_lr_replica', true ) ) {
		return;
	}
	wp_enqueue_style( 'lr-replica', 'https://nownexts.com/lr-assets/lovart-replica.css?v=2', array(), null );
	wp_enqueue_script( 'lr-replica', 'https://nownexts.com/lr-assets/lovart-replica.js?v=2', array(), null, true );
	wp_add_inline_style( 'lr-replica', '.lr-replica-page [data-elementor-type="header"],.lr-replica-page [data-elementor-type="footer"]{display:none !important}' );
}, 20 );

add_filter( 'script_loader_tag', function ( $tag, $handle ) {
	if ( 'lr-replica' === $handle ) {
		$tag = str_replace( ' src=', ' defer data-cfasync="false" src=', $tag );
	}
	return $tag;
}, 10, 2 );

add_filter( 'body_class', function ( $classes ) {
	if ( is_singular() && get_post_meta( get_queried_object_id(), '_lr_replica', true ) ) {
		$classes[] = 'lr-replica-page';
	}
	return $classes;
} );

/**
 * Sticky 兜底重建：Elementor Pro 的 sticky handler 在容器懒加载时序下创建的引擎
 * 实例不生效（有 data-settings、有 .elementor-sticky 基类，但滚动永不激活）。
 * 这里在 window load 后对所有带 sticky 配置的元素销毁重建引擎（手动重建实测可激活）。
 * 仅复刻页加载；Elementor 编辑器/预览模式跳过（编辑态交给 Pro 原生 handler）。
 */
add_action( 'wp_footer', function () {
	if ( ! is_singular() || ! get_post_meta( get_queried_object_id(), '_lr_replica', true ) ) {
		return;
	}
	?>
	<script data-cfasync="false">
	/* LR sticky rebuild (replica pages only) */
	( function () {
		function run() {
			if ( ! window.jQuery || ! jQuery.fn.sticky ) { return; }
			if ( /elementor-preview|elementor-iframed/.test( location.search ) ) { return; }
			var ef = window.elementorFrontend;
			if ( ef && ef.config && ef.config.environmentMode && ef.config.environmentMode.edit ) { return; }
			var dev = ( ef && ef.getCurrentDeviceMode ) ? ef.getCurrentDeviceMode() : 'desktop';
			jQuery( '.elementor-element[data-settings*="sticky"]' ).each( function () {
				var $el = jQuery( this );
				var s = $el.data( 'settings' ) || {};
				if ( ! s.sticky || 'none' === s.sticky ) { return; }
				var on = s.sticky_on || [ 'desktop', 'tablet', 'mobile' ];
				if ( on.indexOf( dev ) === -1 ) { return; }
				var offset = parseInt( s.sticky_offset, 10 ) || 0;
				var adminBar = document.getElementById( 'wpadminbar' );
				if ( adminBar && 'fixed' === getComputedStyle( adminBar ).position ) {
					offset += adminBar.offsetHeight;
				}
				try { if ( $el.data( 'sticky' ) ) { $el.sticky( 'destroy' ); } } catch ( e ) {}
				$el.sticky( {
					to: s.sticky,
					offset: offset,
					effectsOffset: parseInt( s.sticky_effects_offset, 10 ) || 0,
					classes: {
						sticky: 'elementor-sticky',
						stickyActive: 'elementor-sticky--active elementor-section--handles-inside',
						stickyEffects: 'elementor-sticky--effects',
						spacer: 'elementor-sticky__spacer'
					},
					isRTL: ! ! ( ef && ef.config && ef.config.is_rtl )
				} );
			} );
		}
		function tryRun( left ) {
			if ( window.jQuery && jQuery.fn.sticky ) { run(); return; }
			if ( left > 0 ) { setTimeout( function () { tryRun( left - 1 ); }, 200 ); }
		}
		if ( document.readyState === 'complete' ) { tryRun( 10 ); }
		else { window.addEventListener( 'load', function () { tryRun( 10 ); } ); }
	} )();
	</script>
	<?php
}, 99 );