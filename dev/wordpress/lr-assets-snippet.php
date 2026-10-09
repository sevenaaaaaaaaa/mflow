/**
 * Lovart Replica — Assets（常驻）
 *
 * 复刻页/LR 模块作用域化资产的正规 enqueue 通道：
 *   - _lr_replica 整页复刻，或 _elementor_data 含 class="lr 模块（模板库插入）时加载
 *   - 历史页面零影响，反向亦然
 *   - CSS: lovart-replica.css（已作用域化到 .lr / .lr.dark，明暗由包裹类决定）
 *   - JS:  lovart-replica.js（footer + defer + data-cfasync="false"，
 *          规避 Cloudflare Rocket Loader 劫持导致的交互失效）
 *   - body class lr-replica-page + 隐藏 Elementor Pro 主题构建器站点头尾，
 *     仅限 _lr_replica 整页（插入单模块的页面保留自身主题头尾）
 *
 * _lr_replica 由迁移通道（lr-elem-bridge）写入，Elementor 编辑器保存不会清除该标记。
 * LR 模板库（lr-* 共 245 个）经 lr_elem_template 端点导入 elementor_library。
 */
add_action( 'wp_enqueue_scripts', function () {
	$pid = get_queried_object_id();
	if ( ! $pid || ! lr_replica_has_module( $pid ) ) {
		return;
	}
	wp_enqueue_style( 'lr-replica', 'https://nownexts.com/lr-assets/lovart-replica.css?v=2', array(), null );
	if ( lr_replica_has_native_module( $pid ) ) {
		wp_enqueue_style( 'lr-native', 'https://nownexts.com/lr-assets/lovart-native.css?v=1', array( 'lr-replica' ), null );
	}
	wp_enqueue_script( 'lr-replica', 'https://nownexts.com/lr-assets/lovart-replica.js?v=2', array(), null, true );
	// 隐藏主题构建器头尾仅限 _lr_replica 整页（插入单模块的页面保留自身主题头尾）
	if ( get_post_meta( $pid, '_lr_replica', true ) ) {
		wp_add_inline_style( 'lr-replica', '.lr-replica-page [data-elementor-type="header"],.lr-replica-page [data-elementor-type="footer"]{display:none !important}' );
	}
}, 20 );

/**
 * 模块级资产检测：页面/文章/LPagery 生成页只要 _elementor_data 里含有 LR 模块
 * （class="lr 包裹），就按需 enqueue 作用域资产——模板可插入任意 Elementor 文档。
 * 历史页（无 LR 内容）不受影响。
 */
function lr_replica_has_module( $pid ) {
	if ( ! $pid ) {
		return false;
	}
	if ( get_post_meta( $pid, '_lr_replica', true ) ) {
		return true;
	}
	if ( 'builder' !== (string) get_post_meta( $pid, '_elementor_edit_mode', true ) ) {
		return false;
	}
	$data = (string) get_post_meta( $pid, '_elementor_data', true );
	return false !== strpos( $data, 'class=\"lr' )
		|| false !== strpos( $data, 'class=&quot;lr' )
		|| false !== strpos( $data, 'lr-native' );
}

function lr_replica_has_native_module( $pid ) {
	if ( ! $pid || 'builder' !== (string) get_post_meta( $pid, '_elementor_edit_mode', true ) ) {
		return false;
	}
	return false !== strpos( (string) get_post_meta( $pid, '_elementor_data', true ), 'lr-native' );
}

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
	if ( ! is_singular() || ! lr_replica_has_module( get_queried_object_id() ) ) {
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