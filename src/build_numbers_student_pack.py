head = open('/home/claude/head_num.html').read()
B = '<span class="box"></span>'
ln = '<span class="long"></span>'
def band(k, h): return f'<div class="band"><div><div class="k">{k}</div><h1>{h}</h1></div><div class="logo">↗ Léim</div></div>'
def ol(items, start=1, cls='ans', extra=''): return f'<ol class="{cls}" start="{start}"{extra}>' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'

cover = '''
<div class="cover">
  <div>
    <span class="pill">Junior Cycle Spanish · Student revision pack</span>
    <h1>Numbers, dates &amp; <span>time</span></h1>
    <div class="sub">Everything a student needs to use numbers, ages, dates, prices and times with confidence. They come up again and again in the listening and reading sections.</div>
    <ul>
      <li>A one-page cheat sheet: numbers, age, dates, time</li>
      <li>30 key questions, days, dates and time phrases with exam sentences</li>
      <li>30 practice questions in three steps</li>
      <li>An exam-style reading: a summer camp advert</li>
      <li>A writing task with a model answer</li>
      <li>A 20-question self-test and fold-over flashcards</li>
      <li>Full answers</li>
    </ul>
  </div>
  <div class="foot">
    <div class="small">Written by a language teacher with over 25 years in the classroom. All texts and questions are original Léim material, written in the style of the exam. Independent practice material: not an official SEC publication. Free game to go with it: leim.ie/number-rush.html</div>
    <div class="logo">↗ Léim</div>
  </div>
</div>'''

plan = [
 ('Read the cheat sheet (page 3). Cut out and fold the flashcards (page 9) and test yourself.', '20 min'),
 ('Learn phrases 1–15 from the phrase bank (page 4). Count from 1 to 100 out loud in tens, then in ones.', '20 min'),
 ('Learn phrases 16–30. Then do Practice A, B and C (page 5) and correct them.', '30 min'),
 ('Exam reading (page 6). Then the writing task (page 7): read the model answer first.', '40 min'),
 ('Self-test (page 8) with no notes. Under 15/20? Go back to page 3 and try again in two days.', '15 min')]
cans = ['count from 1 to 100 and say years like 2013',
 'say my age and ask someone else\'s with tener',
 'say the date and my birthday (el tres de mayo)',
 'tell the time, with y cuarto, y media and menos',
 'understand prices and 24-hour times',
 'pick out numbers, dates and times in a reading or listening text']
start = f'''
<div class="page">
  {band('Start here','How to use this pack')}
  <p>Numbers, dates and times turn up all over Junior Cycle Spanish: ages and birthdays when people introduce themselves, times in timetables and plans, prices in shops and adverts. In the <b>listening and reading</b> sections they are some of the easiest marks to win, if you know them well.</p>
  <h2>Your 5-day plan</h2>
  <table class="prog">
    <tr><th style="width:16mm">Day</th><th>Do this</th><th style="width:22mm">Time</th><th style="width:12mm">Tick</th></tr>
    {''.join(f'<tr><td><b>{i+1}</b></td><td>{d}</td><td>{t}</td><td>{B}</td></tr>' for i,(d,t) in enumerate(plan))}
  </table>
  <h2>Can you do it? Tick now, and again on day 5</h2>
  <table class="prog">
    <tr><th>I can…</th><th style="width:20mm">Day 1</th><th style="width:20mm">Day 5</th></tr>
    {''.join(f'<tr><td>{c}</td><td>{B}</td><td>{B}</td></tr>' for c in cans)}
  </table>
  <div class="note"><b>For parents:</b> you don't need any Spanish to help. Call out a number, a date or a time in English and let your child say it in Spanish, or point at a clock. All answers are on page 10.</div>
  <div class="tip"><b>Practise on screen too:</b> Number Rush, the free Léim game, has a listening mode that reads numbers, dates and times aloud: <b>leim.ie/number-rush.html</b></div>
</div>'''

