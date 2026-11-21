# Exam corners for the JC Spanish game pages (after-launch free job, started 21 Nov 2026).
# One entry per game slug, added one topic per auto-build run in Spanish tracker order.
# EVERYTHING here is written by Léim in the style of the exam: never copy or adapt SEC
# questions, texts, audio or marking-scheme wording (SEC reply 20 Nov 2026).
# Facts used (from the Spanish Exam Centre): one common-level paper, 2 hours, 360 marks
# (Listening 140, Reading 140, Writing 80); Q17 = 5-point email/blog (30 marks), Q18 = 8-question letter (40 marks).
#
# Task kinds:
#   listen: audio = {"who": [speaker names], "lines": [[speaker index, "Spanish line"], ...]}
#           (read aloud by the browser's Spanish voice: src/build_oral_cba.py's player; plain text only)
#   read:   text = HTML of the Spanish text (shown in a .pass box)
#   write:  no text; the task is in "q"
# Every task: q (the task, HTML), qs (list of questions, may be empty), model (HTML), marks (HTML).

CORNERS = {
"meet-and-greet": dict(
    where=('Greetings and introductions are how most <b>Listening</b> dialogues start: someone meets a receptionist, '
           'a host family or a new friend, and you have to catch the <b>name</b> (often spelled out), the <b>age</b>, '
           'where they are <b>from</b> and how they <b>feel</b>. In <b>Writing</b>, every email and letter (Q17 and Q18) '
           'opens with a greeting and closes with a sign-off, and many ask you to introduce yourself. '
           'There is no speaking in the June exam, but the Oral CBA starts the same way: <em>Buenos días, me llamo…</em>'),
    tips=['<b>Answer in the language asked.</b> Listening and Reading questions are usually answered in English (or by ticking): write <em>14</em> or <em>fourteen</em>, not <em>catorce</em>.',
          '<b>Spelled names:</b> write the letters down as you hear them. Know the tricky ones: <em>ge</em> = G, <em>jota</em> = J, <em>i</em> = I, <em>e</em> = E, <em>erre</em> = R, <em>uve</em> = V.',
          '<b>Formal or informal?</b> <em>usted, señor, señora, le, buenos días</em> = formal. <em>tú, ¿qué tal?, hola</em> = informal. Give the clue word as your reason.',
          '<b>Traps:</b> <em>soy de</em> (where you\'re from) and <em>vivo en</em> (where you live) can be two different places.',
          '<b>In Writing</b>, cover every point, then check <em>tengo … años</em> (never <em>soy</em>) and <em>-o / -a</em> endings (<em>encantado / encantada</em>).'],
    tasks=[
        dict(kind='listen', title='Listening 1: at a hotel in Seville',
             q='You will hear a conversation at a hotel reception. Answer in English.',
             audio=dict(who=['Recepcionista', 'Cliente'], lines=[
                 [0, 'Buenas tardes, señora. ¿En qué puedo ayudarle?'],
                 [1, 'Buenas tardes. Tengo una reserva para tres noches.'],
                 [0, 'Muy bien. ¿Cómo se llama usted?'],
                 [1, 'Me llamo Aoife Brennan.'],
                 [0, '¿Cómo se escribe su apellido, por favor?'],
                 [1, 'Be, erre, e, ene, ene, a, ene. Brennan.'],
                 [0, 'Gracias. ¿Y de dónde es usted?'],
                 [1, 'Soy de Galway, en el oeste de Irlanda.'],
                 [0, 'Perfecto. Su habitación es la número catorce. ¡Bienvenida al hotel!']]),
             qs=['How many nights is the booking for?', 'Write down the surname she spells.',
                 'Where is she from? Give two details.', 'What is her room number?',
                 'Is this conversation formal or informal? Give one word that tells you.'],
             model='(a) <b>Three</b> nights. (b) <b>Brennan</b>. (c) <b>Galway</b>, in the <b>west of Ireland</b>. (d) Room <b>14</b>. '
                   '(e) <b>Formal</b>: the receptionist says <em>usted</em> (also: <em>señora</em>, <em>le</em>, <em>su</em>, <em>buenas tardes</em>).',
             marks='one mark for each detail; the number must be exact (14, not 4 or 40); the surname must be spelled right; '
                   'for (e), "formal" plus a clue word from the conversation.'),
        dict(kind='listen', title='Listening 2: first day at a summer camp',
             q='Two teenagers meet on the first day of a summer camp in Spain. Answer in English.',
             audio=dict(who=['Javier', 'Niamh'], lines=[
                 [0, '¡Hola! ¿Qué tal? Soy Javier. ¿Cómo te llamas?'],
                 [1, 'Hola, Javier. Me llamo Niamh. Estoy un poco nerviosa porque es mi primer día.'],
                 [0, '¡No pasa nada! Yo también estoy nervioso. ¿Cuántos años tienes?'],
                 [1, 'Tengo catorce años. ¿Y tú?'],
                 [0, 'Tengo quince. Soy de Valencia, pero vivo en Madrid. ¿De dónde eres?'],
                 [1, 'Soy irlandesa, de Kilkenny.'],
                 [0, 'Mira, te presento a mi amigo Raúl. Es muy simpático.'],
                 [1, '¡Mucho gusto, Raúl! Encantada.']]),
             qs=['How does Niamh feel, and why?', 'How old is Javier?',
                 'Where is Javier from, and where does he live now?', 'Who does Javier introduce, and what is he like?'],
             model='(a) A bit <b>nervous</b>, because it is her <b>first day</b>. (b) <b>15</b>. '
                   '(c) He is <b>from Valencia</b> but <b>lives in Madrid</b>. (d) His <b>friend Raúl</b>, who is very <b>nice / friendly</b>.',
             marks='one mark for each detail; (a) and (c) need both parts. The trap is (c): <em>soy de</em> and <em>vivo en</em> are different places. '
                   'Javier is 15, not 14 (that is Niamh).'),
        dict(kind='read', title='Reading: a message from your exchange partner',
             q='Seán is going to Spain on an exchange. Read the message from his exchange partner, Lucía, and answer the questions in English.',
             text=('<span class="sp">¡Hola, Seán! ¿Qué tal? Me llamo Lucía y soy tu compañera de intercambio. Tengo trece años y vivo en Salamanca '
                   'con mis padres y mi hermano pequeño.</span>'
                   '<span class="sp">Mañana vamos juntos al instituto. Las clases empiezan a las ocho y media. Mi profesora de inglés se llama Carmen: '
                   'es muy simpática, pero habla muy rápido. Si no entiendes, di: «¿Puede repetir, por favor?».</span>'
                   '<span class="sp">En mi instituto, los alumnos hablan de tú a los profesores. ¡No te preocupes!</span>'
                   '<span class="sp">¡Hasta mañana! Un abrazo, Lucía</span>'),
             qs=['Who does Lucía live with?', 'What time do classes start?', 'Give two details about Carmen.',
                 'What should Seán say if he doesn\'t understand?', 'What does Lucía say about how students speak to teachers?'],
             model='(a) Her <b>parents</b> and her <b>little brother</b>. (b) At <b>half past eight</b> (8:30). '
                   '(c) Any two: she is the <b>English teacher</b>; she is <b>very nice</b>; she <b>speaks very fast</b>. '
                   '(d) "<b>Can you repeat that, please?</b>" (e) Students say <b>tú</b> to their teachers (they speak to them informally).',
             marks='one mark for each detail. In (a), "brother" alone is not enough if the question has two parts: give both. '
                   '<em>pequeño</em> here means younger / little.'),
        dict(kind='write', title='Writing: an email to your exchange partner (like Q17)',
             q='You are going on an exchange to Spain. Write an email in Spanish to your exchange partner, Lucía. Include all five points:'
               '<ol style="margin:6px 0 0 22px"><li>Greet her and say your name and age.</li><li>Say where you are from and where you live.</li>'
               '<li>Describe yourself (one or two details).</li><li>Say which languages you speak.</li><li>Ask her two questions, and sign off.</li></ol>',
             qs=[],
             model='<span lang="es"><i>¡Hola, Lucía! ¿Qué tal? Me llamo Seán y tengo catorce años. Soy irlandés, de Cork, y vivo en Ballincollig con mi familia. '
                   'Soy simpático y un poco tímido. Hablo inglés e irlandés, y ahora estudio español. ¿Tienes hermanos? ¿Qué te gusta hacer los fines de semana? '
                   '¡Hasta pronto! Un abrazo, Seán</i></span>',
             marks='every one of the five points covered (a missed point can\'t be made up elsewhere); the message clear first time; '
                   'correct verbs (<em>me llamo, tengo, soy, vivo, hablo</em>); <em>e</em> instead of <em>y</em> before <em>irlandés</em>; '
                   'questions with <b>¿ ?</b>; a friendly greeting and sign-off.'),
    ]),
"number-rush": dict(
    where=('Numbers are in almost every <b>Listening</b> question: <b>times</b>, <b>prices</b>, <b>dates</b>, <b>ages</b>, '
           '<b>phone numbers</b>, room and platform numbers. They are quick, easy marks if you catch them, and easy to lose '
           'if you mix up <em>sesenta</em> and <em>setenta</em>. In <b>Reading</b>, posters, adverts and timetables are full of dates and times. '
           'In <b>Writing</b> (Q17 and Q18) you will often give your age, your birthday or the time and date of a plan.'),
    tips=['<b>Write digits, not words.</b> In Listening, jot <em>68</em> the moment you hear <em>sesenta y ocho</em>, then answer in English.',
          '<b>Pairs that trip people up:</b> <em>sesenta</em> 60 / <em>setenta</em> 70, <em>catorce</em> 14 / <em>cuarenta</em> 40, <em>quince</em> 15 / <em>cincuenta</em> 50, <em>doce</em> 12 / <em>dos</em> 2.',
          '<b>Times with <em>menos</em>:</b> go back from the NEXT hour. <em>Las doce menos diez</em> = 11:50, not 12:10.',
          '<b>Dates go day, then month:</b> <em>el veintitrés de junio</em> = 23 June. Don\'t mix up <em>junio</em> (June) and <em>julio</em> (July).',
          '<b>In Writing:</b> <em>tengo … años</em> (never <em>soy</em>), <em>el</em> + number + <em>de</em> + month, no capital letters on months or days, and <em>a las</em> for "at" a time.'],
    tasks=[
        dict(kind='listen', title='Listening 1: buying a train ticket in Madrid',
             q='You will hear a conversation at a train station ticket office. Answer in English.',
             audio=dict(who=['Cliente', 'Empleada'], lines=[
                 [0, 'Buenos días. Un billete de ida y vuelta para Toledo, por favor.'],
                 [1, 'Buenos días. ¿Para hoy?'],
                 [0, 'Sí, para hoy. ¿A qué hora sale el próximo tren?'],
                 [1, 'Sale a las once y cuarto, y llega a Toledo a las doce menos diez.'],
                 [0, 'Muy bien. ¿Cuánto cuesta?'],
                 [1, 'Son catorce euros cincuenta.'],
                 [0, 'Vale. Aquí tiene.'],
                 [1, 'Gracias. El tren sale del andén número siete. ¡Buen viaje!']]),
             qs=['What kind of ticket does the customer want, and where to?', 'What time does the next train leave?',
                 'What time does it arrive?', 'How much does the ticket cost?', 'Which platform does the train leave from?'],
             model='(a) A <b>return</b> ticket to <b>Toledo</b>. (b) At <b>11:15</b> (quarter past eleven). (c) At <b>11:50</b> (ten to twelve). '
                   '(d) <b>€14.50</b>. (e) Platform <b>7</b>.',
             marks='one mark for each detail; times and prices must be exact. The trap is (c): <em>las doce menos diez</em> is 11:50, not 12:10. '
                   'In (d), <em>catorce</em> is 14, not 40.'),
        dict(kind='listen', title='Listening 2: a phone message about a party',
             q='Ciara\'s Spanish friend Marta leaves her a phone message. Answer in English.',
             audio=dict(who=['Marta'], lines=[
                 [0, 'Hola, Ciara, soy Marta. Te llamo porque el sábado es mi cumpleaños. ¡Voy a cumplir quince años!'],
                 [0, 'Hago una fiesta en mi casa el sábado veintitrés de junio, a las siete de la tarde.'],
                 [0, 'Mi dirección es calle Mayor, número sesenta y ocho.'],
                 [0, 'Si no puedes venir, llámame al seis, cuatro, uno, treinta y dos, setenta, dieciocho.'],
                 [0, '¡Hasta pronto! Un beso.']]),
             qs=['How old will Marta be?', 'Give the day and the date of the party.', 'What time does the party start?',
                 'What is Marta\'s house number?', 'Write down her phone number.'],
             model='(a) <b>15</b>. (b) <b>Saturday 23 June</b>. (c) At <b>7 pm</b> (seven in the evening). (d) <b>68</b> (Calle Mayor). '
                   '(e) <b>641 32 70 18</b>.',
             marks='one mark for each detail; (b) needs the day and the date, and the month must be June (<em>junio</em>), not July. '
                   'Listen for <em>sesenta</em> (60) in the address and <em>setenta</em> (70) in the phone number.'),
        dict(kind='read', title='Reading: a summer camp poster',
             q='Read this poster for a summer camp in Spain and answer the questions in English.',
             text=('<span class="sp"><b>Campamento de verano «Sol y Deporte» – Málaga</b></span>'
                   '<span class="sp">Para chicos y chicas de doce a dieciséis años.</span>'
                   '<span class="sp">Fechas: del uno al quince de julio.</span>'
                   '<span class="sp">Horario: de lunes a viernes, de las nueve y media de la mañana a las dos de la tarde.</span>'
                   '<span class="sp">Actividades: fútbol, natación, tenis y vela.</span>'
                   '<span class="sp">Precio: ciento ochenta euros por las dos semanas. ¡Para hermanos, veinte euros menos!</span>'
                   '<span class="sp">Inscripción antes del treinta de mayo. Teléfono: 952 47 60 13.</span>'),
             qs=['Who is the camp for?', 'Give the dates of the camp.', 'On which days, and between what times, does the camp run?',
                 'Name two activities.', 'How much does it cost, and what is the special offer?', 'What is the closing date for booking?'],
             model='(a) Boys and girls aged <b>12 to 16</b>. (b) From <b>1 to 15 July</b>. (c) <b>Monday to Friday</b>, from <b>9:30 am to 2 pm</b>. '
                   '(d) Any two: <b>football</b>, <b>swimming</b>, <b>tennis</b>, <b>sailing</b>. (e) <b>€180</b> for the two weeks; '
                   '<b>€20 off</b> for brothers and sisters. (f) <b>30 May</b>.',
             marks='one mark for each detail; (c) and (e) need both parts. <em>Ciento ochenta</em> is 180 (not 108), and the camp is in '
                   '<em>julio</em> (July) but booking closes in <em>mayo</em> (May).'),
        dict(kind='write', title='Writing: an invitation to your birthday party (like Q17)',
             q='Write an email in Spanish to your Spanish friend, Pablo, inviting him to your birthday party. Include all five points:'
               '<ol style="margin:6px 0 0 22px"><li>Greet him and say how old you will be.</li><li>Say the date of your birthday and the day of the party.</li>'
               '<li>Say what time the party starts and where it is.</li><li>Say two things you will do at the party.</li>'
               '<li>Ask him when his birthday is, and sign off.</li></ol>',
             qs=[],
             model='<span lang="es"><i>¡Hola, Pablo! ¿Qué tal? El mes que viene voy a cumplir quince años. Mi cumpleaños es el doce de marzo, '
                   'y hago una fiesta el sábado catorce de marzo. La fiesta empieza a las ocho de la tarde en mi casa, en Athlone. '
                   'Vamos a comer pizza y a bailar. ¿Puedes venir? ¿Cuándo es tu cumpleaños? ¡Hasta pronto! Un abrazo, Clodagh</i></span>',
             marks='every one of the five points covered (a missed point can\'t be made up elsewhere); dates as <em>el</em> + number + <em>de</em> + month '
                   '(no capital letter on <em>marzo</em> or <em>sábado</em>); <em>a las</em> for the time; <em>voy a</em> / <em>vamos a</em> + infinitive for plans; '
                   'questions with <b>¿ ?</b>; a friendly greeting and sign-off.'),
    ]),
}
