import browser_cookie3

def fetch_cookies_uri():
    uri = "wss://ws.olymptrade.com/otp?cid_ver=1&cid_app=web%40OlympTrade%402024.4.24560%4024560&cid_device=%40%40desktop&cid_os=windows%4010"
    try:

        # Fetch cookies from Firefox
        cookies = browser_cookie3.firefox(domain_name='olymptrade.com')

        if cookies:
            # Create a single string with cookies in the desired format
            cookie_string = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
            return cookie_string,uri,True  # Return the cookie string
        
        else:
            print("No cookies found.")
            return None ,None,False # Return None if no cookies are found

    except Exception as e:
        print(f"Error fetching cookies: {e}")
        return None,None,False  # Return None on error



