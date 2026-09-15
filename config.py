import os 

from dotenv import load_dotenv

load_dotenv()

LOG_PATH = "./output/main.log"

PROXIES = {
    "http": os.getenv("PROXY"),
    "https": os.getenv("PROXY")
}

TIMEOUT = 30

BASE_URL="https://www.buscalibre.com.ar"

DISCOVERY_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:157.0) Gecko/20100101 Firefox/157.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    # 'Cookie': 'bl_session=7cqb2tn2iab160b6u6cq9c9p6d; _ga_D5PFPYSQF6=GS2.1.s1789473156$o3$g0$t1789473170$j46$l0$h0; _ga=GA1.3.601826788.1786966921; _twpid=tw.1786966921933.272113962913097784; _fbp=fb.2.1786966922159.91210210212844113.AQYAAQIB; _tt_enable_cookie=1; _ttp=01M07REMZGMTNWXJ3M0PS6KBVZ_.tt.2; ttcsid_CG90VRRC77U77CS2EGKG=1786966922231::_8OlXSVql5ghWeIH4as5.1.1786967335619.1; ttcsid=1786966922231::eBzZkKq9KivvstT2ayqp.1.1786967335619.0::1.412067.413116::412048.14.111.97::423134.152.0; _hjSessionUser_3613354=eyJpZCI6ImM3ZDk0OWQ2LWQyNDItNTE3Mi04MDlmLTc2OGIxYTBjY2Y5OSIsImNyZWF0ZWQiOjE3ODY5NjY5MjIyNTEsImV4aXN0aW5nIjp0cnVlfQ==; g_state={"i_l":2,"i_ll":1786967335410,"i_b":"TNgpxBCWNd8160pB3utaPCXt0BT0HL28GHfaaDN6UR8","i_e":{"enable_itp_optimization":24},"i_et":1786967335410,"i_p":1787053622021}; _gcl_au=1.1.966504775.1786967219; _gid=GA1.3.1882527332.1789473157; _twsid=1789473157110-818011595.1.1789473167115; _hjSession_3613354=eyJpZCI6IjQ1MTk5MzNlLWJiNDUtNDQ5Ny1iMmM4LTIwOWQwNmIwOTJiNSIsImMiOjE3ODk0NzMxNTczNjUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; aws-waf-token=f0c44310-9e48-4329-8ded-7a940119cf85:EQoAjo1pxt5XlAAA:zqYD72fxJUsRBKTMvdfCb/OqLfVjfJLO5IzW7SVdBtaJ5Q0uvDyereaQoTlviJd2x3LR0Vo+y7cEoZEQ1WsBtsThIAdZoUr3iXLh0L3v+M/PuHrLyz9iOISUBi3lOF3Pelb+cJu6xa0mufU5E/W507kwShRYtlAxlX8ESPYIcyOqgSCSmOdRMoWvp4J7kwJKSBlh6bS1mVosFhRF3Y55VVt6r4QiLVqCEFK3myZdIUYvxl7VKjRGCrK4Say9aGyZ391dAgi/EkkiWtq8PbkoDAZ7NKLgYk/DcztuguVlhL/5L6cJWXe/ub89ImYuEZ93LoO0pFE4dn1pOqCAdABkENQ=',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
}

PDP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:157.0) Gecko/20100101 Firefox/157.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    # 'Cookie': 'bl_session=7cqb2tn2iab160b6u6cq9c9p6d; _ga_D5PFPYSQF6=GS2.1.s1789476051$o4$g1$t1789476062$j49$l0$h0; _ga=GA1.1.601826788.1786966921; _twpid=tw.1786966921933.272113962913097784; _fbp=fb.2.1786966922159.91210210212844113.AQYAAQIB; _tt_enable_cookie=1; _ttp=01M07REMZGMTNWXJ3M0PS6KBVZ_.tt.2; ttcsid_CG90VRRC77U77CS2EGKG=1789476070903::56KZeOu9LbTrDeFdDlbs.2.1789476071112.0; ttcsid=1789476070903::Fybx-xYumFuqh3BwiNsx.2.1789476071112.0::1.-27014.0::0.0.0.0::0.0.0; _hjSessionUser_3613354=eyJpZCI6ImM3ZDk0OWQ2LWQyNDItNTE3Mi04MDlmLTc2OGIxYTBjY2Y5OSIsImNyZWF0ZWQiOjE3ODY5NjY5MjIyNTEsImV4aXN0aW5nIjp0cnVlfQ==; g_state={"i_l":2,"i_ll":1786967335410,"i_b":"TNgpxBCWNd8160pB3utaPCXt0BT0HL28GHfaaDN6UR8","i_e":{"enable_itp_optimization":24},"i_et":1786967335410,"i_p":1787053622021}; _gcl_au=1.1.966504775.1786967219; _gid=GA1.3.1882527332.1789473157; _twsid=1789476050064-667663799.2.1789476060066; _gat_UA-41147306-8=1; _hjSession_3613354=eyJpZCI6IjZmY2MzNmZhLTYzMDQtNGIyZi05MmFkLWExNWY1ZmExNmIyZSIsImMiOjE3ODk0NzYwNTA5ODksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; aws-waf-token=f0c44310-9e48-4329-8ded-7a940119cf85:EQoAnqSGHZCsYQAA:k/QbGYDPwUvSzWIkLAE/0ncAg6x9IN0OkhbO68uRNAtxvAwS67KNX0iUynpGTj67MJ+fA1In3PoZ1uC+YeSfSkxdiHSmiNfuzORmMP30ShlFyzDFE87qytH1I8xQQP3GqhA6BIVWbdj9gHX1YVBpKaVC/1mEOKv9JPJo4qoFAi2lMUZhEGnlfWtXid3l04ppkAUyw5RVCM5m9VnTt8U4t1AYW2Lv0+2QPuBTANKfx2VfaqGskOr0EVCpbSUp/QlbP3YgfPT/E5CUeMbYHoNyEx3JIGeKGbuAxYJ+yZidkdqdw0Kz3TKg+xL2qN/cbRwH4eYUvIVfABGPdn/L/ChT+Fw=',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}