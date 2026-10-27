# Bouwt een pagina per branche in branches/<slug>.html en het menu 'Branches' in index.html
# (draai: python3 -I scripts/maak-branches.py, daarna scripts/maak-ontwikkelaars.py voor het menu daar).
# De basis (kleuren, knoppen, navigatie, footer) komt uit index.html, zodat alles hetzelfde oogt.
# Alleen wat Botlu echt kan: vragen beantwoorden uit je website, afspraken inplannen en verzetten,
# terugbelverzoeken noteren, meldingen, opnames en vijf talen. Doorverbinden en sms staan op 'binnenkort'.
import html, pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent

# Iconen: gewoon zwart, zonder vlak (stijlregel van Daniel)
ICON = {
  'medisch': '<path d="M5 3v5a4 4 0 0 0 8 0V3"/><path d="M9 12v3a5 5 0 0 0 10 0v-2"/><circle cx="19" cy="11" r="2"/>',
  'hotel': '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h.01M12 7h.01M15 7h.01M9 11h.01M12 11h.01M15 11h.01M10 21v-4h4v4"/>',
  'hamer': '<path d="M13 7 4.5 15.5a2.1 2.1 0 0 0 3 3L16 10"/><path d="m11 5 3-2 7 7-2 3z"/>',
  'weegschaal': '<path d="M12 3v18M7 21h10M5 7h14"/><path d="M5 7 2.5 13a2.5 2.5 0 0 0 5 0zM19 7l-2.5 6a2.5 2.5 0 0 0 5 0z"/>',
  'persoon': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
  'gebouwen': '<path d="M3 21h18M5 21V8l6-4v17M11 21V10l8 3v8"/><path d="M8 10h.01M8 14h.01M15 15h.01M15 18h.01"/>',
  'kantoor': '<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2"/>',
  'auto': '<path d="M4 15l1.5-5A2 2 0 0 1 7.4 8.5h9.2a2 2 0 0 1 1.9 1.5L20 15v3H4z"/><circle cx="7.5" cy="18" r="1.5"/><circle cx="16.5" cy="18" r="1.5"/>',
  'overheid': '<path d="M3 21h18M4 10h16M12 3l8 5H4z"/><path d="M6 10v8M10 10v8M14 10v8M18 10v8"/>',
  'sleutelgereedschap': '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
  'groep': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6.5 6.5 0 0 1 3.5 6"/>',
  'lach': '<circle cx="12" cy="12" r="9"/><path d="M8 14a4.5 4.5 0 0 0 8 0M9 9.5h.01M15 9.5h.01"/>',
  'hartslag': '<path d="M20.8 6.6a5 5 0 0 0-8.8-1.5 5 5 0 0 0-8.8 1.5C2 11 7 15.5 12 20c5-4.5 10-9 8.8-13.4z"/><path d="M3.5 12h5l1.5-3 2.5 6 1.5-3h6"/>',
  'stempel': '<path d="M5 21h14M6 17h12v-3a2 2 0 0 0-2-2h-1.5l-.5-3a2.5 2.5 0 1 0-4 0l-.5 3H8a2 2 0 0 0-2 2z"/>',
  'winkel': '<path d="M4 10v10h16V10M3 6l2-3h14l2 3v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0z"/><path d="M10 20v-5h4v5"/>',
  'tas': '<path d="M6 7h12l1 13H5z"/><path d="M9 7a3 3 0 0 1 6 0"/>',
  'rekenmachine': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 18h.01M12 18h.01M16 18h.01"/>',
  'pil': '<rect x="2.5" y="8.5" width="19" height="7" rx="3.5" transform="rotate(-45 12 12)"/><path d="m8.5 8.5 7 7"/>',
  'sleutel': '<circle cx="8" cy="15" r="4"/><path d="M10.8 12.2 19 4M16 7l2 2M14 9l2 2"/>',
  'bestek': '<path d="M7 3v8M5 3v4a2 2 0 0 0 4 0V3M7 11v10M17 3c-2 1-3 3-3 6v4h3v8"/>',
  'zoekpersoon': '<circle cx="10" cy="8" r="4"/><path d="M3 20a7 7 0 0 1 9.5-6.5"/><circle cx="17" cy="17" r="3"/><path d="m21 21-1.8-1.8"/>',
  # voor de kaarten met taken
  'agenda': '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
  'terugbel': '<path d="M6.6 3.5h2.6l1.6 4-2 1.3a11 11 0 0 0 5.4 5.4l1.3-2 4 1.6v2.6a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z"/><path d="M15 3.5h5.5V9M20.5 3.5 14 10"/>',
  'kennis': '<path d="M5 4.5h10a3 3 0 0 1 3 3v12H8a3 3 0 0 1-3-3z"/><path d="M5 16.5a3 3 0 0 1 3-3h10"/>',
  'melding': '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>',
  'taal': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.7 5.6 3.7 9s-1.2 6.4-3.7 9c-2.5-2.6-3.7-5.6-3.7-9S9.5 5.6 12 3z"/>',
  'opname': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/>',
  'nacht': '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
}
def icon(n, cls=''): return f'<svg{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[n]}</svg>'

