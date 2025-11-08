# WEB_Trilogy

# UNIZG Career Hub

## Opis web aplikacije

<html>
<body>
<!--StartFragment--><h2 data-start="359" data-end="395"><strong data-start="365" data-end="395">1. Opis projektnog zadatka</strong></h2>
<h3 data-start="397" data-end="420"><strong data-start="401" data-end="420">Cilj aplikacije</strong></h3>
<p data-start="422" data-end="659">Glavni cilj aplikacije <strong data-start="445" data-end="465">UNIZG Career Hub</strong> je pružiti modernu, centraliziranu i preglednu web platformu koja povezuje <strong data-start="541" data-end="581">sve sastavnice Sveučilišta u Zagrebu</strong> (fakultete i akademije) s učenicima, studentima, alumnijima i poslodavcima.</p>
<p data-start="661" data-end="682">Aplikacija omogućuje:</p>
<ul data-start="683" data-end="896">
<li data-start="683" data-end="734">
<p data-start="685" data-end="734">jednostavno informiranje učenika o fakultetima,</p>
</li>
<li data-start="735" data-end="799">
<p data-start="737" data-end="799">pristup praksama, Erasmus projektima i studentskim udrugama,</p>
</li>
<li data-start="800" data-end="842">
<p data-start="802" data-end="842">objavu poslova i praksi za poslodavce,</p>
</li>
<li data-start="843" data-end="896">
<p data-start="845" data-end="896">povezivanje alumnija sa studentima i tržištem rada.</p>
</li>
</ul>
<p data-start="898" data-end="1090">Projekt ima za cilj razviti <strong data-start="926" data-end="988">intuitivnu, responzivnu i dvojezičnu (hrvatski / engleski)</strong> aplikaciju koja je dostupna široj zajednici, uključujući i <strong data-start="1048" data-end="1067">strane studente</strong> Sveučilišta u Zagrebu.</p>
<p data-start="1092" data-end="1228">Sustav omogućuje <strong data-start="1109" data-end="1137">prijave putem <a data-start="1125" data-end="1135" class="decorated-link cursor-pointer" rel="noopener">AAI@edu.hr<span aria-hidden="true" class="ms-0.5 inline-block align-middle leading-none"><svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" data-rtl-flip="" class="block h-[0.75em] w-[0.75em] stroke-current stroke-[0.75]"><path d="M14.3349 13.3301V6.60645L5.47065 15.4707C5.21095 15.7304 4.78895 15.7304 4.52925 15.4707C4.26955 15.211 4.26955 14.789 4.52925 14.5293L13.3935 5.66504H6.66011C6.29284 5.66504 5.99507 5.36727 5.99507 5C5.99507 4.63273 6.29284 4.33496 6.66011 4.33496H14.9999L15.1337 4.34863C15.4369 4.41057 15.665 4.67857 15.665 5V13.3301C15.6649 13.6973 15.3672 13.9951 14.9999 13.9951C14.6327 13.9951 14.335 13.6973 14.3349 13.3301Z"></path></svg></span></a></strong> za studente, alumnije i djelatnike sastavnica te <strong data-start="1187" data-end="1213">prijavu putem eGrađani</strong> za poslodavce.</p>
<hr data-start="1230" data-end="1233">
<h3 data-start="1235" data-end="1261"><strong data-start="1239" data-end="1261">Tehnička struktura</strong></h3>
<div class="_tableContainer_1rjym_1"><div tabindex="-1" class="group _tableWrapper_1rjym_13 flex w-fit flex-col-reverse">
Aplikacija je izrađena korištenjem React.js za frontend, Flaska (Python) za backend i PostgreSQL baze podataka.
Frontend je zadužen za prikaz korisničkog sučelja i interakciju s korisnikom, dok backend omogućuje komunikaciju, autentifikaciju i obradu zahtjeva.
Svi podaci o fakultetima, korisnicima, praksama i Erasmus projektima pohranjuju se u relacijsku bazu.
Sustav podržava AAI@edu.hr
 prijave za studente, alumnije i djelatnike sastavnica te eGrađani prijave za poslodavce.
