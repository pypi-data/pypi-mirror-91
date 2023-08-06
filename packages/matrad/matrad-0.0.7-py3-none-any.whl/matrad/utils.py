import json, time, hmac, hashlib
from typing import Dict, List, Tuple
from os.path import expanduser, join
from .properties import req_mapping, endpoint_mapping, pair_list_path, urls


def get_current_timestamp() -> int:
    """Get current timestamp in the same form than provided by Binance API

    Returns:
        int: Current timestamp (in ms)
    """    
    return round(time.time() * 1000)


def get_api_key(secret=False) -> str:
    """Get secret api key from .binance_api_secrets file stored in current directory

    Args:
        secret (bool, optional): If to return the secret (True) or the key (False). Defaults to False.

    Returns:
        str: your Binance API key
    """    
    secret_path = join(expanduser('~'), '.binance_api_secrets')
    with open(secret_path) as f:
        keys = json.load(f)
    key = keys.get('secret') if secret else keys.get('key')
    return key


def get_query_string(params: Dict) -> str:
    """Makes a string corresponding to the query string of `params`

    Args:
        params (Dict): Parameters given in the API call

    Returns:
        str: URL argument used to call the API
    """
    return '&'.join([f'{k}={v}' for k, v in params.items()])


def get_hashmap_signature(params: Dict, data: Dict = {}, secret_key: Tuple[str, None] = None) -> str:
    """Compute HMAC SHA256 signature for the arguments given in the query string and request body
    See: https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#signed-endpoint-examples-for-post-apiv3order
    Args:
        params (Dict): Query string key-value pairs
        data (Dict, optional): Request body key-value pairs
        secret_key (str, optional): Your personal Binance API secret

    Returns:
        str: signature expected by the Binance API
    """
    msg = get_query_string(params) + get_query_string(data)
    secret_key = get_api_key(secret=True) if secret_key is None else secret_key
    signature = hmac.new(secret_key.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature


def call_api(url: str = 'https://api.binance.com', endpoint: str = '', method: str = 'GET', params: Dict = {}, data: Dict = {}, 
            signature_required: bool = False, raw: bool = False, key: Tuple[str, None] = None, secret_key: Tuple[str, None] = None) -> Dict:
    """ Query the Binance API to the specified `url` at the given `endpoint` with the corresponding `method`.
    If there is an error, it will return a corresponding Dict up to the caller to handle. 
    Args:
        url (str, optional): URL where to adress the API. Defaults to 'https://api.binance.com'.
        endpoint (str, optional): Endpoint corresponding to the API function to call. Defaults to ''.
        method (str, optional): HTTP method to use. Defaults to 'GET'.
        params (Dict, optional): Parameters corresponding to the query string. Defaults to {}.
        data (Dict, optional): Parameters corresponding to the request body. Defaults to {}.
        signature_required (bool, optional): If the function called requires a signature or not. Defaults to False.
        raw (bool, optional): If to return the result raw result (True) or as a Dict (False). Defaults to False.
        key (str, optional): Your personal Binance API public key
        secret_key (str, optional): Your personal Binance API secret

    Returns:
        Dict: either the result of the function (API response) or the error it generated
    """
    key = get_api_key(secret=False) if key is None else key
    headers = {'Content-Type': 'application/json;charset=utf-8', 'X-MBX-APIKEY': key}
    if signature_required:
        signature = get_hashmap_signature(params, data, secret_key)
        params['signature'] = signature
    req = req_mapping.get(method)
    if req is None:
        error_message = f"method '{method}' not supported for requests, only {','.join(list(req_mapping.keys()))}"
        print(f"ERROR: {error_message}")
        return {'requeserror': error_message}
    response = req(f'{url}{endpoint}', headers=headers, params=params, data=data)
    status_code = response.status_code
    if status_code != 200:
        return {'httperror': status_code}
    if not raw:
        response = response.json()
    return response


def execute_query(name: str, params: Dict = {}, data: Dict = {}, url: str = 'https://api.binance.com', 
                    raw: bool = False, key: Tuple[str, None] = None, secret_key: Tuple[str, None] = None) -> Dict: 
    """Execute query to the Binance API given its name as defined in `endpoint_mapping` in properties.py.
    It basically wraps `call_api()`.

    Args:
        name (str): Name of the query to execute. Must be a key in `endpoint_mapping`
        params (Dict, optional): Corresponds to the query string for the query. Defaults to {}.
        data (Dict, optional): Parameters corresponding to the request body. Defaults to {}.
        url (str, optional): Corresponds to the request body for the query. Defaults to 'https://api.binance.com'.
        raw (bool, optional): If to return the response in raw form (True) or as Dict (False). Defaults to False.
        key (str, optional): Your personal Binance API public key
        secret_key (str, optional): Your personal Binance API secret

    Returns:
        Dict: either the result of the function (API response) or the error it generated
    """
    props = endpoint_mapping.get(name)
    
    if props is None:
        print(f"ERROR: '{name}' is not a supported function. \
                    Supported functions: {', '.join(list(endpoint_mapping.keys()))}")
        return {}
    endpoint, method, signature_required = props.get('endpoint'), props.get('method'), props.get('signature_required')
    response = call_api(url=url, endpoint=endpoint, method=method, params=params, data=data, 
                        signature_required=signature_required, raw=raw, key=key, secret_key=secret_key)
    return response
    

def update_pair_list() -> None:
    """ Generate or update the list of coin pairs available on Binance and 
    saves it under `pair_list_path` defined in properties.py """
    prices = execute_query('latest_price')
    pairs = [price.get('symbol') for price in prices]
    with open(pair_list_path, 'w') as f:
        f.write('\n'.join(pairs))


def get_all_pairs(update: bool = False) -> List[str]:
    """Get all pairs of coins available on Binance

    Args:
        update (bool, optional): If to update it from the Binance API. Defaults to False.

    Returns:
        List: All the coin pairs available
    """
    if update:
        update_pair_list
    with open(pair_list_path, 'r') as f:
        pairs = f.readlines()
    pairs = [pair.replace('\n', '') for pair in pairs]
    return pairs


def get_urls_speeds() -> Dict:
    """Compares the speed of the different Binance urls (as listed in `urls` in properties.py)

    Returns:
        Dict: Ping duration (in second) for each url.
    """
    urls_speeds = {}
    for url in urls:
        response = execute_query('connectivity', url=url, raw=True)
        duration = response.elapsed.total_seconds()
        urls_speeds[url] = duration
    return urls_speeds