# slug, naam in het menu, icoon, 'voor …', 'je …' (de zaak), kop, kop (zacht), intro,
# voorbeeldgesprek (bedrijf, vraag, antwoord, uitkomst), drie taken (icoon, titel, tekst), zes vragen
B = [
 ('medische-praktijk', 'Medische praktijk', 'medisch', 'medische praktijken', 'praktijk',
  'Je praktijk bereikbaar,', 'ook als de lijn bezet is.',
  'Botlu neemt op als je assistentes het druk hebben. Hij plant afspraken in, beantwoordt vragen over je praktijk en noteert wie teruggebeld wil worden.',
  ('Huisartsenpraktijk De Linde', 'Kan ik deze week nog terecht voor een controle?', 'Donderdag om 9:40 is er nog plek. Zal ik die voor je vastzetten?', 'Afspraak'),
  [('agenda', 'Afspraken inplannen', 'Hij kijkt welke tijden vrij zijn en zet de afspraak meteen vast.'),
   ('terugbel', 'Terugbelverzoeken', 'Vragen voor de huisarts of assistente noteert hij met naam en nummer.'),
   ('kennis', 'Jij bepaalt wat hij zegt bij spoed', 'Bijvoorbeeld je spoednummer of de huisartsenpost.')],
  ['Wat zijn jullie openingstijden?', 'Kan ik een afspraak maken bij de huisarts?', 'Hoe vraag ik een herhaalrecept aan?', 'Ik wil mijn afspraak van morgen afzeggen.', 'Nemen jullie nieuwe patiënten aan?', 'Kan de assistente mij terugbellen?']),
 ('hotels', 'Hotels', 'hotel', 'hotels', 'hotel',
  'Elke gast geholpen,', 'ook midden in de nacht.',
  'Gasten bellen over kamers, parkeren, ontbijt en inchecken. Botlu antwoordt meteen, in vijf talen, en noteert wie een reservering wil.',
  ('Hotel Aan de Gracht', 'Hoe laat kan ik morgen inchecken?', 'Inchecken kan vanaf 15:00. Kom je eerder, dan bewaren we je bagage graag.', 'Opgelost'),
  [('taal', 'Spreekt de taal van je gast', 'Nederlands, Engels, Duits, Frans en Spaans.'),
   ('kennis', 'Weet alles van je hotel', 'Ontbijt, parkeren, huisdieren en annuleren: uit je eigen website.'),
   ('terugbel', 'Reserveringen doorgegeven', 'Wie wil boeken, staat meteen klaar voor je receptie.')],
  ['Hebben jullie dit weekend nog een kamer?', 'Is het ontbijt inbegrepen?', 'Kan ik bij jullie parkeren?', 'Mag mijn hond mee?', 'Tot wanneer kan ik gratis annuleren?', 'Hoe kom ik vanaf het station bij jullie?']),
 ('vakmensen', 'Vakmensen', 'hamer', 'vakmensen', 'bedrijf',
  'Jij op de steiger,', 'Botlu aan de telefoon.',
  'Geen gemiste klussen meer omdat je handen vol zitten. Botlu neemt op, vraagt door wat er moet gebeuren en plant een afspraak of zet een terugbelverzoek klaar.',
  ('Schildersbedrijf Bakker', 'Kunnen jullie volgende week onze kozijnen schilderen?', 'Dat noteer ik. Om hoeveel kozijnen gaat het ongeveer? Dan belt Kees je vandaag terug.', 'Terugbellen'),
  [('terugbel', 'Klusaanvragen op een rij', 'Wie, waar, wat en hoe dringend, in één samenvatting.'),
   ('agenda', 'Afspraken voor een opname', 'Hij plant een bezoek in op momenten dat jij kunt.'),
   ('melding', 'Meteen een seintje', 'Een melding of e-mail na elk gesprek, zodat je snel reageert.')],
  ['Kunnen jullie een offerte maken?', 'Wanneer hebben jullie tijd?', 'Werken jullie ook in mijn regio?', 'Mijn kraan lekt, kan er vandaag iemand komen?', 'Wat kost het voorrijden?', 'Kan ik foto’s van de klus sturen?']),
 ('advocatenkantoren', 'Advocatenkantoren', 'weegschaal', 'advocatenkantoren', 'kantoor',
  'Elke cliënt netjes te woord,', 'ook buiten kantoortijd.',
  'Botlu neemt op voor je kantoor, noteert waar een nieuwe zaak over gaat en plant een kennismaking in. Jij leest de samenvatting en beslist.',
  ('Van Leeuwen Advocaten', 'Ik heb een vraag over mijn ontslag. Kan ik een afspraak maken?', 'Dat kan. Donderdag om 14:00 is er een kennismakingsgesprek vrij. Zal ik het vastzetten?', 'Afspraak'),
  [('kennis', 'Intake op een rij', 'Naam, rechtsgebied en een korte omschrijving, voordat je terugbelt.'),
   ('agenda', 'Kennismakingen ingepland', 'Direct in je agenda, op tijden die jij vrijgeeft.'),
   ('opname', 'Jij bepaalt wat er wordt opgenomen', 'Opnemen zet je per assistent aan of uit.')],
  ['Doen jullie ook arbeidsrecht?', 'Wat kost een eerste gesprek?', 'Kan mijn advocaat mij terugbellen?', 'Ik wil mijn afspraak verzetten.', 'Werken jullie op toevoeging?', 'Waar zitten jullie precies?']),
 ('zelfstandigen', 'Zelfstandigen', 'persoon', 'zelfstandigen', 'bedrijf',
  'Jij werkt,', 'Botlu neemt op.',
  'Als zzp’er kun je niet altijd opnemen. Botlu doet het voor je, in jouw naam, en stuurt je na elk gesprek een korte samenvatting.',
  ('Fotograaf Lisa de Wit', 'Ben je nog vrij voor een shoot op 14 juni?', 'Lisa heeft die middag nog ruimte. Zal ik vragen of ze je vandaag terugbelt?', 'Terugbellen'),
  [('melding', 'Samenvatting op je telefoon', 'Per e-mail, Slack of Discord, zodat je weet wie je moet terugbellen.'),
   ('agenda', 'Afspraken zonder heen-en-weer', 'Hij biedt vrije tijden uit je agenda aan.'),
   ('nacht', 'Altijd bereikbaar', 'Ook als je bij een klant bent of op vakantie.')],
  ['Wat zijn je tarieven?', 'Ben je volgende week beschikbaar?', 'Kan ik een kennismaking plannen?', 'Werk je ook op locatie?', 'Hoe lang duurt een opdracht meestal?', 'Kun je me terugbellen?']),
 ('vastgoedbeheer', 'Vastgoedbeheer', 'gebouwen', 'vastgoedbeheerders', 'organisatie',
  'Huurders geholpen,', 'ook bij een lekkage om middernacht.',
  'Botlu neemt meldingen aan, vraagt door wat er aan de hand is en zet alles klaar voor je monteur. Bij spoed geeft hij het nummer dat jij instelt.',
  ('Woonbeheer Oost', 'Er lekt water door het plafond in de badkamer.', 'Vervelend! Ik noteer je adres en de melding. Een monteur belt je zo snel mogelijk terug.', 'Terugbellen'),
  [('terugbel', 'Storingen genoteerd', 'Adres, wat er mis is en hoe dringend, in één melding.'),
   ('melding', 'Meteen bij de juiste persoon', 'Via Slack, Teams of e-mail, zodat er snel iemand op afgaat.'),
   ('kennis', 'Vragen over huur en onderhoud', 'Huur betalen, onderhoud en opzeggen: uit je eigen informatie.')],
  ['Mijn cv-ketel doet het niet.', 'Wanneer komt de monteur?', 'Hoe zeg ik mijn huur op?', 'Wie betaalt dit onderhoud?', 'Ik ben mijn sleutel kwijt, wat nu?', 'Hebben jullie woningen vrij?']),
 ('bedrijven', 'Bedrijven', 'kantoor', 'bedrijven', 'bedrijf',
  'Je receptie,', 'altijd bezet.',
  'Botlu neemt op voor je bedrijf, beantwoordt veelgestelde vragen en zorgt dat elk bericht bij de juiste collega terechtkomt.',
  ('Jansen Logistiek', 'Ik wil iemand spreken over een offerte.', 'Ik noteer je vraag en je nummer. Een collega van sales belt je vandaag nog terug.', 'Terugbellen'),
  [('kennis', 'Veelgestelde vragen', 'Openingstijden, adres en levertijden: hij weet het van je website.'),
   ('terugbel', 'Berichten voor collega’s', 'Wie belde, waarover en voor wie, in één overzicht.'),
   ('melding', 'In je eigen systemen', 'Meldingen in Slack of Teams, of via webhooks en de API.')],
  ['Met wie spreek ik over een offerte?', 'Wat zijn jullie openingstijden?', 'Hebben jullie vacatures?', 'Ik wil een factuur bespreken.', 'Waar kan ik een pakket afleveren?', 'Kan iemand mij terugbellen?']),
 ('autodealers', 'Autodealers', 'auto', 'autodealers', 'showroom',
  'Elke proefrit ingepland,', 'ook op zondag.',
  'Botlu beantwoordt vragen over je aanbod, plant proefritten in en noteert wie interesse heeft, zodat je verkoper gericht kan terugbellen.',
  ('Autobedrijf Visser', 'Staat de blauwe Golf uit jullie advertentie er nog?', 'Dat laat ik een verkoper voor je nakijken. Zal ik alvast een proefrit voor zaterdag inplannen?', 'Afspraak'),
  [('agenda', 'Proefritten inplannen', 'Direct in de agenda van je showroom.'),
   ('terugbel', 'Warme leads', 'Welke auto, inruil en budget: je verkoper weet het voordat hij belt.'),
   ('kennis', 'Financiering en garantie', 'Hij haalt het antwoord van je eigen website.')],
  ['Kan ik een proefrit maken?', 'Nemen jullie mijn auto in?', 'Kan ik de auto financieren?', 'Hoeveel garantie krijg ik?', 'Tot hoe laat is de showroom open?', 'Is deze auto nog beschikbaar?']),
 ('overheidsinstanties', 'Overheidsinstanties', 'overheid', 'overheidsinstanties', 'organisatie',
  'Inwoners snel geholpen,', 'zonder wachtrij.',
  'Botlu beantwoordt de vragen die elke dag terugkomen en plant afspraken in. Voor de rest noteert hij een terugbelverzoek voor de juiste afdeling.',
  ('Gemeente Voorbeeld', 'Hoe vraag ik een nieuw paspoort aan?', 'Dat kan op afspraak. Dinsdag om 10:15 is er plek bij de balie. Zal ik die voor je vastzetten?', 'Afspraak'),
  [('kennis', 'De vragen die altijd terugkomen', 'Openingstijden, afval, parkeren en documenten, uit jullie eigen informatie.'),
   ('agenda', 'Afspraken aan de balie', 'Direct ingepland op vrije tijden.'),
   ('taal', 'In meerdere talen', 'Nederlands, Engels, Duits, Frans en Spaans.')],
  ['Hoe vraag ik een paspoort aan?', 'Wanneer wordt het grofvuil opgehaald?', 'Hoe krijg ik een parkeervergunning?', 'Waar kan ik een melding doen?', 'Wanneer is het gemeentehuis open?', 'Wie helpt mij met mijn aanvraag?']),
 ('autogarages', 'Autogarages', 'sleutelgereedschap', 'autogarages', 'garage',
  'Werkplaats vol,', 'telefoon toch opgenomen.',
  'Botlu plant APK’s en onderhoudsbeurten in, beantwoordt vragen over prijzen en noteert wie wil weten of zijn auto klaar is.',
  ('Garage De Vries', 'Wanneer kan mijn auto de APK in?', 'Donderdag om 8:00 kan hij binnen. Zal ik dat voor je inplannen?', 'Afspraak'),
  [('agenda', 'APK en onderhoud ingepland', 'Op de tijden die jouw werkplaats aankan.'),
   ('kennis', 'Prijzen en openingstijden', 'Uit je eigen website, ook als je monteurs onder een auto liggen.'),
   ('terugbel', 'Is mijn auto klaar?', 'Hij noteert de vraag, zodat jij terugbelt zodra het zover is.')],
  ['Wat kost een kleine beurt?', 'Kan ik een vervangende auto krijgen?', 'Wanneer is mijn auto klaar?', 'Doen jullie ook bandenwissels?', 'Er brandt een lampje, kan ik langskomen?', 'Tot hoe laat zijn jullie open?']),
 ('verenigingen', 'Verenigingen', 'groep', 'verenigingen', 'vereniging',
  'Vrijwilligers ontlast,', 'leden altijd geholpen.',
  'Botlu beantwoordt vragen over lidmaatschap, trainingen en contributie, zodat je vrijwilligers niet de hele dag hoeven op te nemen.',
  ('Tennisvereniging De Kaats', 'Kan mijn dochter een proefles komen doen?', 'Zeker! Woensdag om 16:00 is er een jeugdtraining. Zal ik haar aanmelden?', 'Afspraak'),
  [('kennis', 'Lid worden en contributie', 'Uit je eigen website, altijd actueel.'),
   ('agenda', 'Proeflessen en kennismaking', 'Direct ingepland.'),
   ('melding', 'Berichten voor het bestuur', 'Per e-mail of in je eigen Slack- of Discord-kanaal.')],
  ['Hoe word ik lid?', 'Wat kost het lidmaatschap?', 'Wanneer zijn de trainingen?', 'Kan ik een proefles doen?', 'Hoe zeg ik mijn lidmaatschap op?', 'Met wie praat ik over sponsoring?']),
 ('tandartsen', 'Tandartsen', 'lach', 'tandartsen', 'praktijk',
  'Je balie ontlast,', 'je stoel gevuld.',
  'Botlu plant controles in, verzet afspraken en beantwoordt vragen over vergoedingen. Bij pijn biedt hij de spoedplekken aan die jij vrijhoudt.',
  ('Tandartspraktijk Lindeboom', 'Ik heb kiespijn, kan ik vandaag nog komen?', 'Om 16:40 is er een spoedplek. Zal ik die voor je vastzetten?', 'Afspraak'),
  [('agenda', 'Controles en verzetten', 'Afspraken maken, verzetten of annuleren, ook ’s avonds.'),
   ('kennis', 'Vragen over vergoedingen', 'Wat de verzekering dekt, uit je eigen informatie.'),
   ('terugbel', 'Spoed op tijd gezien', 'Jij bepaalt welke spoedplekken hij mag aanbieden.')],
  ['Kan ik een controle inplannen?', 'Ik wil mijn afspraak verzetten.', 'Nemen jullie nieuwe patiënten aan?', 'Wordt dit vergoed?', 'Ik heb kiespijn, wat nu?', 'Hoe laat zijn jullie open?']),
 ('fysiotherapeuten', 'Fysiotherapeuten', 'hartslag', 'fysiotherapeuten', 'praktijk',
  'Meer tijd voor je patiënten,', 'minder aan de telefoon.',
  'Botlu plant behandelingen in, verzet afspraken en beantwoordt vragen over verwijzingen en vergoedingen.',
  ('Fysio Centrum Zuid', 'Kan ik mijn afspraak van dinsdag verzetten?', 'Natuurlijk. Past donderdag om 9:30 of om 15:00 beter?', 'Afspraak'),
  [('agenda', 'Behandelingen ingepland', 'Maken, verzetten en annuleren, direct in je agenda.'),
   ('kennis', 'Verwijzing en vergoeding', 'Heb ik een verwijzing nodig? Wat wordt vergoed? Hij weet het.'),
   ('terugbel', 'Vragen voor je therapeut', 'Netjes genoteerd, met naam en nummer.')],
  ['Heb ik een verwijzing nodig?', 'Hoeveel behandelingen worden vergoed?', 'Kan ik vandaag nog terecht?', 'Ik wil mijn afspraak verzetten.', 'Doen jullie ook sportfysiotherapie?', 'Waar kan ik parkeren?']),
 ('notarissen', 'Notarissen', 'stempel', 'notarissen', 'kantoor',
  'Je kantoor bereikbaar,', 'je agenda goed gevuld.',
  'Botlu beantwoordt vragen over testamenten, huizenkoop en tarieven, en plant een kennismaking of ondertekening in.',
  ('Notariskantoor Smit', 'Wat kost het om een testament op te laten stellen?', 'Dat hangt af van je situatie. Zal ik een vrijblijvend kennismakingsgesprek voor je plannen?', 'Afspraak'),
  [('kennis', 'Tarieven en werkwijze', 'Uit je eigen website, helder uitgelegd.'),
   ('agenda', 'Afspraken voor ondertekening', 'Direct in je agenda.'),
   ('terugbel', 'Vragen voor de notaris', 'Met naam, nummer en waar het over gaat.')],
  ['Wat kost een testament?', 'Kunnen jullie de levering van mijn huis doen?', 'Wat moet ik meenemen?', 'Kan ik een volmacht laten opstellen?', 'Wanneer kan ik komen tekenen?', 'Kan de notaris mij terugbellen?']),
 ('winkels', 'Winkels', 'winkel', 'winkels', 'winkel',
  'Klanten geholpen,', 'terwijl jij achter de kassa staat.',
  'Botlu beantwoordt vragen over openingstijden, voorraad en service, en noteert wat je zelf moet uitzoeken.',
  ('Fietsenwinkel Van Dijk', 'Tot hoe laat zijn jullie vandaag open?', 'Vandaag zijn we open tot 18:00. Kom je voor een reparatie? Dan plan ik meteen een afspraak.', 'Opgelost'),
  [('kennis', 'Openingstijden en service', 'Altijd het goede antwoord, uit je eigen website.'),
   ('agenda', 'Afspraken voor reparatie of advies', 'Op de momenten dat jij tijd hebt.'),
   ('terugbel', 'Is het op voorraad?', 'Wat hij niet zeker weet, noteert hij voor je.')],
  ['Tot hoe laat zijn jullie open?', 'Hebben jullie dit op voorraad?', 'Kan ik iets reserveren?', 'Kan ik mijn aankoop ruilen?', 'Waar kan ik parkeren?', 'Doen jullie ook reparaties?']),
 ('retail', 'Retail', 'tas', 'retailers', 'winkels',
  'Klantenservice die nooit sluit,', 'voor al je winkels.',
  'Botlu beantwoordt vragen over levertijden, retourneren en filialen, op elk moment van de dag, en zet de rest klaar voor je team.',
  ('Modehuis Noord', 'Hoe kan ik mijn bestelling retourneren?', 'Je kunt binnen 30 dagen gratis retourneren, in een van onze winkels of met het label in je pakket.', 'Opgelost'),
  [('kennis', 'Retouren en levertijden', 'Uit je eigen website, altijd hetzelfde antwoord.'),
   ('taal', 'Ook voor klanten uit het buitenland', 'Nederlands, Engels, Duits, Frans en Spaans.'),
   ('melding', 'Klachten direct bij je team', 'Via Slack, Teams of e-mail.')],
  ['Waar blijft mijn bestelling?', 'Hoe retourneer ik iets?', 'Welke winkel heeft dit op voorraad?', 'Hoe laat is de winkel in Utrecht open?', 'Kan ik mijn bestelling wijzigen?', 'Hebben jullie cadeaukaarten?']),
 ('belastingadviseurs', 'Belastingadviseurs', 'rekenmachine', 'belastingadviseurs', 'kantoor',
  'Rustig de aangifteweken door,', 'Botlu neemt de telefoon.',
  'Botlu beantwoordt vragen over deadlines en tarieven, vraagt welke stukken iemand heeft en plant een gesprek in.',
  ('Adviesbureau Hendriks', 'Kunnen jullie mijn aangifte inkomstenbelasting doen?', 'Zeker. Woensdag om 11:00 is er plek voor een intake. Zal ik die vastzetten?', 'Afspraak'),
  [('agenda', 'Intakes ingepland', 'Direct in je agenda, ook in de drukke weken.'),
   ('kennis', 'Deadlines en tarieven', 'Uit je eigen informatie, zonder dat jij hoeft op te nemen.'),
   ('terugbel', 'Vragen voor je adviseur', 'Met naam, nummer en waar het over gaat.')],
  ['Wanneer moet mijn aangifte binnen zijn?', 'Wat kost een aangifte?', 'Welke papieren moet ik aanleveren?', 'Doen jullie ook de btw-aangifte?', 'Kan ik uitstel aanvragen?', 'Kan mijn adviseur mij terugbellen?']),
 ('apotheken', 'Apotheken', 'pil', 'apotheken', 'apotheek',
  'Minder wachten aan de lijn,', 'meer tijd aan de balie.',
  'Botlu beantwoordt vragen over openingstijden, herhaalrecepten en ophalen, en zet vragen over medicijnen klaar voor je apotheker.',
  ('Apotheek Het Plein', 'Ligt mijn herhaalrecept al klaar?', 'Dat kan ik niet zelf inzien. Ik noteer je vraag en een assistent belt je vandaag terug.', 'Terugbellen'),
  [('kennis', 'Openingstijden en dienstapotheek', 'Ook ’s avonds en in het weekend het juiste antwoord.'),
   ('terugbel', 'Vragen voor de apotheker', 'Vragen over medicijnen zet hij voor je klaar.'),
   ('taal', 'In meerdere talen', 'Nederlands, Engels, Duits, Frans en Spaans.')],
  ['Ligt mijn medicijn klaar?', 'Hoe vraag ik een herhaalrecept aan?', 'Welke apotheek heeft vanavond dienst?', 'Kunnen jullie mijn medicijnen bezorgen?', 'Tot hoe laat zijn jullie open?', 'Kan de apotheker mij terugbellen?']),
 ('makelaars', 'Makelaars', 'sleutel', 'makelaars', 'kantoor',
  'Elke bezichtiging ingepland,', 'ook als je zelf op pad bent.',
  'Botlu beantwoordt vragen over je aanbod, plant bezichtigingen in en noteert wie een waardebepaling wil.',
  ('Makelaardij De Haan', 'Is het huis aan de Dorpsstraat nog te koop?', 'Ja! Zaterdag om 14:00 is er een bezichtiging. Zal ik je aanmelden?', 'Afspraak'),
  [('agenda', 'Bezichtigingen', 'Direct ingepland op de momenten die jij vrijgeeft.'),
   ('terugbel', 'Waardebepalingen', 'Adres en wens genoteerd, zodat je gericht terugbelt.'),
   ('kennis', 'Vragen over je aanbod', 'Vraagprijs, oplevering en status, uit je eigen website.')],
  ['Is dit huis nog beschikbaar?', 'Kan ik een bezichtiging plannen?', 'Wat is mijn huis waard?', 'Wat kost verkoopbegeleiding?', 'Kan ik een bod doen?', 'Kan de makelaar mij terugbellen?']),
 ('restaurants', 'Restaurants', 'bestek', 'restaurants', 'restaurant',
  'Reserveringen aangenomen,', 'ook tijdens de drukste service.',
  'Botlu neemt op als je team in de keuken en de bediening staat, beantwoordt vragen over het menu en zet reserveringen in je agenda.',
  ('Restaurant De Gouden Lepel', 'Hebben jullie vanavond plek voor vier?', 'Om 19:30 is er een tafel voor vier. Op welke naam mag ik hem zetten?', 'Reservering'),
  [('agenda', 'Reserveringen', 'Direct in je agenda, op de tijden die jij openzet.'),
   ('kennis', 'Menu en dieetwensen', 'Uit je eigen website. Twijfelt hij, dan noteert hij het voor de keuken.'),
   ('taal', 'Ook voor toeristen', 'Nederlands, Engels, Duits, Frans en Spaans.')],
  ['Hebben jullie vanavond nog plek?', 'Hebben jullie vegetarische gerechten?', 'Kan ik voor een groep van twaalf reserveren?', 'Tot hoe laat is de keuken open?', 'Kan ik mijn reservering verzetten?', 'Kunnen we op het terras zitten?']),
 ('recruiters', 'Recruiters', 'zoekpersoon', 'recruiters', 'bureau',
  'Geen kandidaat gemist,', 'ook als je zelf in gesprek bent.',
  'Botlu beantwoordt vragen over vacatures, noteert wie er belt en voor welke functie, en plant een kennismaking in.',
  ('Talent & Co', 'Ik bel over de vacature voor magazijnmedewerker.', 'Leuk! Ik noteer je naam en ervaring en plan een kennismaking. Past donderdag om 10:00?', 'Afspraak'),
  [('terugbel', 'Kandidaten op een rij', 'Naam, functie en ervaring in één samenvatting.'),
   ('agenda', 'Kennismakingen', 'Direct in de agenda van je recruiters.'),
   ('kennis', 'Vragen over vacatures', 'Uit je eigen website, altijd actueel.')],
  ['Is deze vacature nog open?', 'Wat is het salaris?', 'Kan ik een kennismaking plannen?', 'Werken jullie ook met uitzendkrachten?', 'Hoe stuur ik mijn cv?', 'Kan de recruiter mij terugbellen?']),
]
assert len(B) == 21 and len({b[0] for b in B}) == 21

