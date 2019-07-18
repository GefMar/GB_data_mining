DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
}

ROTATING_PROXY_LIST = ['51.68.95.200:8080',
                       '138.197.202.174:3128',
                       '94.130.20.85:31288',
                       '5.79.227.20:8080']