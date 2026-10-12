/**
 * LR Bridge（临时迁移工具，迁移完成后删除）— Elementor 原生化迁移通道。
 *
 * 背景（WP/Elementor 渲染机制）：
 *   Elementor 前端唯一事实来源 = _elementor_data（post meta）。_elementor_edit_mode=builder
 *   时 the_content filter 渲染 Elementor 数据而非 post_content。本通道把构建好的
 *   Elementor 文档 JSON 写入页面 meta，使复刻页成为真正的 Elementor 页面。
 *
 * WAF 注意：内容不经过 REST/admin-ajax 请求体（Aliyun WAF 会拦大 payload），
 *   而是让 WP 服务器直接从 nownexts.com 服务器间拉取 JSON。
 *
 * 端点（admin-ajax，需管理员登录态）：
 *   action=lr_elem_import  page_id=<id>  url=<https://nownexts.com/lr-assets/elem/*.json>  secret=...
 *     → 写 _elementor_data/_elementor_edit_mode/_elementor_version/_lr_replica，重生成该页 CSS
 *   action=lr_elem_read   page_id=<id>  secret=...
 *     → 回读 Elementor meta 与 _elementor_data（结构对齐/诊断用）
 */
define( 'LR_BRIDGE_SECRET', 'lrb-2026-x7k9' );

add_action( 'wp_ajax_lr_elem_import', function () {
	if ( ! current_user_can( 'edit_pages' ) ) {
		wp_send_json_error( 'perm' );
	}
	if ( ! isset( $_POST['secret'] ) || LR_BRIDGE_SECRET !== $_POST['secret'] ) {
		wp_send_json_error( 'secret' );
	}
	$pid = isset( $_POST['page_id'] ) ? absint( $_POST['page_id'] ) : 0;
	$url = isset( $_POST['url'] ) ? esc_url_raw( wp_unslash( $_POST['url'] ) ) : '';
	if ( ! $pid || 0 !== strpos( $url, 'https://nownexts.com/lr-assets/' ) ) {
		wp_send_json_error( 'args' );
	}
	$nomark = ! empty( $_POST['nomark'] );
	$r = wp_remote_get( $url, array( 'timeout' => 90 ) );
	if ( is_wp_error( $r ) || 200 !== (int) wp_remote_retrieve_response_code( $r ) ) {
		wp_send_json_error( 'fetch:' . wp_remote_retrieve_response_code( $r ) );
	}
	$payload = json_decode( wp_remote_retrieve_body( $r ), true );
	if ( empty( $payload['data'] ) || ! is_array( $payload['data'] ) ) {
		wp_send_json_error( 'payload' );
	}

	update_post_meta( $pid, '_elementor_edit_mode', 'builder' );
	update_post_meta( $pid, '_elementor_template_type', 'wp-page' );
	update_post_meta( $pid, '_elementor_version', isset( $payload['version'] ) ? $payload['version'] : '3.35.7' );
	update_post_meta( $pid, '_elementor_data', wp_slash( wp_json_encode( $payload['data'] ) ) );
	if ( $nomark ) {
		delete_post_meta( $pid, '_lr_replica' );
	} else {
		update_post_meta( $pid, '_lr_replica', 1 );
	}
	delete_post_meta( $pid, '_elementor_css' );
	delete_post_meta( $pid, '_elementor_element_cache' );

	// 重生成该页的 Elementor CSS 文件（post-{id}.css + meta 版本号）
	if ( class_exists( '\Elementor\Core\Files\CSS\Post' ) ) {
		$css_file = new \Elementor\Core\Files\CSS\Post( $pid );
		$css_file->update();
	}
	wp_send_json_success( array( 'page' => $pid, 'elements' => count( $payload['data'] ) ) );
} );

/**
 * action=lr_lpagery_nonce  secret=...
 *   → 返回 lpagery_ajax nonce（LPagery 批量建页产线的程序化入口；
 *     dashboard 页面 HTML 里没有该 nonce，只能服务端生成）。
 */
add_action( 'wp_ajax_lr_lpagery_nonce', function () {
	if ( ! current_user_can( 'edit_pages' ) ) {
		wp_send_json_error( 'perm' );
	}
	if ( ! isset( $_POST['secret'] ) || LR_BRIDGE_SECRET !== $_POST['secret'] ) {
		wp_send_json_error( 'secret' );
	}
	wp_send_json_success( array( 'nonce' => wp_create_nonce( 'lpagery_ajax' ) ) );
} );