cheat = f'''
<div class="page tight">
  {band('Cheat sheet','Numbers, dates &amp; time on one page')}
  <h2>1. Numbers</h2>
  <table>
    <tr><td><b>0–15</b></td><td>cero, uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, diez, once, doce, trece, catorce, quince</td></tr>
    <tr><td><b>16–29</b><br>one word</td><td>dieciséis, diecisiete, dieciocho, diecinueve, veinte, veintiuno, veintidós, veintitrés … veintinueve</td></tr>
    <tr><td><b>30–99</b><br>tens + y + unit</td><td>treinta, cuarenta, cincuenta, sesenta, setenta, ochenta, noventa · 35 = treinta <b>y</b> cinco · 47 = cuarenta <b>y</b> siete</td></tr>
    <tr><td><b>100+</b></td><td>100 cien · 101 ciento uno · 200 doscientos · 500 quinientos · 1000 mil · 2013 dos mil trece</td></tr>
  </table>
  <p><b>Don't mix up:</b> sesenta (60) / setenta (70) · quince (15) / cincuenta (50) · catorce (14) / cuarenta (40). <b>Prices:</b> 2,50 € = dos euros cincuenta (Spain uses a comma).</p>
  <div class="two">
    <div>
      <h2>2. Age: tener, not ser</h2>
      <p>¿Cuántos años <b>tienes</b>? → <b>Tengo</b> trece años.<br>Mi madre <b>tiene</b> cuarenta y un años.<br>Before años: uno → <b>un</b> (veinti<b>ún</b> años).</p>
      <h2>3. Dates and days</h2>
      <p><b>el</b> + number + <b>de</b> + month: <i>Mi cumpleaños es <b>el</b> tres <b>de</b> mayo.</i><br>Months and days have <b>no capital</b>: enero, febrero, marzo, abril, mayo, junio, julio, agosto, septiembre, octubre, noviembre, diciembre · lunes, martes, miércoles, jueves, viernes, sábado, domingo.<br><b>el</b> lunes = on Monday · <b>los</b> lunes = on Mondays</p>
    </div>
    <div>
      <h2>4. Telling the time</h2>
      <table>
        <tr><th>Time</th><th>¿Qué hora es?</th></tr>
        <tr><td>1:00</td><td><b>Es la</b> una</td></tr>
        <tr><td>3:00</td><td><b>Son las</b> tres (en punto)</td></tr>
        <tr><td>3:15</td><td>Son las tres y cuarto</td></tr>
        <tr><td>3:30</td><td>Son las tres y media</td></tr>
        <tr><td>3:40</td><td>Son las <b>cuatro menos</b> veinte</td></tr>
        <tr><td>3:45</td><td>Son las <b>cuatro menos</b> cuarto</td></tr>
      </table>
      <p>After half past: next hour + <b>menos</b>. At a time: <b>a las</b> ocho, <b>a la</b> una. Timetables use the 24-hour clock: 20:30 = las veinte treinta.</p>
    </div>
  </div>
  <h2>5. The five mistakes that cost the most marks</h2>
  <table>
    <tr><th>Wrong</th><th>Right</th><th>Why</th></tr>
    <tr><td><s>Soy</s> trece años.</td><td><b>Tengo</b> trece años.</td><td>Age uses tener.</td></tr>
    <tr><td><s>Es</s> las tres.</td><td><b>Son</b> las tres.</td><td>Only one o'clock is "es la una".</td></tr>
    <tr><td>Es <s>en</s> tres de <s>Mayo</s>.</td><td>Es <b>el</b> tres de <b>mayo</b>.</td><td>el + date; no capital.</td></tr>
    <tr><td><s>a las una</s></td><td><b>a la una</b></td><td>una is singular.</td></tr>
    <tr><td>Tiene <s>veintiuno</s> años.</td><td>Tiene <b>veintiún</b> años.</td><td>uno → un before a noun.</td></tr>
  </table>
  <div class="tip"><b>Exam tip:</b> in listening, read the question first, and write numbers in <b>digits</b> as you hear them. Watch out for <b>menos</b> (it changes the hour) and for sesenta / setenta.</div>
</div>'''

