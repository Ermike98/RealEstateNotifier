from immobiliare import ImmobiliareSearch
from selenium import webdriver
import webbrowser
from desktop_notifier import DesktopNotifier, Button, DEFAULT_SOUND
import asyncio

options = webdriver.FirefoxOptions()
options.headless = False
driver = webdriver.Firefox(options=options)

immo_roma_nord_metro_A = "https://www.immobiliare.it/affitto-case/roma/?criterio=data&ordine=desc&prezzoMinimo=600&prezzoMassimo=1100&superficieMinima=40&idMZona[]=10145&idMZona[]=10157&idMZona[]=10172&idQuartiere[]=12741&idQuartiere[]=12716&idQuartiere[]=12709"
immo_roma_sud_metro_A = "https://www.immobiliare.it/affitto-case/roma/?criterio=data&ordine=desc&prezzoMinimo=600&prezzoMassimo=1100&superficieMinima=40&idMZona[]=10151&idMZona[]=10149&idMZona[]=10164&idMZona[]=10152&idMZona[]=10283&idQuartiere[]=10811&idQuartiere[]=10805&idQuartiere[]=10810&idQuartiere[]=11449"
immo_roma_ovest_metro_B = "https://www.immobiliare.it/affitto-case/roma/?criterio=data&ordine=desc&prezzoMinimo=650&prezzoMassimo=1100&superficieMinima=40&idMZona[]=10306&idMZona[]=10147&idMZona[]=10161&idMZona[]=10163&idQuartiere[]=10848&idQuartiere[]=10852&idQuartiere[]=10801&idQuartiere[]=12720&idQuartiere[]=10841&idQuartiere[]=10837&idQuartiere[]=10839"
immo_roma_sud_metro_B = "https://www.immobiliare.it/affitto-case/roma/?criterio=data&ordine=desc&prezzoMinimo=600&prezzoMassimo=1100&superficieMinima=40&idMZona[]=10156&idMZona[]=10170&idMZona[]=10169&idMZona[]=10420&idMZona[]=10167&idMZona[]=10153&idMZona[]=10154&idMZona[]=10155&idQuartiere[]=10821&idQuartiere[]=10881&idQuartiere[]=10879&idQuartiere[]=13238&idQuartiere[]=12726"
immo_roma_metro_C = "https://www.immobiliare.it/affitto-case/roma/?criterio=data&ordine=desc&prezzoMinimo=600&prezzoMassimo=1100&superficieMinima=40&idMZona[]=10150&idMZona[]=10164&idQuartiere[]=10809&idQuartiere[]=12732&idQuartiere[]=12765&idQuartiere[]=10855&idQuartiere[]=11433"
immo_zone_studentesche = "https://www.immobiliare.it/affitto-case/roma/?criterio=data&ordine=desc&prezzoMinimo=600&prezzoMassimo=1100&superficieMinima=40&idMZona[]=10150&idMZona[]=10163&idMZona[]=10148&idQuartiere[]=10809&idQuartiere[]=10806&idQuartiere[]=10851&idQuartiere[]=10847#activeImage-1580247085"

searches = [
    ImmobiliareSearch(driver, "Roma Nord - Metro A", immo_roma_nord_metro_A),
    ImmobiliareSearch(driver, "Roma Sud - Metro A", immo_roma_sud_metro_A),
    ImmobiliareSearch(driver, "Roma Ovest - Metro B", immo_roma_ovest_metro_B),
    ImmobiliareSearch(driver, "Roma Sud - Metro B", immo_roma_sud_metro_B),
    ImmobiliareSearch(driver, "Metro C", immo_roma_metro_C),
    ImmobiliareSearch(driver, "Zone Studentesche", immo_zone_studentesche)
]


async def send_notification(notifier, adv):
    await notifier.send(
        title=adv.title.title(),
        message=f"{round(adv.price)}€, Piano {round(adv.floor)}, {round(adv.size)} mq, {adv.search_name}",
        buttons=[
            Button(
                title=f"Apri {adv.website.title()}!",
                on_pressed=lambda: webbrowser.open(adv.link),
            )
        ],
        sound=DEFAULT_SOUND,
    )


def run_searches(adv_repo, searches):
    for search in searches:
        advs = search.search()
        for adv in advs:
            if adv.link not in adv_repo:
                adv_repo[adv.link] = adv
                asyncio.run(send_notification(notifier, adv))


notifier = DesktopNotifier(
    app_name="Real Estate Bot",
)


def init_repo():
    repository = dict()

    for search in searches:
        advs = search.search()
        for adv in advs:
            if adv.link not in repository:
                repository[adv.link] = adv
    return repository


if __name__ == '__main__':

    adv_repo = init_repo()

    while True:
        run_searches(adv_repo, searches)
        break

    driver.close()