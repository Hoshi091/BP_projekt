# Ako spustiť aplikáciu? [sk]
Tu sú niektoré kroky, ktoré je potrebné podniknúť, aby sa zabezpečilo, že aplikácia funguje správne a plne využíva svoj potenciál.
## Krok 1: Inštalácia všetkých prvkov
- Inštalácia Pythonu: Stiahnite a nainštalujte Python zo [oficiálnej webovej stránky Pythonu](https://www.python.org/downloads/) podľa vášho operačného systému.
- Inštalácia knižníc: Prejdite do adresára obsahujúceho projektové súbory pomocou príkazového riadka alebo terminálu. Potom použite nasledujúci príkaz: ```pip install -r requirements.txt``` na inštaláciu potrebných knižníc.
## Krok 2: Spustenie aplikácie
- Prejdite do adresára obsahujúceho projektové súbory cez príkazový riadok alebo terminál.
- Pustite aplikáciu Flask pomocou nasledujúceho príkazu: ```python app.py``` Tento príkaz spustí server Flask a mal by sa zobraziť oznam o tom, že server beží.
- Otvorte webový prehliadač a prejdite na nasledujúcu adresu URL: ```http://localhost:5000/``` alebo alternatívne: ```http://127.0.0.1:5000/```. Tieto adresy URL vás presmerujú na domovskú stránku aplikácie.
## Krok 3: Používanie aplikácie
Po spustení aplikácie môžete teraz využívať rôzne funkcie, ktoré aplikácia poskytuje. Tu je stručný prehľad:

**Vstupný formulár:** Na domovskej stránke uvidíte vstupný formulár, kde môžete zadať URL adresu, vybrať typy obsahu, špecifikovať vyhľadávané slovo a ďalšie možnosti.

**Odoslanie formulára:** Po vyplnení formulára stlačíte tlačidlo pre jeho odoslanie.

**Zobrazenie výsledkov:** Aplikácia spracuje vstup a zobrazí výsledky na tej istej stránke. Získaný obsah sa zobrazí pod formulárom s možnosťou uloženia textu.

## Krok 4: Ukončenie aplikácie
Pre zastavenie vývojového servera Flask a ukončenie aplikácie môžete stlačiť Ctrl + C v príkazovom riadku alebo termináli, kde server beží, a tak ukončiť server.

# How to start the application? [en]
Here are some steps that one needs to take to ensure that the application works properly and to its full extent.
## Step 1: Installing all dependencies
- Install Python: Download and install Python from the official [Python website](https://www.python.org/downloads/) based on your operating system. 
- Install Dependencies: Navigate to the directory containing the project files using the command line or terminal. Then use the following command: ``` pip install -r requirements.txt ``` to install the required dependencies.
## Step 2: Starting the Flask application
- Navigate to the directory containing the project files in the command line or terminal.
- Run the Flask application using the following command: ``` python app.py ``` This command will start the Flask server and you should see an indication that the server is running.
- Open a web browser and navigate to the following URL: ```http://localhost:5000/``` or alternatively: ```http://127.0.0.1:5000/```. Either of these URLs will take you to the application's Homepage.
## Step 3: Using the application
Once you have opened the Flask web application in your web browser, you can use it to perform various tasks. Here's a brief overview of how to use the application:

**Input Form:** On the home page, you will see an input form where you can enter a URL, select content types, specify keywords, and other options.

**Submit Form:** After entering the required and optional information, click on the submit button to submit the form.

**View Results:** The application will process your input and display the results on the same page. You can view the extracted content below with the option to save the results or try scraping again.
## Step 4: Exiting the application
To stop the Flask development server and exit the application, you can press Ctrl + C in the command line or terminal where the server is running to stop the server.
