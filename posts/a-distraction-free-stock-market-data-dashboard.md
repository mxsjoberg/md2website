# A distraction-free stock market data dashboard

<mark>July 5, 2023</mark> by [Michael Sjöberg](/about.html)

I recently (re)launched my Yahoo Finance alternative "Terminal", it's available here: [trystockstack.com](https://www.trystockstack.com/)

Stockstack is a slimmed-down version of the Terminal with more focus on delivering distraction-free stock market data. The goal is to beat Yahoo Finance in data coverage and user experience. I have removed several old features, such as portfolio tracker, batch requests, and search queries (to reduce workload!).

The updated version instead has an improved grid for organizing data widgets. Data widgets have scalable text, support multiple columns (great for quarterly financials), are resizable, and movable (drag-and-drop).

I have updated almost all data sources and added many new widgets. As a bonus, if you add your own API key for Seeking Alpha (via RapidAPI) there's now five different news widgets.

Threre's also widgets for interest rates, market status, upcoming holidays, and company filings (filed today and historical for ticker). The old chart widget is replace by four smaller widgets for different ranges, so you can now view multiple ranges at the same time.

There's an AI-assistant widget (obviously). It's not as good or fast as looking at data in widgets, but it's very useful for providing wikipedia-style information about companies (especially companies with little or no information provided via APIs).

Here's a few example responses when asking about business model for [Capcom (9697.T)](https://www.trystockstack.com/symbol/9697.T) and [Kakao (035720.KS)](https://www.trystockstack.com/symbol/035720.KS):

> Capcom Co., Ltd. (9697.T) is a Japanese company that is primarily known for its video game development and publishing. They are best known for creating iconic game franchises such as Resident Evil, Street Fighter, and Monster Hunter. In addition to developing and publishing games, Capcom also operates amusement arcades in Japan. Here's an unexpected trivia about Capcom: Did you know that the company's name, "Capcom," is an abbreviation of "Capsule Computers"? This name was chosen to reflect the company's focus on creating innovative games that are like capsules filled with fun and excitement.

> Kakao Corp. (035720.KS) is a South Korean company primarily involved in the technology and communication sector. Their business model revolves around providing various services and platforms to users in different areas. [...] 1. Messaging Services: Kakao Corp. operates messaging services, similar to WhatsApp, Facebook Messenger, LINE, and WeChat. 2. Mobile Content and Gaming: Kakao Corp. competes in the mobile content and gaming industry. They develop and publish popular mobile games and digital content. Competitors in this space include companies like Netmarble, NCSoft, and Nexon. 3. Payments: Kakao Corp. also offers financial services, including digital payment solutions. They compete with companies like PayPal, Alipay, and Apple Pay in the payments sector. 4. Advertising: Kakao Corp. operates in the advertising space as well. They provide digital advertising platforms that help businesses reach their target audience. Competitors in this area include Google Ads, Facebook Ads, and domestic South Korean advertising companies.

Pricing starts at USD 10.00, but will increase to USD 29.00 in a few weeks. I'm still thinking about adding a free plan.
