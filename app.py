import streamlit as st
import json
import requests
import pandas as pd
urls = [
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetCompanyEnrichment?code=QaE8UX7kwcYV57WIdm0gLA/T2JPKevT5w2juw9x76wcJl7XNvyaAtQ==&Url=<<Url>>",
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetDomainCategories?code=i1wUn2KLjnQ8kKV077fD3xBXGNw3kJZtC3fUb6vNDvseF2AjerbV8w==&Url=<<Url>>&Country=<<Country>>",
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetMetaScraping?code=vdT93lDIpuitGDf4pLxBChaZOCQ6o_jNOmLLtxjWGuHDAzFu6VOBBQ==&Url=<<Url>>",
    # "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetTrustpilot?code=6cwB4fuIlVqwCaksbAdM5ReeTiUXefxIzDIagJWKf_5aAzFuy2PaLg==&Token=&Url=<<Url>>",
    # "https://branalyzerazuresocialmediafunctions.azurewebsites.net/api/GetSocialMediaFromUrl?code=N0JyCYxIh62m1fu2eedLKkV0Nk1ce04pEU7s4JyfgTrpYvoUMo4JeQ==&Url=<<Url>>",
    # "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetDomainsHistory?code=5CN5DhdsbWiQ0LazNsD7YV2oqWx/mWXxPJfVz4tQ5W75EfoKFqpM8A==&Url=<<Url>>&Country=<<Country>>",
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetDomainKeywords?code=keMqyBpejEqJZDTU4Es3FFleZa97ml5MwQQpXUjsLedCGbQ4cG5Ggw==&Url=<<Url>>&Country=<<Country>>",
    "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetDomainBacklinks?code=wwomGd4AKCbOYDv0ZopQA00ZzqYuvAD/gxgh2BnGeWmjQVq3JnbUjg==&Url=<<Url>>&Mode=",
    # "https://branalyzerazuredomainfunctions.azurewebsites.net/api/GetDomainCompetitors?code=ZP1DRmPagZkpQYSMqIklvgHzHbbfOCZKZZcuMv1SfBaWd1JVg9SjOw==&Url=<<Url>>&Country=<<Country>>",
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


def make_clickable(link):
    # Check if link already starts with "http://" or "https://"
    if not link.startswith("http://") and not link.startswith("https://"):
        link = "https://" + link
    # Return the clickable link
    return link


def make_request(url, params):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


# def get_emails_and_social_media_links(url):
#     endpoint = "https://branalyzerazuresocialmediafunctions.azurewebsites.net/api/GetSocialMediaFromUrl?code=N0JyCYxIh62m1fu2eedLKkV0Nk1ce04pEU7s4JyfgTrpYvoUMo4JeQ==&Url=<<Url>>"
#     response, error = make_request(endpoint.replace("<<Url>>", url), {})
#     emails = []
#     if response is not None:
#         # st.success(response)
#         for email in response['emails']:
#             emails.append(email['value'])
#         return json.dumps(email)
#     else:
#         return None
    
    
def get_emails_and_social_media_links(url):
    endpoint = "https://branalyzerazuresocialmediafunctions.azurewebsites.net/api/GetSocialMediaFromUrl?code=N0JyCYxIh62m1fu2eedLKkV0Nk1ce04pEU7s4JyfgTrpYvoUMo4JeQ==&Url=<<Url>>"
    
    try:
        response = requests.get(endpoint.replace("<<Url>>", url))
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        
        emails = []
        for email in data.get('emails', []):
            emails.append(email['value'])
        
        return json.dumps(emails)
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    except KeyError as e:
        print(f"Error: Key not found in response - {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON response - {e}")
        return None    
    
st.title("Branalyzer Clone")
url_input = st.text_input("Enter URL:")
country_input = st.text_input("Enter Country:")
error_occurred = False

if st.button("Proceed"):
    results = st.session_state.get("results", {})
    for url in urls:
        url = url.replace("<<Url>>", url_input).replace(
            "<<Country>>", country_input)
        endpoint = url.split("/api/")[1].split("?")[0]
        response, error = make_request(url, {})
        if response is not None:
            results[endpoint] = response
            st.session_state["results"] = results
            with st.expander("URL: " + endpoint):
                st.json(response)
        else:
            st.error(f"Error occurred for {endpoint}: {error}")
            # error_occurred = True

    st.success("All requests completed successfully.")

# Display summary
results = st.session_state.get("results", {})
if 'GetCompanyEnrichment' in results and isinstance(results['GetCompanyEnrichment'], dict):
    st.header("Company Enrichment Summary")
    for key, value in results['GetCompanyEnrichment'].items():
        st.markdown(f"**{key}**: {value}")

if 'GetDomainCategories' in results and isinstance(results['GetDomainCategories'], dict):
    st.header("Domain Categories Summary")
    for key, value in results['GetDomainCategories'].items():
        st.markdown(f"**{key}**: {value}")

if 'GetMetaScraping' in results and isinstance(results['GetMetaScraping'], dict):
    st.header("Meta Scraping Summary")
    for key, value in results['GetMetaScraping'].items():
        st.markdown(f"**{key}**: {value}")


if 'GetDomainKeywords' in results and isinstance(results['GetDomainKeywords'], list):
    st.header("Brand Keywords")
    # for item in results['GetDomainKeywords']:
    #     st.json(item)
    df_dkw = pd.DataFrame(results['GetDomainKeywords'])
    # List of columns to keep
    columns_to_keep = ['keyword', "traff", 'cost', 'url']

    # Selecting only the specified columns
    df_dkw = df_dkw.loc[:, columns_to_keep]

    # Sort the DataFrame based on the "traff" column in descending order
    df_dkw = df_dkw.sort_values(by='traff', ascending=False)

    st.dataframe(
        df_dkw,
        column_config={
            "keyword": st.column_config.TextColumn("Keyword"),
            "traff": st.column_config.TextColumn("Traffic"),
            "cost": st.column_config.TextColumn("CPC"),
            "url": st.column_config.LinkColumn("URL")
        },
        hide_index=True,
        use_container_width=True
    )
    # st.table(item)

if 'GetDomainBacklinks' in results and isinstance(results['GetDomainBacklinks'], dict):
    st.header("Brand Backlinks")
    backlink_data = results['GetDomainBacklinks']
    for key, value in backlink_data.items():
        if key != 'domainsList':
            st.markdown(f"**{key}**: {value}")
    if 'domainsList' in backlink_data and isinstance(backlink_data['domainsList'], list):
        st.subheader("Backlink Domains List")
        df = pd.DataFrame(backlink_data['domainsList'])

        # List of columns to keep
        columns_to_keep = ['domain', 'categoryMainIAB', 'links',
                           'mozDA', 'mozPA', 'majesticCF', 'majesticTF', 'price', "traff"]

        # Selecting only the specified columns
        df = df.loc[:, columns_to_keep]



        # Sort the DataFrame based on the "traff" column in descending order
        df = df.sort_values(by='price', ascending=False)

        # Apply the function to each row to create the new column "contact_emails"
        df['contact_emails'] = df['domain'].apply(get_emails_and_social_media_links)
        df['domain'] = df['domain'].apply(make_clickable)

        st.dataframe(
            df,
            column_config={
                "domain": st.column_config.LinkColumn("Domain"),
                "categoryMainIAB": st.column_config.TextColumn("Category"),
                "links": st.column_config.TextColumn("Links"),
                "mozDA": st.column_config.TextColumn("DA"),
                "mozPA": st.column_config.TextColumn("PA"),
                "majesticCF": st.column_config.TextColumn("CF"),
                "majesticTF": st.column_config.TextColumn("TF"),
                "price": st.column_config.TextColumn("Price"),
                "traff": st.column_config.TextColumn("Traffic"),
                "contact_emails": st.column_config.TextColumn("Contact Emails")
            },
            hide_index=True,
        )