Rezultati pretraga prikazuju se uz paginaciju radi bolje preglednosti i performansi.

</div></div>
<p data-start="1723" data-end="1842">Aplikacija koristi <strong data-start="1742" data-end="1770">straničenje (paginaciju)</strong> za prikaz rezultata pretraga kako bi se osigurala brzina i preglednost.</p>
<hr data-start="1844" data-end="1847">
<h3 data-start="1849" data-end="1877"><strong data-start="1853" data-end="1877">Korisnici aplikacije</strong></h3>
<h4 data-start="1879" data-end="1893">🧒 Učenik</h4>
<p data-start="1894" data-end="1910"><strong data-start="1894" data-end="1910">Bez prijave:</strong></p>
<ul data-start="1911" data-end="2058">
<li data-start="1911" data-end="1955">
<p data-start="1913" data-end="1955">Pregled fakulteta i studijskih programa.</p>
</li>
<li data-start="1956" data-end="2014">
<p data-start="1958" data-end="2014">Pretraga po afinitetima (“Koji je fakultet za mene?”).</p>
</li>
<li data-start="2015" data-end="2058">
<p data-start="2017" data-end="2058">Pregled studentskih udruga i događanja.</p>
</li>
</ul>
<p data-start="2060" data-end="2088"><strong data-start="2060" data-end="2088">S prijavom (<a data-start="2074" data-end="2084" class="decorated-link cursor-pointer" rel="noopener">AAI@edu.hr<span aria-hidden="true" class="ms-0.5 inline-block align-middle leading-none"><svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" data-rtl-flip="" class="block h-[0.75em] w-[0.75em] stroke-current stroke-[0.75]"><path d="M14.3349 13.3301V6.60645L5.47065 15.4707C5.21095 15.7304 4.78895 15.7304 4.52925 15.4707C4.26955 15.211 4.26955 14.789 4.52925 14.5293L13.3935 5.66504H6.66011C6.29284 5.66504 5.99507 5.36727 5.99507 5C5.99507 4.63273 6.29284 4.33496 6.66011 4.33496H14.9999L15.1337 4.34863C15.4369 4.41057 15.665 4.67857 15.665 5V13.3301C15.6649 13.6973 15.3672 13.9951 14.9999 13.9951C14.6327 13.9951 14.335 13.6973 14.3349 13.3301Z"></path></svg></span></a>):</strong></p>
<ul data-start="2089" data-end="2171">
<li data-start="2089" data-end="2132">
<p data-start="2091" data-end="2132">Spremanje omiljenih fakulteta i udruga.</p>
</li>
<li data-start="2133" data-end="2171">
<p data-start="2135" data-end="2171">Slanje upita ili zahtjeva fakultetu.</p>
</li>
</ul>
<hr data-start="2173" data-end="2176">
<h4 data-start="2178" data-end="2196">🧑‍🎓 Student</h4>
<p data-start="2197" data-end="2213"><strong data-start="2197" data-end="2213">Bez prijave:</strong></p>
<ul data-start="2214" data-end="2273">
<li data-start="2214" data-end="2273">
<p data-start="2216" data-end="2273">Pregled studentskih udruga, praksi i Erasmus projekata.</p>
</li>
</ul>
<p data-start="2275" data-end="2303"><strong data-start="2275" data-end="2303">S prijavom (<a data-start="2289" data-end="2299" class="decorated-link cursor-pointer" rel="noopener">AAI@edu.hr<span aria-hidden="true" class="ms-0.5 inline-block align-middle leading-none"><svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" data-rtl-flip="" class="block h-[0.75em] w-[0.75em] stroke-current stroke-[0.75]"><path d="M14.3349 13.3301V6.60645L5.47065 15.4707C5.21095 15.7304 4.78895 15.7304 4.52925 15.4707C4.26955 15.211 4.26955 14.789 4.52925 14.5293L13.3935 5.66504H6.66011C6.29284 5.66504 5.99507 5.36727 5.99507 5C5.99507 4.63273 6.29284 4.33496 6.66011 4.33496H14.9999L15.1337 4.34863C15.4369 4.41057 15.665 4.67857 15.665 5V13.3301C15.6649 13.6973 15.3672 13.9951 14.9999 13.9951C14.6327 13.9951 14.335 13.6973 14.3349 13.3301Z"></path></svg></span></a>):</strong></p>
<ul data-start="2304" data-end="2457">
<li data-start="2304" data-end="2336">
<p data-start="2306" data-end="2336">Prijava na praksu ili posao.</p>
</li>
<li data-start="2337" data-end="2374">
<p data-start="2339" data-end="2374">Pridruživanje studentskoj udruzi.</p>
</li>
<li data-start="2375" data-end="2406">
<p data-start="2377" data-end="2406">Prijava na Erasmus projekt.</p>
</li>
<li data-start="2407" data-end="2457">
<p data-start="2409" data-end="2457">Uređivanje osobnog profila i spremanje favorita.</p>
</li>
</ul>
<hr data-start="2459" data-end="2462">
<h4 data-start="2464" data-end="2479">🎓 Alumnus</h4>
<p data-start="2480" data-end="2496"><strong data-start="2480" data-end="2496">Bez prijave:</strong></p>
<ul data-start="2497" data-end="2539">
<li data-start="2497" data-end="2539">
<p data-start="2499" data-end="2539">Pregled otvorenih poslova i događanja.</p>
</li>
</ul>
<p data-start="2541" data-end="2569"><strong data-start="2541" data-end="2569">S prijavom (<a data-start="2555" data-end="2565" class="decorated-link cursor-pointer" rel="noopener">AAI@edu.hr<span aria-hidden="true" class="ms-0.5 inline-block align-middle leading-none"><svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" data-rtl-flip="" class="block h-[0.75em] w-[0.75em] stroke-current stroke-[0.75]"><path d="M14.3349 13.3301V6.60645L5.47065 15.4707C5.21095 15.7304 4.78895 15.7304 4.52925 15.4707C4.26955 15.211 4.26955 14.789 4.52925 14.5293L13.3935 5.66504H6.66011C6.29284 5.66504 5.99507 5.36727 5.99507 5C5.99507 4.63273 6.29284 4.33496 6.66011 4.33496H14.9999L15.1337 4.34863C15.4369 4.41057 15.665 4.67857 15.665 5V13.3301C15.6649 13.6973 15.3672 13.9951 14.9999 13.9951C14.6327 13.9951 14.335 13.6973 14.3349 13.3301Z"></path></svg></span></a>):</strong></p>
<ul data-start="2570" data-end="2666">
<li data-start="2570" data-end="2591">
<p data-start="2572" data-end="2591">Prijava na posao.</p>
</li>
<li data-start="2592" data-end="2619">
<p data-start="2594" data-end="2619">Mentoriranje studenata.</p>
</li>
<li data-start="2620" data-end="2666">
<p data-start="2622" data-end="2666">Uređivanje profila i karijernih informacija.</p>
</li>
</ul>
<hr data-start="2668" data-end="2671">
<h4 data-start="2673" data-end="2691">🏢 Poslodavac</h4>
<p data-start="2692" data-end="2708"><strong data-start="2692" data-end="2708">Bez prijave:</strong></p>
<ul data-start="2709" data-end="2753">
<li data-start="2709" data-end="2753">
<p data-start="2711" data-end="2753">Pregled fakulteta i studijskih smjerova.</p>
</li>
</ul>
<p data-start="2755" data-end="2781"><strong data-start="2755" data-end="2781">S prijavom (eGrađani):</strong></p>
<ul data-start="2782" data-end="2938">
<li data-start="2782" data-end="2827">
<p data-start="2784" data-end="2827">Objavljivanje oglasa za posao ili praksu.</p>
</li>
<li data-start="2828" data-end="2883">
<p data-start="2830" data-end="2883">Pregled prijavljenih kandidata (studenti i alumni).</p>
</li>
<li data-start="2884" data-end="2938">
<p data-start="2886" data-end="2938">Kontaktiranje kandidata i uređivanje profila tvrtke.</p>
</li>
</ul>
<hr data-start="2940" data-end="2943">
<h4 data-start="2945" data-end="2975">🏛️ Fakultet / Sastavnica</h4>
<p data-start="2976" data-end="3004"><strong data-start="2976" data-end="3004">S prijavom (<a data-start="2990" data-end="3000" class="decorated-link cursor-pointer" rel="noopener">AAI@edu.hr<span aria-hidden="true" class="ms-0.5 inline-block align-middle leading-none"><svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" data-rtl-flip="" class="block h-[0.75em] w-[0.75em] stroke-current stroke-[0.75]"><path d="M14.3349 13.3301V6.60645L5.47065 15.4707C5.21095 15.7304 4.78895 15.7304 4.52925 15.4707C4.26955 15.211 4.26955 14.789 4.52925 14.5293L13.3935 5.66504H6.66011C6.29284 5.66504 5.99507 5.36727 5.99507 5C5.99507 4.63273 6.29284 4.33496 6.66011 4.33496H14.9999L15.1337 4.34863C15.4369 4.41057 15.665 4.67857 15.665 5V13.3301C15.6649 13.6973 15.3672 13.9951 14.9999 13.9951C14.6327 13.9951 14.335 13.6973 14.3349 13.3301Z"></path></svg></span></a>):</strong></p>
<ul data-start="3005" data-end="3157">
<li data-start="3005" data-end="3043">
<p data-start="3007" data-end="3043">Upravljanje fakultetskim profilom.</p>
</li>
<li data-start="3044" data-end="3077">
<p data-start="3046" data-end="3077">Objavljivanje Erasmus ponuda.</p>
</li>
<li data-start="3078" data-end="3115">
<p data-start="3080" data-end="3115">Upravljanje studentskim udrugama.</p>
</li>
<li data-start="3116" data-end="3157">
<p data-start="3118" data-end="3157">Pregled interesa učenika i poslodavaca.</p>
</li>
</ul>
<hr data-start="3159" data-end="3162">
<h3 data-start="3164" data-end="3190"><strong data-start="3168" data-end="3190">Moguće nadogradnje</strong></h3>
<ul data-start="3191" data-end="3535">
<li data-start="3191" data-end="3245">
<p data-start="3193" data-end="3245">Chat modul između studenata, udruga i poslodavaca.</p>
</li>
<li data-start="3246" data-end="3308">
<p data-start="3248" data-end="3308">AI sustav za preporuku fakulteta prema interesima učenika.</p>
</li>
<li data-start="3309" data-end="3369">
<p data-start="3311" data-end="3369">Kalendar događanja (Smotra, Erasmus, karijerni sajmovi).</p>
</li>
<li data-start="3370" data-end="3438">
<p data-start="3372" data-end="3438">Statistički dashboard za fakultete (analiza interesa i prijava).</p>
</li>
<li data-start="3439" data-end="3484">
<p data-start="3441" data-end="3484">Sinkronizirana engleska verzija sadržaja.</p>
</li>
<li data-start="3485" data-end="3535">
<p data-start="3487" data-end="3535">Integracija s LinkedIn API-em za alumni profile.</p>
</li>
</ul>
<hr data-start="3537" data-end="3540">
<h3 data-start="3542" data-end="3559"><strong data-start="3546" data-end="3559">Zaključak</strong></h3>
<p data-start="3561" data-end="3851"><strong data-start="3561" data-end="3581">UNIZG Career Hub</strong> povezuje učenike, studente, alumnije, poslodavce i sastavnice Sveučilišta u Zagrebu kroz jedinstveno, digitalno i interaktivno sučelje.<br data-start="3717" data-end="3720">
Projekt promiče razvoj karijera, međunarodnu suradnju i vidljivost Sveučilišta kroz transparentan, suvremen i lako proširiv sustav.</p>
<!--EndFragment-->
</body>
</html>