bank = [
 ('¿Cuántos años tienes?','How old are you?','Tengo catorce años.'),
 ('¿Cuándo es tu cumpleaños?','When is your birthday?','Es el doce de octubre.'),
 ('¿Qué hora es?','What time is it?','Son las cinco y media.'),
 ('¿A qué hora…?','At what time…?','¿A qué hora empieza la película?'),
 ('¿Cuánto cuesta?','How much is it?','Cuesta tres euros cincuenta.'),
 ('¿Qué fecha es hoy?',"What's the date today?",'Hoy es el uno de junio.'),
 ('nací en…','I was born in…','Nací en dos mil doce.'),
 ('tener … años','to be … years old','Mi abuelo tiene setenta años.'),
 ('el cumpleaños','birthday','Mi cumpleaños es en verano.'),
 ('el euro / el céntimo','euro / cent','Son dos euros con veinte céntimos.'),
 ('lunes, martes, miércoles','Monday, Tuesday, Wednesday','El lunes tengo español.'),
 ('jueves, viernes','Thursday, Friday','Los viernes juego al fútbol.'),
 ('sábado, domingo','Saturday, Sunday','El sábado voy al cine.'),
 ('el fin de semana','the weekend','El fin de semana descanso.'),
 ('hoy / mañana','today / tomorrow','Hoy es martes y mañana es miércoles.'),
 ('ayer','yesterday','Ayer fue domingo.'),
 ('la semana que viene','next week','El examen es la semana que viene.'),
 ('el mes / el año','month / year','Hay doce meses en un año.'),
 ('en enero','in January','Mi cumpleaños es en enero.'),
 ('primavera, verano, otoño, invierno','spring, summer, autumn, winter','Prefiero la primavera.'),
 ('en punto',"o'clock exactly",'Son las ocho en punto.'),
 ('y cuarto','quarter past','Son las dos y cuarto.'),
 ('y media','half past','Son las siete y media.'),
 ('menos cuarto','quarter to','Son las diez menos cuarto.'),
 ('a las…',"at … o'clock",'Las clases empiezan a las nueve.'),
 ('de la mañana','in the morning','Me levanto a las siete de la mañana.'),
 ('de la tarde','in the afternoon / evening','Vuelvo a las cuatro de la tarde.'),
 ('de la noche','at night','Me acuesto a las diez de la noche.'),
 ('el mediodía / la medianoche','midday / midnight','Comemos a mediodía.'),
 ('temprano / tarde','early / late','Los sábados me levanto tarde.')]
groups = {0:'Questions and answers',10:'Days, dates and seasons',20:'Telling the time'}
rows = ''
for i,(es,en,ex) in enumerate(bank):
    if i in groups: rows += f'<tr><td colspan="4" style="background:var(--green-soft);font-weight:800;color:var(--green)">{groups[i]}</td></tr>'
    rows += f'<tr><td>{i+1}</td><td><b>{es}</b></td><td>{en}</td><td>{ex}</td></tr>'
bankpage = f'''
<div class="page">
  {band('Phrase bank','The 30 phrases you\'ll use most')}
  <p class="small">Cover the Spanish and test yourself from the English. Remember: days and months have no capital letter in Spanish.</p>
  <table class="vb lob">
    <tr><th></th><th>Spanish</th><th>English</th><th>Exam sentence</th></tr>
    {rows}
  </table>
</div>'''

