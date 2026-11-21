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
}
