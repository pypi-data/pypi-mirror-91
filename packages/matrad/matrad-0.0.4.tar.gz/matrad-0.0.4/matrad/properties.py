from requests import get, post, delete, put


# Where the list of tradable coin pairs will be stored
pair_list_path = 'pairs.txt'

# Mapping between the HTTP method expected by an API function and its corresponding requests method
req_mapping = {'GET': get, 'POST': post, 'DELETE': delete, 'PUT': put}

# Available urls for the Binance API. See: https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#general-api-information
urls = ['https://api.binance.com', 'https://api1.binance.com', 'https://api2.binance.com', 'https://api3.binance.com']

# The key is the internal name of each function on the API.
endpoint_mapping = {
    'connectivity': {'endpoint': '/api/v3/ping', 'method': 'GET', 'signature_required': False},
    'server_time': {'endpoint': '/api/v3/time', 'method': 'GET', 'signature_required': False},
    'exchange_info': {'endpoint': '/api/v3/exchangeInfo', 'method': 'GET', 'signature_required': False},
    'depth': {'endpoint': '/api/v3/depth', 'method': 'GET', 'signature_required': False},
    'recent_trades': {'endpoint': '/api/v3/trades', 'method': 'GET', 'signature_required': False},
    'old_trades': {'endpoint': '/api/v3/historicalTrades', 'method': 'GET', 'signature_required': False},
    'aggregated_trade_list': {'endpoint': '/api/v3/aggTrades', 'method': 'GET', 'signature_required': False},
    'candlesticks': {'endpoint': '/api/v3/klines', 'method': 'GET', 'signature_required': False},
    'current_avg_price': {'endpoint': '/api/v3/avgPrice', 'method': 'GET', 'signature_required': False},
    '24hr_price_stats': {'endpoint': '/api/v3/ticker/24hr', 'method': 'GET', 'signature_required': False},
    'latest_price': {'endpoint': '/api/v3/ticker/price', 'method': 'GET', 'signature_required': False},
    'order_book_best': {'endpoint': '/api/v3/ticker/bookTicker', 'method': 'GET', 'signature_required': False},
    'order': {'endpoint': '/api/v3/order', 'method': 'POST', 'signature_required': True},
    'order_test': {'endpoint': '/api/v3/order/test', 'method': 'POST', 'signature_required': True},
    'query_order': {'endpoint': '/api/v3/order', 'method': 'GET', 'signature_required': True},
    'cancel_order': {'endpoint': '/api/v3/order', 'method': 'DELETE', 'signature_required': True},
    'cancel_all_open_orders': {'endpoint': '/api/v3/openOrders', 'method': 'DELETE', 'signature_required': True},
    'current_open_orders': {'endpoint': '/api/v3/openOrders', 'method': 'GET', 'signature_required': True},
    'all_orders': {'endpoint': '/api/v3/allOrders', 'method': 'GET', 'signature_required': True},
    'new_oco': {'endpoint': '/api/v3/order/oco', 'method': 'POST', 'signature_required': True},
    'cancel_oco': {'endpoint': '/api/v3/orderList', 'method': 'DELETE', 'signature_required': True},
    'query_oco': {'endpoint': '/api/v3/orderList', 'method': 'GET', 'signature_required': True},
    'query_all_oco': {'endpoint': '/api/v3/allOrderList', 'method': 'GET', 'signature_required': True},
    'query_open_oco': {'endpoint': '/api/v3/openOrderList', 'method': 'GET', 'signature_required': True},
    'account_information': {'endpoint': '/api/v3/account', 'method': 'GET', 'signature_required': True},
    'account_trade_list': {'endpoint': '/api/v3/myTrades', 'method': 'GET', 'signature_required': True},
    'trade_list': {'endpoint': '/api/v3/myTrades', 'method': 'GET', 'signature_required': True},
    'start_datastream': {'endpoint': '/api/v3/userDataStream', 'method': 'POST', 'signature_required': False},
    'keep_alive_datastream': {'endpoint': '/api/v3/userDataStream', 'method': 'PUT', 'signature_required': False}
}