# Volgorde in het menu: zoals Daniel hem liet zien (drie kolommen, rij voor rij)
MENU_ORDER = ['medische-praktijk', 'hotels', 'vakmensen', 'advocatenkantoren', 'zelfstandigen', 'vastgoedbeheer', 'bedrijven', 'autodealers',
              'overheidsinstanties', 'autogarages', 'verenigingen', 'tandartsen', 'fysiotherapeuten', 'notarissen', 'winkels', 'retail',
              'belastingadviseurs', 'apotheken', 'makelaars', 'restaurants', 'recruiters']
BY = {b[0]: b for b in B}

# ---------- 1. Menu 'Branches' in index.html (tussen de markeringen) ----------
idx_path = SITE / 'index.html'
idx = idx_path.read_text()
items = ''.join(f'<a href="/branches/{s}">{icon(BY[s][2])}{html.escape(BY[s][1])}</a>' for s in MENU_ORDER)
menu = ('      <!-- branches -->\n      <div class="menu">\n'
        '        <button class="menu-knop" type="button" aria-haspopup="true">Branches <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 4.5l3 3 3-3"/></svg></button>\n'
        f'        <div class="menu-paneel branches">{items}</div>\n      </div>\n      <!-- /branches -->\n')
if '<!-- branches -->' in idx:
    idx = re.sub(r'      <!-- branches -->\n.*?      <!-- /branches -->\n', lambda m: menu, idx, flags=re.S)
