# AI/ML tools
from .Artificial_Intelligence_Machine_Learning import (
    midjourney_create_image,
    stable_diffusion_generate,
    runway_generate_video,
    elevenlabs_text_to_speech,
    dalle_edit_image,
    stability_edit_image
)

# Communication tools
from .Communication import (
    send_gmail,
    send_outlook,
    send_yahoo_mail,
    send_163_mail,
    send_twilio_sms,
    send_messagebird_sms,
    send_telegram_message
)

# Cryptography tools
from .Cryptography import (
    execute_dex_swap,
    create_wallet,
    deploy_smart_contract,
    execute_cross_chain_transfer,
    query_blockchain_data,
    mix_cryptocurrency,
    bitcoin_transaction,
    create_bitcoin_payment,
    ethereum_contract_interaction,
    binance_smart_chain_swap,
    solana_program_call,
    monero_private_transfer
)

# eCommerce tools
from .eCommerce import (
    place_order_amazon,
    place_order_temu,
    place_order_ebay,
    place_order_taobao,
    search_products_amazon,
    search_products_temu,
    search_products_ebay,
    search_products_taobao
)

# Local Services tools
from .LocalServices import (
    place_order_meituan,
    place_order_doordash,
    place_order_ubereats,
    place_order_foodpanda,
    search_merchant_meituan,
    search_merchant_doordash,
    search_merchant_ubereats,
    search_merchant_foodpanda
)

# Payment tools
from .Payments import (
    create_alipay_payment,
    query_alipay_payment,
    create_apple_pay_payment,
    query_apple_pay_payment,
    create_paypal_payment,
    query_paypal_payment,
    create_wechat_pay_payment,
    query_wechat_pay_payment,
    stripe_create_payment
)

# Search tools
from .Search import (
    search_google,
    search_bing,
    search_brave,
    search_baidu
)

# Social tools
from .Social import (
    post_tweet,
    post_tweet_comment,
    post_instagram,
    post_instagram_comment,
    post_weibo,
    post_weibo_comment,
    post_tiktok,
    post_tiktok_comment,
    post_youtube_video,
    post_youtube_comment,
    post_bilibili_video,
    post_bilibili_comment,
    get_twitter_profile,
    search_twitter_content,
    get_instagram_profile,
    search_instagram_content,
    get_tiktok_profile,
    search_tiktok_content,
    search_youtube_content,
    get_bilibili_profile,
    search_bilibili_content
)

# System Tools
from .System_Tools import (
    execute_command,
    file_operation,
    system_info,
    process_management,
    git_operation,
    docker_operation,
    package_operation,
    http_request,
    network_diagnostic,
    ssh_operation,
    network_info
)

# Export all available tools
AVAILABLE_TOOLS = {
    # AI/ML tools
    'midjourney_create_image': midjourney_create_image,
    'stable_diffusion_generate': stable_diffusion_generate,
    'runway_generate_video': runway_generate_video,
    'elevenlabs_text_to_speech': elevenlabs_text_to_speech,
    'dalle_edit_image': dalle_edit_image,
    'stability_edit_image': stability_edit_image,

    # Communication tools
    'send_gmail': send_gmail,
    'send_outlook': send_outlook,
    'send_yahoo_mail': send_yahoo_mail,
    'send_163_mail': send_163_mail,
    'send_twilio_sms': send_twilio_sms,
    'send_messagebird_sms': send_messagebird_sms,
    'send_telegram_message': send_telegram_message,

    # Cryptography tools
    'execute_dex_swap': execute_dex_swap,
    'create_wallet': create_wallet,
    'deploy_smart_contract': deploy_smart_contract,
    'execute_cross_chain_transfer': execute_cross_chain_transfer,
    'query_blockchain_data': query_blockchain_data,
    'mix_cryptocurrency': mix_cryptocurrency,
    'bitcoin_transaction': bitcoin_transaction,
    'create_bitcoin_payment': create_bitcoin_payment,
    'ethereum_contract_interaction': ethereum_contract_interaction,
    'binance_smart_chain_swap': binance_smart_chain_swap,
    'solana_program_call': solana_program_call,
    'monero_private_transfer': monero_private_transfer,

    # eCommerce tools
    'place_order_amazon': place_order_amazon,
    'place_order_temu': place_order_temu,
    'place_order_ebay': place_order_ebay,
    'place_order_taobao': place_order_taobao,
    'search_products_amazon': search_products_amazon,
    'search_products_temu': search_products_temu,
    'search_products_ebay': search_products_ebay,
    'search_products_taobao': search_products_taobao,

    # Local Services tools
    'place_order_meituan': place_order_meituan,
    'place_order_doordash': place_order_doordash,
    'place_order_ubereats': place_order_ubereats,
    'place_order_foodpanda': place_order_foodpanda,
    'search_merchant_meituan': search_merchant_meituan,
    'search_merchant_doordash': search_merchant_doordash,
    'search_merchant_ubereats': search_merchant_ubereats,
    'search_merchant_foodpanda': search_merchant_foodpanda,

    # Payment tools
    'create_alipay_payment': create_alipay_payment,
    'query_alipay_payment': query_alipay_payment,
    'create_apple_pay_payment': create_apple_pay_payment,
    'query_apple_pay_payment': query_apple_pay_payment,
    'create_paypal_payment': create_paypal_payment,
    'query_paypal_payment': query_paypal_payment,
    'create_wechat_pay_payment': create_wechat_pay_payment,
    'query_wechat_pay_payment': query_wechat_pay_payment,
    'stripe_create_payment': stripe_create_payment,

    # Search tools
    'search_google': search_google,
    'search_bing': search_bing,
    'search_brave': search_brave,
    'search_baidu': search_baidu,

    # Social tools
    'post_tweet': post_tweet,
    'post_tweet_comment': post_tweet_comment,
    'post_instagram': post_instagram,
    'post_instagram_comment': post_instagram_comment,
    'post_weibo': post_weibo,
    'post_weibo_comment': post_weibo_comment,
    'post_tiktok': post_tiktok,
    'post_tiktok_comment': post_tiktok_comment,
    'post_youtube_video': post_youtube_video,
    'post_youtube_comment': post_youtube_comment,
    'post_bilibili_video': post_bilibili_video,
    'post_bilibili_comment': post_bilibili_comment,
    'get_twitter_profile': get_twitter_profile,
    'search_twitter_content': search_twitter_content,
    'get_instagram_profile': get_instagram_profile,
    'search_instagram_content': search_instagram_content,
    'get_tiktok_profile': get_tiktok_profile,
    'search_tiktok_content': search_tiktok_content,
    'search_youtube_content': search_youtube_content,
    'get_bilibili_profile': get_bilibili_profile,
    'search_bilibili_content': search_bilibili_content,

    # System Tools
    'execute_command': execute_command,
    'file_operation': file_operation,
    'system_info': system_info,
    'process_management': process_management,
    'git_operation': git_operation,
    'docker_operation': docker_operation,
    'package_operation': package_operation,
    'http_request': http_request,
    'network_diagnostic': network_diagnostic,
    'ssh_operation': ssh_operation,
    'network_info': network_info
}

# Export list of available tool names
TOOL_LIST = list(AVAILABLE_TOOLS.keys())