g = '<span class="gap" style="min-width:60px"></span>'
nums = ['setenta y dos','quince','sesenta y seis','cincuenta','catorce','noventa y uno','quinientos','cuarenta y tres','dos mil once','trescientos veinte']
times = ['1:00','4:15','6:30','8:45','10:20','11:50','2:05','7:35','12:00','9:10']
practice = f'''
<div class="page">
  {band('Practice · 30 marks','Three steps to sure')}
  <h2>A. Write the number in digits <span class="m">/ 10</span></h2>
  <p class="small">This is the skill you need for the listening section: hear (or read) the Spanish, write the digits fast.</p>
  <div class="two">{ol([f'{n} → {g}' for n in nums[:5]],1,'q')}{ol([f'{n} → {g}' for n in nums[5:]],6,'q')}</div>
  <h2>B. ¿Qué hora es? Write the time in Spanish <span class="m">/ 10</span></h2>
  <div class="two">{ol([f'<b>{t}</b><span class="long"></span>' for t in times[:5]],1,'q')}{ol([f'<b>{t}</b><span class="long"></span>' for t in times[5:]],6,'q')}</div>
  <h2>C. Say it in Spanish <span class="m">/ 10 (2 each)</span></h2>
  {ol([x+ln for x in ['My birthday is on the 3rd of May.','My sister is 21 years old.','The film starts at half past eight.','It costs 4 euros 50.','On Saturdays I get up at ten o\'clock.']],1,'q')}
</div>'''

qs = ['What ages is the camp for?','What are the dates for group B?','How much does the camp cost, and what is included?','What discount do brothers and sisters get?',
 'What time is breakfast?','What activities are there in the morning? Give <b>one</b>.','What can you do in your free time? Give <b>one</b> thing.',
 'What time is dinner?','Where do they go on Sundays, and what time do they come back?','What is the last date to sign up?']
reading = f'''
<div class="page tight rd">
  {band('Exam-style reading · 25 marks','A summer camp in Spain')}
  <p>Read the advert and Daniel's message, then answer <b>in English</b>. Write times and dates in digits.</p>
  <div class="text">
    <p class="title" style="font-weight:800;font-size:12pt">CAMPAMENTO DE VERANO «SOL Y MAR» · Santander</p>
    <p>Para jóvenes de <b>12 a 16 años</b>. <b>Fechas:</b> del 1 al 14 de julio (grupo A) · del 15 al 28 de julio (grupo B).</p>
    <p><b>Precio:</b> 450 euros por dos semanas, con todas las comidas incluidas. Hermanos: 50 euros de descuento.</p>
    <p><b>Un día normal:</b> 8:00 desayuno · 9:30 clases de surf o de vela · 13:30 comida · 15:00 tiempo libre (piscina o playa) · 17:00 talleres: teatro, música o fotografía · 21:00 cena · 22:30 ¡a dormir!</p>
    <p><b>Los domingos:</b> excursión a Bilbao (salida a las 9:00, vuelta a las 19:00).</p>
    <p><b>Inscripciones:</b> antes del 30 de mayo.</p>
  </div>
  <div class="text">
    <p>¡Hola! Me llamo Daniel. Tengo trece años y mi cumpleaños es el veinte de julio. Voy al campamento con mi hermana Sara, que tiene quince años. Vamos en el grupo B, así que ¡voy a celebrar mi cumpleaños en la playa!</p>
  </div>
  <h2>The advert <span class="m">/ 20</span></h2>
  <ol class="q">{''.join(f'<li>{q}{ln}</li>' for q in qs)}</ol>
  <h2>Daniel's message <span class="m">/ 5</span></h2>
  <div class="two"><ol class="q" type="a"><li>How old is Daniel? <span class="gap"></span></li><li>When is his birthday? <span class="gap"></span></li><li>How old is Sara? <span class="gap"></span></li></ol>
  <ol class="q" type="a" start="4"><li>Which group are they in? <span class="gap"></span></li><li>Where will he celebrate? <span class="gap"></span></li></ol></div>
</div>'''

