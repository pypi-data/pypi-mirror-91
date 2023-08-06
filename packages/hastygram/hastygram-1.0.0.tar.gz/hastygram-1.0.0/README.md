# hastygram
 
[![Build status](https://github.com/Zopieux/hastygram/workflows/Package/badge.svg)](https://github.com/Zopieux/hastygram/actions)

A lightweight frontend for Instagram. No fuss, just navigate to `/<username>` and enjoy the content.
This supports images, videos and "groups" thereof – Instagram call them *sidecars*.

Click on a media to enlarge it to its original resolution. No more ridiculously small pictures!

### Usage

1. You need an account, otherwise Instagram will quickly rate-limit your anonymous session.
2. Connect to Instagram using the [website](https://instagram.com), then using the browser devtools, copy the `sessionid` 
   cookie value to the clipboard.
3. On your Hastygram frontend, use the **Authenticate** button to paste the cookie value. This is necessary only once.
4. If you encounter errors after a while, follow the same procedure again with a fresh `sessionid` cookie.

### Building and deploying

See [`/example`](/example) for an example deployment using Nginx. 

```shell
# The frontend:
# You'll have to serve the resulting web/build/ directory as static files.
$ ( cd web && yarn run build )

# The Python backend:
# You'll have to reverse-proxy :8000 in location /_.
$ pip install hastygram 'uvicorn[standard]'
$ uvicorn hastygram.app:app --port 8000
```

### License

GNU General Public License v3.0

### Screenshot

![screenshot](.github/screenshot.jpeg)
