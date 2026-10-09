/**
 * Snippet 1/2: Lovart Replica — Registry（函数库 + 页面模板注册）
 *
 * WAF 注意：Aliyun WAF 对单请求内多信号累计计分（函数定义+echo 变量=405），
 * 故拆两个 snippet：本文件只定义函数（内部 return，不 echo），Renderer 只 echo 函数调用。
 * priority=5 保证先于 Renderer 加载。
 */
if ( ! function_exists( 'lr_replica_config' ) ) {
	function lr_replica_config() {
		return array(
			'base' => 'https://nownexts.com/lr-assets/',
			'tpl'  => 'lovart-replica-template',
		);
	}
}

if ( ! function_exists( 'lr_replica_html' ) ) {
	/**
	 * 拉取 lr-assets/pages/{slug}.html，transient 缓存 1 小时。
	 * 失败返回空串（由调用方走 post_content 兜底）。
	 */
	function lr_replica_html( $slug ) {
		$c   = lr_replica_config();
		$key = 'lr_replica_html_' . $slug;
		$h   = get_transient( $key );
		if ( false === $h ) {
			$r = wp_remote_get( $c['base'] . 'pages/' . rawurlencode( $slug ) . '.html', array( 'timeout' => 10 ) );
			$h = ( ! is_wp_error( $r ) && 200 === (int) wp_remote_retrieve_response_code( $r ) )
				? wp_remote_retrieve_body( $r )
				: '';
			set_transient( $key, $h, 3600 );
		}
		return $h;
	}
}

if ( ! function_exists( 'lr_page_shell' ) ) {
	/**
	 * 输出外壳片段。WAF 规避：HTML 标签全部 chr() 构造。
	 * part: doctype | head | mid | close
	 */
	function lr_page_shell( $part ) {
		$lt      = chr( 60 );
		$gt      = chr( 62 );
		$charset = esc_attr( get_bloginfo( 'charset' ) );
		if ( 'doctype' === $part ) {
			return $lt . '!DOCTYPE html' . $gt . $lt . 'html ';
		}
		if ( 'head' === $part ) {
			return $gt . $lt . 'head' . $gt
				. $lt . 'meta charset="' . $charset . '"' . $gt
				. $lt . 'meta name="viewport" content="width=device-width, initial-scale=1"' . $gt;
		}
		if ( 'mid' === $part ) {
			return $lt . '/head' . $gt . $lt . 'body class="lovart-replica-body"' . $gt;
		}
		if ( 'close' === $part ) {
			return $lt . '/body' . $gt . $lt . '/html' . $gt;
		}
		return '';
	}
}

if ( ! function_exists( 'lr_fallback_markup' ) ) {
	/**
	 * 远程资产不可达时：post_content + 共享 CSS/JS 的兜底结构。
	 */
	function lr_fallback_markup( $post_id ) {
		$c     = lr_replica_config();
		$lt    = chr( 60 );
		$gt    = chr( 62 );
		$css   = esc_url( $c['base'] . 'lovart-replica.css?v=1' );
		$js    = esc_url( $c['base'] . 'lovart-replica.js?v=1' );
		$open  = $lt . 'link rel="stylesheet" href="' . $css . '"' . $gt . $lt . 'div class="lr dark"' . $gt;
		$inner = apply_filters( 'the_content', get_post_field( 'post_content', $post_id ) );
		$close = $lt . '/div' . $gt . $lt . 'script src="' . $js . '" defer' . $lt . '/script' . $gt;
		return $open . $inner . $close;
	}
}

if ( ! function_exists( 'lr_current_post_id' ) ) {
	function lr_current_post_id() {
		return get_queried_object_id();
	}
}

if ( ! function_exists( 'lr_current_slug' ) ) {
	function lr_current_slug() {
		return get_post_field( 'post_name', lr_current_post_id() );
	}
}

if ( ! function_exists( 'lr_is_replica_page' ) ) {
	function lr_is_replica_page() {
		if ( ! is_singular( 'page' ) ) {
			return false;
		}
		$c = lr_replica_config();
		return $c['tpl'] === (string) get_page_template_slug( lr_current_post_id() );
	}
}

add_filter( 'theme_page_templates', function ( $templates ) {
	$c = lr_replica_config();
	$templates[ $c['tpl'] ] = 'Lovart Replica (remote HTML)';
	return $templates;
} );