writing = f'''
<div class="page tight">
  {band('Exam-style writing','An email before the camp')}
  <div class="taskbox"><b>The task:</b> You are going to a summer camp in Spain. Write an email (about 80–100 words) to your Spanish group leader, Lucía. Include:
    ① your age and your birthday · ② your family (names and ages) · ③ your normal school day, with times · ④ when you arrive and one thing you want to do.</div>
  <h2>Model answer</h2>
  <div class="model">
    <p>¡Hola, Lucía!</p>
    <p>Me llamo Ciarán y <b class="v">tengo catorce años</b>. Mi cumpleaños es <b class="v">el nueve de marzo</b>. Vivo en Waterford con mi madre y mis dos hermanos. Mi hermano Eoin <b class="v">tiene diecisiete años</b> y mi hermana Aoife <b class="v">tiene once</b>.</p>
    <p>Entre semana me levanto <b class="v">a las siete y cuarto</b> y las clases empiezan <b class="v">a las nueve menos diez</b>. Vuelvo a casa <b class="v">a las cuatro y media</b>.</p>
    <p>Llego a Santander <b class="v">el quince de julio a las seis de la tarde</b>. ¡Quiero hacer surf todos los días!</p>
    <p>Hasta pronto,<br>Ciarán</p>
  </div>
  <h2>Why it scores</h2>
  <ul class="why">
    <li><b>All four points are covered.</b> A missed point loses marks however good the Spanish is.</li>
    <li><b>Ages with tener</b> for him and his family, never "soy … años".</li>
    <li><b>Dates the Spanish way:</b> el nueve de marzo, el quince de julio, with no capital letters.</li>
    <li><b>A range of times:</b> y cuarto, menos diez, y media, de la tarde, all with "a las".</li>
    <li><b>Quiero + infinitive</b> to say what he wants to do, and a proper email opening and closing.</li>
  </ul>
  <div class="note"><b>Steal these phrases:</b> Tengo … años · Mi cumpleaños es el … de … · Entre semana me levanto a las… · Llego el … a las … de la tarde · ¡Quiero…!</div>
  <div class="yt"><b>Your turn:</b> Write a message (about 80–100 words) inviting a Spanish friend to a birthday party. Include: ① whose birthday it is and how old they are · ② the day, date and time · ③ where it is · ④ what to bring and what time it finishes.</div>
  {ln*10}
  <p class="small" style="margin-top:6px"><b>Before you finish:</b> {B}all 4 points {B}ages with tener {B}dates with el … de … {B}a las / a la una {B}about 80–100 words</p>
</div>'''

mc = [('"Sesenta" is…','16','60','70'),('"Quince" is…','50','14','15'),('Yo ___ trece años.','tengo','soy','estoy'),
 ('___ la una.','Son','Es','Está'),('3:30 = Son las tres y ___.','media','medio','mitad'),('3:45 = Son las ___ menos cuarto.','tres','cuatro','dos'),
 ('Mi cumpleaños es ___ cinco de abril.','en','el','la'),('Mi hermano tiene ___ años. (21)','veintiuno','veinte uno','veintiún'),
 ('The seventh month is…','junio','julio','mayo'),('"Miércoles" is…','Wednesday','Thursday','Monday'),
 ('El partido empieza ___ ocho.','en las','a las','las'),('2010 = dos mil ___','diez','cien','uno'),('100 = ___','cien','ciento','cientos'),
 ('"Los sábados" means…','on one Saturday','on Saturdays',"Saturday's"),('¿___ años tienes?','Cuánto','Cuántos','Cuándo'),
 ('¿___ es tu cumpleaños?','Cuántos','Qué','Cuándo'),('22:00 = las diez de la ___','mañana','noche','tarde'),
 ('2,50 € = dos euros ___','cincuenta','cinco','quinientos'),('40 = ___','catorce','cuarenta','cuatro'),('Hoy es ___. (Monday)','Lunes','el lunes','lunes')]
key = ['b','c','a','b','a','b','b','c','b','a','b','a','a','b','b','c','b','a','b','c']
mcl = ''.join(f'<li>{q}<span class="o">a) {a} &nbsp; b) {b} &nbsp; c) {c}</span></li>' for q,a,b,c in mc)
selftest = f'''
<div class="page">
  {band('Self-test · no notes · 20 marks','Are you exam-ready?')}
  <p>Circle the right answer. Give yourself 10 minutes.</p>
  <ol class="mc">{mcl}</ol>
  <h2>Your score</h2>
  <table class="prog">
    <tr><th style="width:28mm">Score</th><th>What next</th></tr>
    <tr><td><b>18–20</b></td><td>Exam-ready. Keep it fresh with a round of Number Rush (listening mode) once a week.</td></tr>
    <tr><td><b>15–17</b></td><td>Nearly there. Check which group your mistakes come from on the cheat sheet (page 3) and redo those flashcards.</td></tr>
    <tr><td><b>0–14</b></td><td>Go back to the cheat sheet and phrase bank, redo Practice A–C, and take the test again in two days.</td></tr>
  </table>
  <div class="tip"><b>Which mistakes?</b> Questions 1, 2, 8, 12, 13, 18, 19 = numbers · 3, 15 = age · 7, 9, 10, 14, 16, 20 = dates and days · 4, 5, 6, 11, 17 = telling the time.</div>
</div>'''

