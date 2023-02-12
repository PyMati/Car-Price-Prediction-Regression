import requests
import bs4
import http.client
import pandas as pd


http.client._MAXHEADERS = 1000

CAR_COLOURS = {
    "Czerwony": "Red",
    "Czarny": "Black",
    "Biały": "White",
    "Zielony": "Green",
    "Niebieski": "Blue",
    "Błękitny": "Blue",
    "Szary": "Gray",
    "Żółty": "Yellow",
    "Srebrny": "Silver",
    "Innykolor": "Else",
    "Brązowy": "Brown",
    "Bordowy": "Claret"
}
data = []
# Generate pages URL's
links = []
for index in range(0, 150):
    links.append(f"https://www.otomoto.pl/osobowe?page={index}")

def make_soup(link: str):
    """Creates bs4 object, using html parser."""
    html_doc = requests.get(link)
    soup = bs4.BeautifulSoup(html_doc.text, 'html.parser')
    return soup

def find_by_class(html_tag: str, class_name: str, soup, text = None) -> list:
    """Finds html elements using class attribute."""
    return soup.find_all(html_tag, class_ = class_name, string = text)

def find_childs(parents_array: list) -> list:
    """Finds next item after of an given element in hierarchy of html doc.  """
    childs = [child.next_element for child in parents_array]
    return childs

def extract_links(array: list) -> list:
    """Extract href's from passed html elements."""
    links = [link['href'] for link in array]
    return links

def format_data(element: str) -> str:
    """Formats text data from html attributes."""
    element = element.rstrip()
    element = element.strip('\n')
    element = element.replace(' ', "")
    return element

for link in links:
    html = requests.get(link)
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    cars = find_by_class('h2', 'e1p19lg76 e1p19lg720 ooa-10p8u4x er34gjf0', soup)
    cars = find_childs(cars)
    cars = extract_links(cars)
    print(link)
    def get_data(link: str, html_tag: str, class_name: str) -> dict:
        """Scraps data about car from site."""
        soup = make_soup(link)
        data_lists = find_by_class(html_tag, class_name, soup)
        
        # Make
        try:
            make = data_lists[0].find("span", string=["Marka pojazdu"]).find_parent().a.get_text()
            make = format_data(make)
        except AttributeError:
            make = None
        
        # Seller
        try:
            seller = data_lists[0].find("span", string=["Oferta od"]).find_parent().a.get_text()
            if format_data(seller) == "Firmy": seller = "Company"
            else: seller = "Private person"
        except AttributeError:
            seller = None

        # Year of production
        try:
            year = data_lists[0].find("span", string=["Rok produkcji"]).find_parent().div.get_text()
            year = format_data(year)
        except AttributeError:
            year = None

        # Gearbox
        try:
            gearbox = data_lists[0].find("span", string=["Skrzynia biegów"]).find_parent().div.get_text()
            if format_data(gearbox) == "Manualna": gearbox = "Manual"
            elif format_data(gearbox) == "Automatyczna": gearbox = "Automatic"
        except AttributeError:
            gearbox = None

        # Mileage
        try:
            mileage = data_lists[0].find("span", string=["Przebieg"]).find_parent().div.get_text()
            mileage = format_data(mileage).replace("km", "")
        except AttributeError:
            mileage = None
        
        # Engine Volume
        try:
            engine_volume = data_lists[0].find("span", string=["Pojemność skokowa"]).find_parent().div.get_text()
            engine_volume = format_data(engine_volume).replace("cm3", "")
        except AttributeError:
            engine_volume = None
        
        # Horsepower
        try:
            horsepower = data_lists[0].find("span", string=["Moc"]).find_parent().div.get_text()
            horsepower = format_data(horsepower).replace("KM", "")
        except AttributeError:
            horsepower = None
        
        # Fuel type
        try:
            fuel = data_lists[0].find("span", string=["Rodzaj paliwa"]).find_parent().div.get_text()
            if format_data(fuel) == "Benzyna": fuel = "Petrol"
            elif format_data(fuel) == "Elektryczny": fuel = "Electric"
            elif format_data(fuel) == "Benzyna+LPG": fuel = "Petrol+LPG"
            elif format_data(fuel) == "Hybryda": fuel = "Hybrid"
            else: fuel = format_data(fuel)
        except AttributeError:
            fuel = None

        # Colour
        try:
            color = data_lists[1].find("span", string=["Kolor"]).find_parent().a.get_text()
            color = format_data(color)
            color = CAR_COLOURS.get(color, "Else")
        except AttributeError:
            color = None

        # Fuel usage in city
        try:
            fuel_usage = data_lists[1].find("span", string=["Spalanie W Mieście"]).find_parent().div.get_text()
            fuel_usage = format_data(fuel_usage).replace('l/100km', '')
        except AttributeError:
            fuel_usage = None

        # Info about accidents
        try:
            accident = data_lists[1].find("span", string=["Bezwypadkowy"]).find_parent().div.get_text()
            if format_data(accident) == "Tak": accident = 0
            else: accident = 1
        except AttributeError:
            accident = None

        # Info about number of doors
        try:
            doors_number = data_lists[1].find("span", string=["Liczba drzwi"]).find_parent().div.get_text()
            doors_number = format_data(doors_number)
        except AttributeError:
            doors_number = None

        # Info about number of seats
        try:
            seats_number = data_lists[1].find("span", string=["Liczba miejsc"]).find_parent().div.get_text()
            seats_number = format_data(seats_number)
        except AttributeError:
            seats_number = None

        # Price
        price = find_by_class("span", "offer-price__number", soup)
        try:
            try:
                price = float(format_data(price[0].get_text().replace("PLN", ''))) / 4.43
            except ValueError:
                price = float(format_data(price[0].get_text().replace("EUR", '')))
        except ValueError:
            pass
        
        return {
            "Make": make,
            "Seller": seller,
            "YearOfProd": year,
            "Mileage (km)": mileage,
            "Color": color,
            "Fuel": fuel,
            "FuelCinCity": fuel_usage,
            "Gearbox": gearbox,
            "EngineVol (cm3)": engine_volume,
            "Horsepower": horsepower,
            "Post-accident": accident,
            "Seats": seats_number,
            "Doors": doors_number,
            "Price": round(price, 2),
        }

    # print(get_data(cars[0], 'ul', 'offer-params__list').values())
    for car in cars:
        data.append(get_data(car, 'ul', 'offer-params__list').values())


df = pd.DataFrame(data, columns=["Make", "Seller", "YearOfProd", "Mileage (km)", "Color", "Fuel", "FuelCinCity",
                                     "Gearbox", "EngineVol (cm3)", "Horsepower", "Post-accident", "Seats", "Doors", "Price"])
print(df)
df.to_csv("dane.csv")