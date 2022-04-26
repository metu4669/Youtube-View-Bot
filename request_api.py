import requests


def starter():
    api_key = "8023b664b6edf63ccace6a2ee62c8eb1a70c498c"
    main_url = "https://proxy.webshare.io"
    _next = "/api/proxy/list/?page=1"
    proxies = []
    while _next is not None:
        response = requests.get(main_url+_next,
                                headers={"Authorization": "Token "+api_key})
        _next = response.json()["next"]
        for result in response.json()["results"]:
            proxy = "socks5://"+result["username"]+":"+result["password"]+"@"+result["proxy_address"]+":"+str(result["ports"]["socks5"])
            proxies.append(proxy)
    return proxies