cards = [('How old are you?','¿Cuántos años tienes?'),("I'm 14",'tengo catorce años'),('When is your birthday?','¿Cuándo es tu cumpleaños?'),
 ('What time is it?','¿Qué hora es?'),("at 8 o'clock",'a las ocho'),("It's 1 o'clock",'es la una'),('half past','y media'),('quarter past','y cuarto'),
 ('quarter to','menos cuarto'),('in the morning','de la mañana'),('15','quince'),('50','cincuenta'),('60','sesenta'),('70','setenta'),
 ('100','cien'),('July','julio'),('Wednesday','miércoles'),('How much is it?','¿Cuánto cuesta?')]
cardhtml = ''.join(f'<div class="card"><div class="en">{e}</div><div class="es" style="font-size:{"12pt" if len(s)>16 else "15pt"}">{s}</div></div>' for e,s in cards)
flash = f'''
<div class="page">
  {band('Cut out · fold · test','Fold-over flashcards')}
  <p>Cut along the dashed lines, then fold each card along the dotted line so the English is on one side and the Spanish on the other. Say the Spanish, then flip to check. Put the ones you get wrong in a separate pile.</p>
  <div class="cards">{cardhtml}</div>
</div>'''

answers = f'''
<div class="page tight">
  {band('Answers','Check your work')}
  <div class="two">
    <div><h2>Practice A</h2>{ol(['72','15','66','50','14','91','500','43','2011','320'])}</div>
    <div><h2>Practice B</h2>{ol(['Es la una.','Son las cuatro y cuarto.','Son las seis y media.','Son las nueve menos cuarto.','Son las diez y veinte.','Son las doce menos diez.','Son las dos y cinco.','Son las ocho menos veinticinco.','Son las doce. (Es mediodía / medianoche.)','Son las nueve y diez.'])}</div>
  </div>
  <h2>Practice C</h2>
  {ol(['Mi cumpleaños es el tres de mayo.','Mi hermana tiene veintiún años.','La película empieza a las ocho y media.','Cuesta cuatro euros cincuenta.','Los sábados me levanto a las diez.'])}
  <div class="two">
    <div><h2>Reading (2 marks each)</h2>
    {ol(['12 to 16.','15 to 28 July.','€450 for two weeks; all meals are included.','€50.','8.00.','Surfing or sailing.','Swimming pool or beach.','21.00 (9 pm).','A trip to Bilbao; back at 19.00 (7 pm).','30 May.'])}
    <p><b>Daniel:</b> a) 13 · b) 20 July · c) 15 · d) group B · e) on the beach</p></div>
    <div><h2>Self-test</h2><div class="cols3">{ol(key)}</div>
    <h2>Writing: check your own</h2>
    <p class="small">Give yourself up to 5 marks for each of the 4 points: 2 for covering it, 3 for correct Spanish (take off 1 for each mistake with ages, dates or times). This is a Léim practice guide, not the official SEC marking scheme.</p></div>
  </div>
</div>'''

head = head.replace('</head>','<style>.rd .long{height:18px}.rd .q li{margin:3px 0}.rd .text{padding:7px 12px}</style></head>')
html = head + cover + start + cheat + bankpage + practice + reading + writing + selftest + flash + answers + '\n</body></html>\n'
open('/home/claude/leim/src/numbers-dates-time-student-pack.html','w').write(html)