else:
    anchor = '      <a href="/ontwikkelaars">Ontwikkelaars</a>\n'
    assert idx.count(anchor) == 1
    idx = idx.replace(anchor, menu + anchor)
idx_path.write_text(idx)

# ---------- 2. Basis uit index.html ----------
def between(start, end, incl_end=False):
    a = idx.index(start); b = idx.index(end, a + len(start))
    return idx[a:b + (len(end) if incl_end else 0)]
head_links = between('<link rel="icon"', '\n<script>')
css_base = between('<style>\n', '  /* ---------- Hero met het lint ---------- */')[len('<style>\n'):]
css_h1 = re.search(r'\n(  h1 \{[^\n]*\})', idx).group(1) + '\n'
css_secties = between('  /* ---------- Secties ---------- */', '  /* Werkt met */')
css_cta = ''.join(l for l in between('  /* ---------- Afsluiter ---------- */', '  /* ---------- Kleinere schermen ---------- */').splitlines(True)
                  if '.visual' not in l and '.ring-stage' not in l)
css_stil = between('  @media (prefers-reduced-motion: reduce) {', '</style>')
nav_src = between('<header class="nav" id="nav">', '</header>', incl_end=True)
footer_src = between('<footer>', '</footer>', incl_end=True)
# Ankers op de homepage worden /#…
nav_src = re.sub(r'href="#([\w-]+)"', r'href="/#\1"', nav_src)
footer_src = re.sub(r'href="#([\w-]+)"', r'href="/#\1"', footer_src)

