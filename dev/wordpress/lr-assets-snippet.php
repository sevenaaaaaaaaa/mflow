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