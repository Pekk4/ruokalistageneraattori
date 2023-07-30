[![CI](https://github.com/Pekk4/ruokalistageneraattori/actions/workflows/CI.yml/badge.svg?branch=master)](https://github.com/Pekk4/ruokalistageneraattori/actions/workflows/CI.yml)

# Ruokalistageneraattori

Sovelluksen avulla käyttäjät voivat generoida itselleen valmiita ruokalistoja helpottamaan arjen ateriasuunnittelua.

Sovellus on toteutettu Helsingin Yliopiston Tietojenkäsittelytieteen aineopintojen harjoitustyönä vuosien 2022 ja 2023 aikana.
Idea sovellukseen on syntynyt, kun ainainen ruokien miettiminen on alkanut tympimään. Sovellus siis koittaa ratkaista olemassaolevaa arjen ongelmaa.

Sovellusta voi testata tuotannossa osoitteessa: [https://ruokalistat.prokkinen.fi](https://ruokalistat.prokkinen.fi).

## Käyttötapaukset

Sovelluksessa on normaalitason käyttäjiä, sekä vähintään yksi ylläpitäjä.

Normaalitason käyttäjä voi luoda itselleen tunnuksen sovellukseen ja lisätä tämän jälkeen ruokalajeja kirjastoonsa, generoida niistä ruokalistoja kuluvalle viikolle, sekä generoida ostoslistan kuluvan viikon ruokalistan raaka-aineista. Lisäksi normaali käyttäjä voi tarkastella edellisten viikkojen ruokalistoja ja asettaa niitä uudelleen käyttöönsä kuluvalle viikolle. Normaali käyttäjä voi myöskin arpoa tai valita yksittäisten päivien ruokia joko heti kirjauduttuaan sisään, jossa on mahdollista arpoa kuluvan päivän ruoan tilalle uusi ruoka, tai sitten ruokalistan muokkasnäkymästä, jossa on mahdollista muokata kuluvan viikon ruokalistaa. Käyttäjä voi myös lisätä, poistaa tai uudelleennimetä raaka-aineita, tai vaihdella niiden määriä ja määrien yksikköjä. Ruokalajeja voi myös poistaa. Käyttäjä voi myös lukea ylläpidon kirjoittamia uutisia.

Ylläpitäjä voi edellä mainittujen toimien lisäksi resetoida käyttäjien unohtamia salasanoja, tarkastella sovelluksen tietokanta-lokia ja lukea sekä kirjoittaa uutisia sovelluksen tilanteesta. Ylläpitäjät tunnistetaan `users`-tietokantataulun `is_admin`-sarakkeen avulla.

## Arkkitehtuuri

Sovellus noudattelee TKT-kursseilta tuttua kerrosarkkitehtuuria, jossa sovelluksen toimintaa on jaettu eri kerroksille. [Repository](https://github.com/Pekk4/ruokalistageneraattori/tree/master/src/repositories)-luokat huolehtivat erilaisista tietokantaoperaatioista, [Service](https://github.com/Pekk4/ruokalistageneraattori/tree/master/src/services)-luokat puolestaan pyytävät tavaraa tietokannasta `Repository`-luokilta ja saattavat muovata sitä hieman parempaan muotoon, kunnes se lopulta [Blueprinttien](https://github.com/Pekk4/ruokalistageneraattori/tree/master/src/blueprints) tarjoamien polkujen ja rajapintojen kautta tarjoillaan käyttäjälle asti Flaskin renderöimien [sivupohjien](https://github.com/Pekk4/ruokalistageneraattori/tree/master/src/templates) mukaisesti.

### Tietoturva

Sovelluksen kehityksessä on koitettu huomioida tietoturvaa mahdollisimman hyvin. Flaskissa on käytössä mm. [CSRFProtect](https://pypi.org/project/Flask-WTF/) ja [Talisman](https://pypi.org/project/talisman/) -lisämoduulit, jotka ehkäisevät CSRF- ja XSS-hyökkäyksiä muun muassa `Content Security Policyn` ja HTTPS-pakotuksen avulla. Flaskin sivupohjat estävät myös oletuksena JavaScriptin mielivaltaisen ajamisen esimerkiksi lomakkeista tai muista kentistä.

Käyttäjien salasanat tallennetaan tietokantaan käyttämällä [Argon2-tiivistefunktiota](https://pypi.org/project/argon2-cffi/).

Käyttäjien sessiot puolestaan tarkistetaan jokaisella kutsulla sellaiseen polkuun, jonka käyttäminen vaatii sisäänkirjautumista. Mikäli esimerkiksi `User-Agent`-tiedot poikkeavat, mitätöidään sessio välittömästi.

SQL-injektioilta on suojauduttu perinteiseen tapaan käyttämällä parametrisoituja kyselyjä. Niiltä suojaisi myös ORM-toiminnallisuuksien käyttäminen jossain määrin, mutta tällä kurssilla ne eivät olleet käytettävissä.

Lisäksi virheenkäsittelyillä on pyritty varmistamaan, että sovellus ei pääse kaatumaan missään tilanteessa.

## Sovelluksen käyttäminen

### Vaatimukset

Sovelluksen käyttäminen ja kehittäminen edellyttää seuraavien pakettien olevien asennettu:

 - docker
 - make
 - npm
 - pip
 - python

Kehittämisessä on käytetty Pythonin versiota 3.9, uudemmilla versioilla toimintaa ei ole kokeiltu.

### Tuotantoversio

Sovelluksen tuotantoversion saa pyörimään luomalla ensin konfiguraation `make`n avulla:

```bash
make prod
```

Käyttäjältä kysytään, millä tiedoilla käyttäjä haluaa konfiguroida tietokannan tunnukset yms. Tuotantoversioon kysytään myös verkkotunnus, jota nginx asetetaan kuuntelemaan.

Tämän lisäksi käyttäjän tulee toimittaa verkkotunnukseen täsmäävän TLS-sertifikaatin tiedostot `certs/`-hakemistoon nimettynä seuraavasti:

```bash
certs/domain.ctr # sertifikaatti
certs/domain.key # yksityinen avain
```

Näiden toimien jälkeen tuotantoympäristön saa pyörimään komennolla:

```bash
docker compose up
```

### Kehitysversio

Kehitysversion puolestaan saa pyörimään luomalla konfiguraatiot ja tekemällä muut tarvittavat toimenpiteet:

```bash
make dev
```

Käyttäjältä kysytään tarvittavat tiedot mm. tietokannan konfigurointiin, sekä asennetaan tarvittavat riippuvuudet. Samalla asetetaan kehitystietokanta pyörimään dockeriin.

Kun kaikki on valmista, aktivoidaan virtuaaliympäristö:

```bash
source venv/bin/activate
```

ja komennetaan tämän jälkeen:

```bash
invoke start
```

Tämä käynnistää Flaskin paikallisesti porttiin `5000`. Mikäli ulkoasuun tekee muutoksia, tarvitsee aktivoida toinen virtuaaliympäristö uuteen komentorivinäkymään ja komentaa: 

```bash
invoke css-builder
```

Tämä käynnistää Tailwindcss-prosessorin, joka seurailee koodiin tulevia muutoksia ja generoi ne välittömästi tyylitiedostoon.

Linttauksen saa puolestaan ajettua komennolla:

```bash
invoke lint
```

Kehitysversioon luodaan admin-käyttäjä automaattisesti tietokantaskeeman mukana tunnuksilla `admin:admin`.

## Sovellukseen jääneitä puutteita

Ruokalajin nimeä ei voi vaihtaa muokkaustilassa, vaan ainoastaa raaka-aineita voi muuttaa. Syy toistaiseksi tuntematon.

Lisäksi käyttäjien syötteille unohtui asettaa ylärajat, jonka huomasin olevan tarkistuslistassa vasta palautuspäivänä, mutta käyttäjän tunkiessa lorem ipsumia kentät täyteen kärsii hän pääsääntöisesti vain itse siitä, sillä sovelluksessa ei ole käyttäjien välistä toimintaa ollenkaan ja esimerkiksi salasana on tiivistefunktiosta johtuen aina saman pituinen.
EDIT: ainakin näemmä rekisteröitymis-kentässä oli ylärajat pituuksille, mutta joistain kentistä taitaa puuttua...

Mikäli ruokalajia lisätessä tai muokatessa tulee virheilmoitus, täytyy sivu ladata uudestaan, tai ilmoitus tulee aina uudestaan vaikkei virhettä enää olisikaan. Aika ei riittänyt korjata tätä.

Sovelluksen lopputulos on melkoisen kokeellinen, sillä sitä kehittäessä tuli kokeiltua kaikenlaista ja näin ollen opittua paljon uutta. Sovelluksen pitkästä kehitysajasta johtuen taidot ovat kehittyneet myös muiden projektien myötä eteenpäin siten, että tämän projektin koodi ehti vanhentua pahasti projektin aikana. Valitettavasti ei ollut kuitenkaan mahdollista tehdä kaikkea uusiksi, vaikka mieli olisi kovasti tehnytkin monesti aloittaa puhtaalta pöydältä.

Projektin koodi lentääkin romukoppaan välittömästi arvioinnin jälkeen ja sovellus koodataan tulevaisuudessa täysin uusiksi, luultavasti Full Stack Open-kurssin harjoitustyönä.

## Lähteitä

Taustakuva: Pfüderi@Pixabay, https://pixabay.com/photos/ingredients-italian-cuisine-flatlay-2364182/

Ikonit: Flaticon, https://www.flaticon.com/

Lisäksi n+1 artikkelia StackOverFlowta, medium.comia yms yms. Projektin asioita googlaillessa sain viime vuonna myös Googlen [foobar](https://www.turing.com/kb/foobar-google-secret-hiring-technique)-kutsun, joka täytyisi vielä suorittaa loppuun, kunhan kiireet helpottavat.