ARROW = '<svg class="arrow" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
PILL = {'Afspraak': 'brand', 'Reservering': 'brand', 'Terugbellen': 'warn', 'Opgelost': 'good'}
e = lambda t: html.escape(t, quote=False)

CSS = '''
  /* ---------- Pagina per branche ---------- */
  .b-hero { position: relative; isolation: isolate; overflow: hidden; padding: 150px 0 110px;
    background: radial-gradient(38% 50% at 12% 10%, rgba(182,220,219,.5), transparent 70%), radial-gradient(40% 50% at 86% 90%, rgba(195,189,230,.5), transparent 70%), var(--bg); }
  .b-hero .metaal { position: absolute; inset: 0; z-index: -1; pointer-events: none;
    -webkit-mask-image: linear-gradient(rgba(0,0,0,.15), #000 160px); mask-image: linear-gradient(rgba(0,0,0,.15), #000 160px); }
  .b-hero .metaal canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
  .b-grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 440px); gap: 64px; align-items: center; }
  .b-copy { position: relative; }
  /* Witte waas achter de tekst, zodat hij leesbaar blijft boven de linten */
  .b-copy::before { content: ""; position: absolute; inset: -18% -20% -18% -40%; z-index: -1; pointer-events: none;
    background: radial-gradient(closest-side, rgba(255,255,255,.93) 55%, rgba(255,255,255,0)); }
  .oog { display: inline-flex; align-items: center; gap: 8px; height: 34px; margin-bottom: 22px; padding: 0 14px 0 12px; border-radius: 99px;
    background: rgba(255,255,255,.85); box-shadow: 0 0 0 1px var(--line-2); font-size: 14px; font-weight: 500; }
  .oog svg { width: 17px; height: 17px; color: var(--ink); }
  .b-hero h1 { font-size: clamp(40px, 4.8vw, 64px); }
  .b-hero h1 .soft { display: block; color: #5b6b8c; }
  .b-hero .lead { max-width: 520px; margin: 22px 0 30px; color: var(--ink-2); font-size: clamp(17px, 1.4vw, 19px); line-height: 1.55; }
  .b-hero .cta { display: flex; flex-wrap: wrap; gap: 12px; }
  /* Voorbeeldgesprek */
  .gesprek { padding: 22px; border-radius: var(--r-2xl); background: #fff; box-shadow: 0 40px 80px -30px rgba(40,30,110,.35), 0 0 0 1px rgba(16,16,24,.06); }
  .gesprek-kop { display: flex; align-items: center; gap: 8px; margin-bottom: 18px; color: var(--ink-3); font-size: 13px; }
  .gesprek-kop i { flex: none; width: 7px; height: 7px; border-radius: 50%; background: var(--good); box-shadow: 0 0 0 3px var(--good-soft); }
  .gesprek-kop b { color: var(--ink); font-weight: 600; }
  .bel { display: grid; gap: 8px; }
  .bel p { max-width: 86%; margin: 0; padding: 10px 14px; border-radius: 18px; font-size: 14.5px; line-height: 1.45; }
  .bel small { display: block; margin-bottom: 2px; color: var(--ink-4); font-size: 11px; font-weight: 600; letter-spacing: .02em; text-transform: uppercase; }
  .bel .ai { justify-self: start; background: var(--soft); border-bottom-left-radius: 6px; }
  .bel .me { justify-self: end; background: var(--brand); color: #fff; border-bottom-right-radius: 6px; }
  .bel .me small { color: rgba(255,255,255,.7); }
  .gesprek-voet { display: flex; align-items: center; justify-content: space-between; margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--line); color: var(--ink-3); font-size: 13.5px; }
  .pill { display: inline-flex; align-items: center; height: 24px; padding: 0 10px; border-radius: 99px; font-size: 12px; font-weight: 600; }
  .pill.good { background: var(--good-soft); color: var(--good); }
  .pill.brand { background: var(--brand-soft); color: var(--brand); }
  .pill.warn { background: var(--warn-soft); color: var(--warn); }
  /* Wat hij regelt */
  .taken { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }
  .taak { padding: 30px; border-radius: var(--r-2xl); background: var(--soft); }
  .taak svg { display: block; width: 28px; height: 28px; margin-bottom: 22px; color: var(--ink); }
  .taak p { margin: 0; color: var(--ink-3); }
  /* Vragen van bellers */
  .vragen { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin: 0; padding: 0; list-style: none; }
  .vragen li { padding: 16px 18px; border-radius: 18px 18px 18px 6px; background: #fff; box-shadow: 0 0 0 1px var(--line-2); color: var(--ink); font-size: 16px; }
  .sec + .sec { padding-top: 0; }
  footer { padding: 40px 0 56px; border-top: 1px solid var(--line); color: var(--ink-3); font-size: 14px; }
  footer .wrap { display: flex; flex-wrap: wrap; align-items: center; gap: 20px 32px; }
  footer nav { display: flex; flex-wrap: wrap; gap: 6px 22px; margin-left: auto; }
  footer a { text-decoration: none; }
  footer a:hover { color: var(--ink); }
  .js .rv { opacity: 0; transform: translateY(26px); transition: opacity .9s var(--ease), transform .9s var(--ease); transition-delay: var(--d, 0s); }
  .js .rv.in { opacity: 1; transform: none; }
  @media (max-width: 900px) {
    .nav-links { display: none; }
    .nav .wrap { gap: 12px; }
    .nav .btn.sm { padding: 0 13px; }
    .b-hero { padding: 120px 0 80px; }
    .b-grid, .taken { grid-template-columns: minmax(0, 1fr); gap: 40px; }
    .taken { gap: 14px; }
    .vragen { grid-template-columns: minmax(0, 1fr); }
    .b-hero .metaal { opacity: .5; }
  }
  @media (max-width: 700px) {
    .sec { padding: 84px 0; }
    .taak { padding: 24px; }
    .cta-box { padding: 56px 24px; }
    footer nav { margin-left: 0; }
  }
'''

