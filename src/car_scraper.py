import time
from joblib import Parallel, delayed
import pandas as pd
import validators
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def write_data(cars_in_page):
    """
    Input / Output Operations writing in data.csv.
    :param cars_in_page: list(cars)
    :return: void

    """
    # I/O Section
    df = pd.DataFrame.from_records(
        [elem.to_dict() for elem in cars_in_page])
    with open("./csv/data.csv", 'a', encoding='utf-8-sig') as f:
        df.to_csv(f, header=False, index=False, line_terminator='\n')
        f.close()


class Car:
    # Class car, each object will have the following attributes
    def __init__(self, update=None, model=None, class_=None, price=None,
                 cant_km=None, fuel=None, cv=None, location=None, year=None):
        self.update = str(update)
        self.model = str(model)
        self.class_ = str(class_)
        self.price = str(price)
        self.cant_km = str(cant_km)
        self.fuel = str(fuel)
        self.cv = str(cv)
        self.location = str(location)
        self.year = str(year)

    def to_dict(self):
        """
        Create a dict from the car object.

        :return: dict with the car attributes
        """
        return {
            'update': self.update,
            'model': self.model,
            'class_': self.class_,
            'price': self.price,
            'cant_km': self.cant_km,
            'fuel': self.fuel,
            'cv': self.cv,
            'location': self.location,
            'year': self.year
        }


class CarsScraper:

    def __init__(self, url):
        self.url = url
        self.user_agent = 'Chrome/86.0.4240.111'
        self.headers = {'User-Agent': self.user_agent
                        }
        self.km0 = 'Km 0'
        self.used = 'Segunda mano '
        self.driver_path = './drivers/chromedriver.exe'

    def din_scraper(self, url):

        """
        Return the browser Chrome driver.

        :param url: string
        :return:  chromedriver
        """

        # Setting the options for the driver.
        opts = Options()
        opts.add_argument(self.user_agent)

        browser = webdriver.Chrome(self.driver_path, options=opts)

        try:
            browser.get(url)
            time.sleep(4)

            # Explicit selenium waiting and,
            # clicking the cookies button in main windows.
            cookies_button = WebDriverWait(browser,
                                           20).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="CybotCookiebotDialogBodyButtonAccept"]')))

            cookies_button.click()

        except:
            print("Error in link : {}".format(url))
            return browser

        return browser

    def get_links(self, browser):

        """
        Get the KM0 and Used Cars links from central menu in the index page.

        :param browser: chromedriver
        :return: links: list(string)
        """
        links = []
        try:
            # Get the central menu element
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "#header > div.header__central-menu.script__header-central-menu"))
            )

            # Get the link finding by element properties.
            link_KM0 = element.find_element_by_link_text(self.km0)
            link_Sec = element.find_element_by_link_text("Segunda mano")

            links.append(link_KM0.get_attribute('href'))
            links.append(link_Sec.get_attribute('href'))

        except:
            print("Error in get_links function")
        return links

    def brands_links(self, link, car_class):

        """
        Get  the links for every brand, for each class, KM0 and
        User Cars.

        :param link: string
        :param car_class: string
        :return: list(string)
        """
        links_brands = []

        cl_name = "row.cc_makes "

        browser = self.din_scraper(link)

        try:
            # Get element finding by class name.
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, cl_name)
                                               )
            )
            # Get the div container for all 'a' elements.
            a_sect = element.find_elements_by_tag_name('a')

            # Get the url variable from each 'a' element.
            for a in a_sect:
                try:
                    # Validator for 'url' format.
                    if validators.url(a.get_attribute('href')):
                        links_brands.append(a.get_attribute('href'))
                except:
                    pass
        finally:
            pass

        browser.quit()
        return links_brands

    def get_all_navegation(self, link, car_class):
        """
        Main functionality method, get all cars for every page navigating
        over the page. Accept the cookies button, and click the next button.

        :param link: string
        :param car_class: string
        :return: void
        """

        cl_name = "pillList"

        browser = self.din_scraper(link)

        while True:
            try:
                cars_in_page = []

                # Get the element that contains all cars.
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, cl_name)
                                                   )
                )

                # Get tall the containers individually.
                a_sect = element.find_elements_by_css_selector(
                    "div[class^='pill "
                    "pill--vo-km0 "
                    "script__pill car-']")

                # Get tha values for each car.
                for a in a_sect:
                    car = Car()
                    if a.find_element_by_class_name(
                            "make-model-version").text != '':
                        car.update = " ".join(a.find_element_by_class_name(
                            "update").text.split()[1:])
                        car.model = a.find_element_by_class_name(
                            "make-model-version").text
                        car.class_ = car_class
                        car.price = a.find_element_by_class_name("price").\
                            text.split()[0]
                        car.cant_km = a.find_element_by_class_name("km").\
                            text.split()[0]
                        car.fuel = a.find_element_by_class_name("gas").text
                        car.cv = a.find_element_by_class_name("cv")\
                            .text.split()[0]
                        car.location = a.find_element_by_class_name(
                            "location").text
                        car.year = a.find_element_by_class_name(
                            "year").text
                        cars_in_page.append(car)

                # I/O Operations.
                try:
                    write_data(cars_in_page)

                except Exception as e:
                    print("Error in I/O Operations. {}.".format(e))

                # Navigate to next page.
                try:
                    next_button = WebDriverWait(browser, 0).until(
                        EC.presence_of_element_located(
                            (By.LINK_TEXT, 'Siguiente')))

                    next_button.click()
                except:
                    browser.quit()
                    break

                # Looking fro next button, if not appear break the sentence.
                try:
                    off_butt = WebDriverWait(browser, 0).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR, '#yw0 > li.pager-next.pager'
                                             '-next--off')))

                    browser.quit()
                    break
                except NoSuchElementException:
                    pass

            except:
                pass


def main():
    # Starting the timer.
    start = time.perf_counter()

    car = Car("last_update", "model", "class", "price", "km", "fuel",
              "cv", "location", "year")

    cars = CarsScraper('https://www.coches.com')
    driver = cars.din_scraper(cars.url)

    # Get Links of classes [Km 0, Used Hand].
    links = cars.get_links(driver)

    # Close the useless driver.
    driver.close()

    # Get links of each brand from each class.
    links_km0 = cars.brands_links(links[0], cars.km0)
    links_sec = cars.brands_links(links[1], cars.used)

    # Writing csv header.
    write_data([car])

    try:
        # Launch the parallel workers for get the km 0 cars.
        Parallel(n_jobs=4)(delayed(
            cars.get_all_navegation)(url, cars.km0) for url in links_km0)

        # Launch the parallel workers for get the used cars.
        Parallel(n_jobs=4)(delayed(
            cars.get_all_navegation)(url, cars.used) for url in links_sec)

        # Ending the timer.
        end = time.perf_counter()

        print("Time elapsed : {} minutes".format((end - start) / 60))

    except Exception as e:
        print("Error in main function. Error : {}".format(e))


main()