add_action( 'wp_ajax_lr_elem_read', function () {
	if ( ! current_user_can( 'edit_pages' ) ) {
		wp_send_json_error( 'perm' );
	}
	if ( ! isset( $_POST['secret'] ) || LR_BRIDGE_SECRET !== $_POST['secret'] ) {
		wp_send_json_error( 'secret' );
	}
	$pid = isset( $_POST['page_id'] ) ? absint( $_POST['page_id'] ) : 0;
	if ( ! $pid ) {
		wp_send_json_error( 'args' );
	}
	$data = json_decode( (string) get_post_meta( $pid, '_elementor_data', true ) );
	wp_send_json_success( array(
		'edit_mode'     => get_post_meta( $pid, '_elementor_edit_mode', true ),
		'template_type' => get_post_meta( $pid, '_elementor_template_type', true ),
		'version'       => get_post_meta( $pid, '_elementor_version', true ),
		'css'           => get_post_meta( $pid, '_elementor_css', true ),
		'lr_replica'    => get_post_meta( $pid, '_lr_replica', true ),
		'data'          => $data,
		'seo'           => array(
			'rank_math_title'       => get_post_meta( $pid, 'rank_math_title', true ),
			'rank_math_description' => get_post_meta( $pid, 'rank_math_description', true ),
			'rank_math_canonical'   => get_post_meta( $pid, 'rank_math_canonical', true ),
		),
	) );
} );

/**
 * action=lr_batch_page  url=<https://nownexts.com/lr-assets/batch/<slug>.json>  secret=...
 *   → 批量建页通道（LPagery free 版占位符上限 3 列，126 列契约走不了，自建）。
 *     payload JSON：{"slug":..., "title":..., "status":"draft|publish",
 *                    "elementor":{"version":"...","data":[...]}}
 *     按 slug 查重：有则更新（标题/内容/meta），无则新建。写 _lr_replica，重生成 CSS。
 */
add_action( 'wp_ajax_lr_batch_page', function () {
	if ( ! current_user_can( 'edit_pages' ) ) {
		wp_send_json_error( 'perm' );
	}
	if ( ! isset( $_POST['secret'] ) || LR_BRIDGE_SECRET !== $_POST['secret'] ) {
		wp_send_json_error( 'secret' );
	}
	$url = isset( $_POST['url'] ) ? esc_url_raw( wp_unslash( $_POST['url'] ) ) : '';
	if ( 0 !== strpos( $url, 'https://nownexts.com/lr-assets/' ) ) {
		wp_send_json_error( 'args' );
	}
	$r = wp_remote_get( $url, array( 'timeout' => 90 ) );
	if ( is_wp_error( $r ) || 200 !== (int) wp_remote_retrieve_response_code( $r ) ) {
		wp_send_json_error( 'fetch:' . wp_remote_retrieve_response_code( $r ) );
	}
	$payload = json_decode( wp_remote_retrieve_body( $r ), true );
	if ( empty( $payload['slug'] ) || empty( $payload['title'] )
		|| empty( $payload['elementor']['data'] ) || ! is_array( $payload['elementor']['data'] ) ) {
		wp_send_json_error( 'payload' );
	}
	$slug = sanitize_title( $payload['slug'] );
	$status = ( isset( $payload['status'] ) && 'publish' === $payload['status'] ) ? 'publish' : 'draft';

	$existing = get_posts( array(
		'post_type'      => 'page',
		'name'           => $slug,
		'post_status'    => array( 'publish', 'draft', 'pending', 'trash' ),
		'posts_per_page' => 1,
		'fields'         => 'ids',
	) );
	if ( $existing ) {
		$pid = (int) $existing[0];
		wp_update_post( array(
			'ID'          => $pid,
			'post_title'  => $payload['title'],
			'post_status' => $status,
		) );
		$created = false;
	} else {
		$pid = wp_insert_post( array(
			'post_title'  => $payload['title'],
			'post_name'   => $slug,
			'post_type'   => 'page',
			'post_status' => $status,
		) );
		if ( ! $pid || is_wp_error( $pid ) ) {
			wp_send_json_error( 'insert' );
		}
		$created = true;
	}

	update_post_meta( $pid, '_elementor_edit_mode', 'builder' );
	update_post_meta( $pid, '_elementor_template_type', 'wp-page' );
	update_post_meta( $pid, '_elementor_version', $payload['elementor']['version'] );
	update_post_meta( $pid, '_elementor_data', wp_slash( wp_json_encode( $payload['elementor']['data'] ) ) );
	update_post_meta( $pid, '_lr_replica', 1 );
	update_post_meta( $pid, '_wp_page_template', 'elementor_header_footer' );
	delete_post_meta( $pid, '_elementor_css' );
	delete_post_meta( $pid, '_elementor_element_cache' );

	if ( ! empty( $payload['seo'] ) ) {
		foreach ( array( 'rank_math_title', 'rank_math_description', 'rank_math_canonical' ) as $k ) {
			if ( isset( $payload['seo'][ $k ] ) && '' !== $payload['seo'][ $k ] ) {
				update_post_meta( $pid, $k, sanitize_text_field( $payload['seo'][ $k ] ) );
			}
		}
	}

	if ( class_exists( '\Elementor\Core\Files\CSS\Post' ) ) {
		$css_file = new \Elementor\Core\Files\CSS\Post( $pid );
		$css_file->update();
	}
	wp_send_json_success( array(
		'page'    => $pid,
		'slug'    => $slug,
		'created' => $created,
		'elements' => count( $payload['elementor']['data'] ),
	) );
} );