(SITE / 'branches').mkdir(exist_ok=True)
for slug, naam, ic, voor, zaak, kop1, kop2, intro, (bedrijf, vraag, antwoord, uitkomst), taken, vragen in B:
    nav = nav_src.replace(f'href="/branches/{slug}"', f'href="/branches/{slug}" aria-current="page"')
    taken_html = ''.join(f'<div class="taak rv" style="--d:{i * .06:.2f}s">{icon(t)}<h3>{e(tt)}</h3><p>{e(tx)}</p></div>' for i, (t, tt, tx) in enumerate(taken))
    vragen_html = ''.join(f'<li class="rv" style="--d:{(i % 3) * .05:.2f}s">“{e(v)}”</li>' for i, v in enumerate(vragen))
    page = f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Botlu voor {e(voor)} · Je telefoon, altijd opgenomen</title>
<meta name="description" content="{html.escape(intro)}">
{head_links}
<script>document.documentElement.classList.add('js');</script>
<style>
{css_base}{css_h1}{css_secties}{css_cta}{CSS}{css_stil}</style>
</head>
<body>

{nav}

<main>
  <section class="b-hero">
    <div class="metaal" aria-hidden="true"><canvas></canvas></div>
    <div class="wrap b-grid">
      <div class="b-copy">
        <span class="oog rv">{icon(ic)}Voor {e(voor)}</span>
        <h1 class="rv" style="--d:.05s">{e(kop1)} <span class="soft">{e(kop2)}</span></h1>
        <p class="lead rv" style="--d:.1s">{e(intro)}</p>
        <div class="cta rv" style="--d:.15s">
          <a class="btn dark" href="/#demo">Plan een gratis demo {ARROW}</a>
          <a class="btn line" href="https://app.botlu.ai/login#aanmaken">Account aanmaken</a>
        </div>
      </div>
      <div class="gesprek rv" style="--d:.1s" aria-label="Voorbeeld van een gesprek">
        <div class="gesprek-kop"><i></i><span>Botlu neemt op voor <b>{e(bedrijf)}</b></span></div>
        <div class="bel">
          <p class="ai"><small>Botlu</small>Goedemiddag, {e(bedrijf)}. Waarmee kan ik je helpen?</p>
          <p class="me"><small>Beller</small>{e(vraag)}</p>
          <p class="ai"><small>Botlu</small>{e(antwoord)}</p>
        </div>
        <div class="gesprek-voet"><span>Samenvatting staat klaar</span><span class="pill {PILL[uitkomst]}">{e(uitkomst)}</span></div>
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="wrap">
      <div class="sec-head rv"><h2>Wat Botlu voor je regelt.</h2></div>
      <div class="taken">{taken_html}</div>
    </div>
  </section>

  <section class="sec">
    <div class="wrap">
      <div class="sec-head rv"><h2>Vragen die hij elke dag beantwoordt.</h2></div>
      <ul class="vragen">{vragen_html}</ul>
    </div>
  </section>

  <section class="cta-sec">
    <div class="wrap">
      <div class="cta-box rv">
        <div class="cta-copy">
          <h2>Probeer Botlu voor je {e(zaak)}.</h2>
          <p>Plan een gratis demo, of maak meteen een account en laat je eerste assistent vandaag nog opnemen.</p>
          <div class="cta">
            <a class="btn dark" href="/#demo">Plan een gratis demo {ARROW}</a>
            <a class="btn line" href="https://app.botlu.ai/login#aanmaken">Account aanmaken</a>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>

{footer_src}

<script src="/linten.js"></script>
<script>
const $ = s => document.querySelector(s);
const nav = $('#nav');
const solid = () => nav.classList.toggle('solid', scrollY > 40);
addEventListener('scroll', solid, {{ passive: true }});
solid();
const io = new IntersectionObserver(es => es.forEach(e => {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }}), {{ rootMargin: '0px 0px -8% 0px' }});
document.querySelectorAll('.rv').forEach(el => io.observe(el));
$('#year').textContent = new Date().getFullYear();
// Dezelfde chromen linten als op de homepage
metal($('.metaal canvas'));
</script>
</body>
</html>
'''
    (SITE / 'branches' / f'{slug}.html').write_text(page)
print('menu bijgewerkt en', len(B), 'pagina’s geschreven in branches/')
