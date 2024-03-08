import streamlit as st
import requests

urls = [
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetCompanyEnrichment?code=QaE8UX7kwcYV57WIdm0gLA/T2JPKevT5w2juw9x76wcJl7XNvyaAtQ==&Url=<<Url>>",
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetDomainCategories?code=i1wUn2KLjnQ8kKV077fD3xBXGNw3kJZtC3fUb6vNDvseF2AjerbV8w==&Url=<<Url>>&Country=<<Country>>",
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetMetaScraping?code=vdT93lDIpuitGDf4pLxBChaZOCQ6o_jNOmLLtxjWGuHDAzFu6VOBBQ==&Url=<<Url>>",
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetTrustpilot?code=6cwB4fuIlVqwCaksbAdM5ReeTiUXefxIzDIagJWKf_5aAzFuy2PaLg==&Token=&Url=<<Url>>",
    "https://branalyzerazuresocialmediafunctions.azurewebsites.net/api/GetSocialMediaFromUrl?code=N0JyCYxIh62m1fu2eedLKkV0Nk1ce04pEU7s4JyfgTrpYvoUMo4JeQ==&Url=<<Url>>",
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetDomainsHistory?code=5CN5DhdsbWiQ0LazNsD7YV2oqWx/mWXxPJfVz4tQ5W75EfoKFqpM8A==&Url=<<Url>>&Country=<<Country>>",
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetDomainKeywords?code=keMqyBpejEqJZDTU4Es3FFleZa97ml5MwQQpXUjsLedCGbQ4cG5Ggw==&Url=<<Url>>&Country=<<Country>>",
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetDomainBacklinks?code=wwomGd4AKCbOYDv0ZopQA00ZzqYuvAD/gxgh2BnGeWmjQVq3JnbUjg==&Url=<<Url>>&Mode=",
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetDomainCompetitors?code=ZP1DRmPagZkpQYSMqIklvgHzHbbfOCZKZZcuMv1SfBaWd1JVg9SjOw==&Url=<<Url>>&Country=<<Country>>",
]

# Define headers
headers = {
    'accept': "application/json, text/plain, */*",
    'accept-language': "en-US,en;q=0.9",
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': "empty",
    'sec-fetch-mode': "cors",
    'sec-fetch-site': "cross-site",
    'Referer': "https://branalyzer.com/",
    'Referrer-Policy': "strict-origin-when-cross-origin"
}

def make_request(url, params):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)

def main():
    st.title("Branalyzer Clone")
    url_input = st.text_input("Enter URL:")
    country_input = st.text_input("Enter Country:")
    error_occurred = False
    if st.button("Proceed"):
        for url in urls:
            url = url.replace("<<Url>>", url_input).replace("<<Country>>", country_input)
            endpoint = url.split("/api/")[1].split("?")[0]
            response, error = make_request(url, {})
            if response is not None:
                with st.expander("URL: " + endpoint):
                    st.json(response)
            else:
                st.error(f"Error occurred for {endpoint}: {error}")
                error_occurred = True

        if not error_occurred:
            st.success("All requests completed successfully.")

if __name__ == "__main__":
    main()