/**
 * action=lr_elem_template  name=<模板标题>  slug=<post_name>  template_type=page|container
 *                          url=<https://nownexts.com/lr-assets/elem/templates/*.json>  secret=...
 *   → upsert elementor_library 帖子（按 post_name 去重），写 Elementor 模板 meta。
 *     模板 JSON 格式同页面：{"version":"3.35.7","data":[...]}
 */
add_action( 'wp_ajax_lr_elem_template', function () {
	if ( ! current_user_can( 'edit_pages' ) ) {
		wp_send_json_error( 'perm' );
	}
	if ( ! isset( $_POST['secret'] ) || LR_BRIDGE_SECRET !== $_POST['secret'] ) {
		wp_send_json_error( 'secret' );
	}
	$name = isset( $_POST['name'] ) ? sanitize_text_field( wp_unslash( $_POST['name'] ) ) : '';
	$slug = isset( $_POST['slug'] ) ? sanitize_title( wp_unslash( $_POST['slug'] ) ) : '';
	$type = isset( $_POST['template_type'] ) ? sanitize_key( wp_unslash( $_POST['template_type'] ) ) : 'container';
	$category = isset( $_POST['category'] ) ? sanitize_text_field( wp_unslash( $_POST['category'] ) ) : '';
	$url  = isset( $_POST['url'] ) ? esc_url_raw( wp_unslash( $_POST['url'] ) ) : '';
	if ( ! $name || ! $slug || ! in_array( $type, array( 'page', 'container', 'section' ), true )
		|| 0 !== strpos( $url, 'https://nownexts.com/lr-assets/' ) ) {
		wp_send_json_error( 'args' );
	}
	$r = wp_remote_get( $url, array( 'timeout' => 90 ) );
	if ( is_wp_error( $r ) || 200 !== (int) wp_remote_retrieve_response_code( $r ) ) {
		wp_send_json_error( 'fetch:' . wp_remote_retrieve_response_code( $r ) );
	}
	$payload = json_decode( wp_remote_retrieve_body( $r ), true );
	if ( empty( $payload['data'] ) || ! is_array( $payload['data'] ) ) {
		wp_send_json_error( 'payload' );
	}

	$existing = get_posts( array(
		'post_type'      => 'elementor_library',
		'name'           => $slug,
		'post_status'    => array( 'publish', 'draft', 'trash' ),
		'posts_per_page' => 1,
		'fields'         => 'ids',
	) );
	$pid = $existing ? (int) $existing[0] : 0;
	if ( $pid ) {
		wp_update_post( array( 'ID' => $pid, 'post_title' => $name, 'post_status' => 'publish' ) );
		$created = false;
	} else {
		$pid = wp_insert_post( array(
			'post_title'  => $name,
			'post_name'   => $slug,
			'post_type'   => 'elementor_library',
			'post_status' => 'publish',
		) );
		if ( ! $pid || is_wp_error( $pid ) ) {
			wp_send_json_error( 'insert' );
		}
		$created = true;
	}
	update_post_meta( $pid, '_elementor_edit_mode', 'builder' );
	update_post_meta( $pid, '_elementor_template_type', $type );
	update_post_meta( $pid, '_elementor_version', isset( $payload['version'] ) ? $payload['version'] : '3.35.7' );
	update_post_meta( $pid, '_elementor_data', wp_slash( wp_json_encode( $payload['data'] ) ) );
	delete_post_meta( $pid, '_elementor_element_cache' );
	if ( $category && taxonomy_exists( 'elementor_library_category' ) ) {
		wp_set_object_terms( $pid, array( $category ), 'elementor_library_category', false );
	}
	wp_send_json_success( array(
		'template' => $pid,
		'slug' => $slug,
		'created' => $created,
		'elements' => count( $payload['data'] ),
		'category' => $category,
	) );
} );