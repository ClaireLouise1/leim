# -*- coding: utf-8 -*-
"""Léim Oral CBA (Junior Cycle Spanish) content. All texts original Léim material.
Used by src/build_oral_cba.py for the pack PDF, the free Speaking page and the audio page.
who: 0 = student, 1 = teacher / other speaker."""

LO17 = "1.9–1.13, 1.15, 2.1, 2.7, 3.2, 3.7, 3.8"

MODELS = [
 dict(id="pres1", fmt="Presentation", title="Mi deporte favorito: el fútbol gaélico",
  who=["Cian", "Profesor"],
  setup="Cian holds up his club jersey and shows two photos on the board: his team, and the final.",
  talk=[
   "Hola, me llamo Cian y hoy voy a hablar de mi deporte favorito, el fútbol gaélico.",
   "Es un deporte tradicional irlandés y es muy popular en Irlanda. Se juega con quince jugadores en cada equipo y con un balón redondo. Puedes tocar el balón con las manos y con los pies. ¡Es una mezcla de fútbol y rugby!",
   "Juego en el club de mi pueblo desde hace seis años. Entrenamos los martes y los jueves, y los partidos son los sábados por la mañana. Me encanta porque es rápido y emocionante, y porque mis mejores amigos están en el equipo. Lo malo es que a veces hace mucho frío y llueve durante los partidos.",
   "El año pasado ganamos la final de la liga y lo celebramos con una fiesta en el club. Fue el mejor día del año.",
   "En el futuro me gustaría jugar en el equipo del condado. En España el fútbol gaélico no es muy conocido, pero hay algunos clubes, por ejemplo en Madrid y en Barcelona. ¡Muchas gracias por escuchar!"],
  qa=[
   ("¿Cuántas horas entrenas a la semana?", "Entreno unas tres horas a la semana, los martes y los jueves."),
   ("¿En qué posición juegas?", "Juego de defensa, pero me gustaría jugar de delantero."),
   ("¿Qué otros deportes practicas?", "También hago natación en verano y a veces juego al baloncesto con mis amigos."),
   ("¿Por qué prefieres el fútbol gaélico al fútbol?", "Porque es más rápido y puedes usar las manos. Además, es un deporte irlandés."),
   ("¿Qué hicisteis después de la final?", "Fuimos al club, comimos pizza y bailamos mucho."),
   ("¿Es caro jugar en tu club?", "No, no es caro. Pagamos cincuenta euros al año."),
  ],
  why=["A clear plan: what it is, me and the sport, a past event, the future, a link to Spain.",
       "Three time frames: <i>juego</i>, <i>ganamos / fue</i>, <i>me gustaría</i>.",
       "Opinions with reasons: <i>me encanta porque…</i>, <i>lo malo es que…</i>",
       "A prop (the jersey) gives the teacher easy things to ask about."]),

 dict(id="pres2", fmt="Presentation", title="Una fiesta de México: el Día de Muertos",
  who=["Niamh", "Profesora"],
  setup="Niamh shows three slides she made: a family altar, sugar skulls, and a Halloween photo from her town.",
  talk=[
   "Hola, me llamo Niamh. Hoy voy a hablar de una fiesta de México: el Día de Muertos.",
   "Se celebra el uno y el dos de noviembre. No es una fiesta triste: es un momento para recordar a las personas de la familia que ya murieron.",
   "Las familias preparan un altar en casa, que se llama ofrenda. En la ofrenda ponen fotos, velas, flores naranjas y la comida favorita de sus familiares. También hay un pan especial, el pan de muerto, y calaveras de azúcar de muchos colores. Por la noche, mucha gente va al cementerio con música y flores.",
   "En Irlanda celebramos Halloween el treinta y uno de octubre. Halloween viene de Samhain, una antigua fiesta celta. ¡Las dos fiestas son casi en las mismas fechas! En Halloween los niños se disfrazan y piden caramelos.",
   "Creo que el Día de Muertos es más bonito porque es una fiesta para la familia. Me gustaría ir a México un día para verlo. ¡Gracias!"],
  qa=[
   ("¿Qué hiciste el Halloween pasado?", "Me disfracé de bruja y fui a una fiesta en casa de mi amiga."),
   ("¿Qué comida hay en la ofrenda?", "Hay pan de muerto, fruta, calaveras de azúcar y la comida favorita de la persona."),
   ("¿Te gustaría probar el pan de muerto?", "Sí, me gustaría probarlo porque me encanta el pan dulce."),
   ("¿Dónde está México?", "Está en América del Norte, al sur de Estados Unidos."),
   ("¿Qué idioma se habla en México?", "Se habla español. Es el país con más hispanohablantes del mundo."),
   ("¿Qué fiesta prefieres?", "Prefiero el Día de Muertos porque es más tranquilo y familiar, pero Halloween es más divertido para los niños."),
  ],
  why=["Culture and comparison with Ireland: exactly what the oral CBA is about.",
       "Useful structures: <i>se celebra</i>, <i>que se llama</i>, <i>más bonito que</i>.",
       "Explains new words simply instead of reading long sentences.",
       "Ends with a personal opinion and a wish (<i>me gustaría…</i>)."]),

 dict(id="int1", fmt="Interview", title="Entrevista: mi vida",
  who=["Róisín", "Profesor"],
  setup="The teacher asks Róisín questions on familiar topics. In a pair interview, the students also ask each other.",
  qa=[
   ("¿Cómo te llamas y cuántos años tienes?", "Me llamo Róisín y tengo catorce años. Mi cumpleaños es el doce de mayo."),
   ("¿Dónde vives?", "Vivo en Galway, en el oeste de Irlanda. Vivo en una casa cerca del mar."),
   ("Háblame de tu familia.", "Somos cinco en mi familia: mis padres, mis dos hermanos y yo. Mi hermano mayor se llama Liam y es muy gracioso. También tenemos un perro, Bruno."),
   ("¿Cómo eres?", "Soy alta, tengo el pelo castaño y los ojos azules. Soy simpática y un poco habladora."),
   ("¿Qué asignaturas te gustan?", "Me encanta el español porque es útil y divertido. Pero no me gustan las matemáticas porque son difíciles."),
   ("¿Qué haces en tu tiempo libre?", "Toco la guitarra y hago natación dos veces a la semana. Los fines de semana salgo con mis amigas."),
   ("¿Qué hiciste el fin de semana pasado?", "El sábado fui al cine con mis amigas y vimos una película de miedo. El domingo comí con mis abuelos."),
   ("¿Cuál es tu comida favorita?", "Mi comida favorita es la pasta, pero también me gusta mucho la paella."),
   ("¿Has visitado España?", "Sí, el verano pasado fui a Valencia con mi familia. Hacía mucho calor y fuimos a la playa todos los días."),
   ("¿Qué vas a hacer este verano?", "Voy a ir a un campamento en Kerry y voy a trabajar en la tienda de mi tía."),
   ("¿Qué te gustaría hacer en el futuro?", "Me gustaría ser veterinaria porque me encantan los animales. También quiero vivir en España un año."),
   ("¿Por qué estudias español?", "Porque es un idioma muy importante: se habla en unos veinte países. Además, me gusta mucho la cultura española."),
  ],
  why=["Every answer goes one step further than the question: a detail, a reason or a second sentence.",
       "All three time frames: <i>vivo</i>, <i>fui / vimos</i>, <i>voy a ir / me gustaría</i>.",
       "Natural links: <i>pero</i>, <i>también</i>, <i>además</i>, <i>porque</i>.",
       "Short and clear. Nothing sounds learnt off like a speech."]),

 dict(id="rp1", fmt="Role-play", title="Role-play: en el hotel",
  who=["Darragh", "Recepcionista"],
  setup="Darragh arrives at a hotel in Málaga without a booking. The teacher plays the receptionist and uses <i>usted</i>.",
  lines=[
   (1, "Buenas tardes. ¿En qué puedo ayudarle?"),
   (0, "Buenas tardes. Quería una habitación doble para tres noches, por favor."),
   (1, "Muy bien. ¿Para cuándo?"),
   (0, "Para esta noche, hasta el viernes."),
   (1, "Tenemos una habitación con vistas al mar. Cuesta noventa euros por noche."),
   (0, "¿El desayuno está incluido?"),
   (1, "Sí, el desayuno está incluido. Es de siete y media a diez."),
   (0, "Perfecto. ¿Hay wifi en la habitación?"),
   (1, "Sí, la contraseña está en la habitación. ¿Su nombre, por favor?"),
   (0, "Me llamo Darragh Murphy. Se escribe D, A, R, R, A, G, H."),
   (1, "Gracias. Aquí tiene la llave. Es la habitación ciento doce, en el primer piso."),
   (0, "¿Dónde está el ascensor?"),
   (1, "Está a la derecha, al lado del restaurante."),
   (0, "¿Hay piscina?"),
   (1, "Sí, en la terraza. Está abierta hasta las nueve de la noche."),
   (0, "¡Genial! Muchas gracias. Hasta luego."),
  ],
  qa=[
   ("¿Prefieres un hotel o un camping? ¿Por qué?", "Prefiero un hotel porque es más cómodo y hay piscina."),
   ("¿Adónde fuiste de vacaciones el año pasado?", "Fui a Kerry con mi familia. Nos quedamos en una casa cerca de la playa."),
   ("¿Qué te gusta hacer en las vacaciones?", "Me gusta nadar, comer en restaurantes y dormir mucho."),
  ],
  why=["Polite forms: <i>quería…</i>, <i>por favor</i>, <i>muchas gracias</i>.",
       "Asks questions as well as answering them: that is spoken interaction.",
       "Spells his name with Spanish letter names (practise the alphabet!).",
       "Handles numbers in context: nights, prices, times, a room number."]),

 dict(id="rp2", fmt="Role-play", title="Role-play: con la familia de intercambio",
  who=["Aoife", "Señora García"],
  setup="Aoife arrives in Salamanca for an exchange. The teacher plays her host mother, Señora García.",
  lines=[
   (1, "¡Hola, Aoife! Bienvenida a Salamanca. ¿Qué tal el viaje?"),
   (0, "Muy bien, gracias, pero estoy un poco cansada. El avión salió a las seis de la mañana."),
   (1, "¡Qué temprano! ¿Tienes hambre?"),
   (0, "Sí, un poco. ¿A qué hora es la cena?"),
   (1, "Cenamos a las nueve y media. ¿Hay algo que no comes?"),
   (0, "Como de todo, pero no me gusta mucho el pescado."),
   (1, "No pasa nada. Esta noche hay tortilla de patatas."),
   (0, "¡Qué bien! Me encanta la tortilla. ¿Puedo llamar a mis padres?"),
   (1, "Claro. ¿Quieres la contraseña del wifi?"),
   (0, "Sí, por favor. ¿Y dónde está el baño?"),
   (1, "Al final del pasillo, a la izquierda. Mañana vamos a visitar la Plaza Mayor."),
   (0, "¡Perfecto! Tengo un regalo de Irlanda para ustedes: chocolate irlandés."),
   (1, "¡Muchas gracias, qué amable!"),
  ],
  qa=[
   ("¿Te gustaría hacer un intercambio? ¿Por qué?", "Sí, me gustaría porque quiero hablar español todos los días."),
   ("¿A qué hora cenas normalmente?", "Normalmente ceno a las seis. ¡En España cenan muy tarde!"),
   ("¿Qué comida irlandesa te gusta?", "Me gusta mucho el estofado irlandés y el pan de soda de mi abuela."),
  ],
  why=["Cultural awareness: Spanish dinner times, and a small gift for the host family.",
       "Feelings and reasons: <i>estoy un poco cansada</i>, <i>no me gusta mucho…</i>",
       "Reacts naturally: <i>¡Qué bien!</i>, <i>¡Perfecto!</i>",
       "Practical questions with <i>¿Puedo…?</i> and <i>¿Dónde está…?</i>"]),

 dict(id="stim1", fmt="Conversation", title="Conversation about a picture: un mercado",
  who=["Oisín", "Profesora"],
  setup="The teacher shows Oisín a picture of a fruit stall at a market (see the picture card) and talks with him about it.",
  lines=[
   (1, "¿Qué hay en la foto?"),
   (0, "En la foto hay un mercado. Creo que está en España porque los carteles están en español."),
   (1, "¿Qué se puede comprar?"),
   (0, "Se puede comprar fruta: naranjas, manzanas y plátanos. Las naranjas están a un euro cincuenta el kilo."),
   (1, "¿Quién está en la foto?"),
   (0, "A la izquierda hay una vendedora. Lleva un delantal verde y sonríe. A la derecha hay un chico y una chica. La chica lleva una bolsa."),
   (1, "¿Qué tiempo hace?"),
   (0, "Hace sol y hace calor. Creo que es verano."),
   (1, "¿Te gusta ir al mercado?"),
   (0, "Sí, me gusta. En mi ciudad hay un mercado los sábados. El sábado pasado compré fresas y pan con mi madre."),
   (1, "¿Qué fruta prefieres?"),
   (0, "Prefiero las fresas porque son dulces. No me gustan los plátanos."),
   (1, "¿Comes bien?"),
   (0, "Creo que sí. Como mucha fruta, pero me encanta el chocolate también."),
  ],
  qa=[],
  why=["Describes in a clear order: what, who, where (<i>a la izquierda / a la derecha</i>), the weather.",
       "Gives a guess with a reason: <i>creo que… porque…</i>",
       "Moves from the picture to his own life, with a past event.",
       "Prices and numbers said aloud correctly."]),
]

QBANK = [
 ("Yo y mi familia", [
  ("¿Cómo te llamas?", "Me llamo…"), ("¿Cuántos años tienes?", "Tengo … años."),
  ("¿Cuándo es tu cumpleaños?", "Mi cumpleaños es el … de …"), ("¿Cuántas personas hay en tu familia?", "Somos … / En mi familia hay…"),
  ("¿Cómo es tu mejor amigo?", "Mi mejor amigo es… / Mi mejor amiga es…"), ("¿Tienes mascotas?", "Sí, tengo… / No, no tengo…")]),
 ("Mi casa y mi pueblo", [
  ("¿Dónde vives?", "Vivo en…, en el norte / sur / este / oeste de…"), ("¿Cómo es tu casa?", "Mi casa es… y tiene…"),
  ("¿Cómo es tu habitación?", "En mi habitación hay…"), ("¿Qué se puede hacer en tu pueblo?", "Se puede…"),
  ("¿Te gusta vivir allí?", "Sí, me gusta porque… / No mucho, porque…"), ("¿Qué hay cerca de tu casa?", "Cerca de mi casa hay…")]),
 ("El colegio", [
  ("¿Qué asignaturas estudias?", "Estudio…"), ("¿Cuál es tu asignatura favorita?", "Mi asignatura favorita es… porque…"),
  ("¿Qué asignatura no te gusta?", "No me gusta… porque…"), ("¿Cómo vas al colegio?", "Voy en autobús / en coche / a pie."),
  ("¿A qué hora empiezan las clases?", "Las clases empiezan a las…"), ("¿Qué hiciste ayer en el colegio?", "Ayer tuve… / estudié… / jugué…")]),
 ("Tiempo libre", [
  ("¿Qué haces en tu tiempo libre?", "En mi tiempo libre…"), ("¿Practicas algún deporte?", "Sí, juego al… / hago…"),
  ("¿Qué música te gusta?", "Me gusta… Mi cantante favorito es…"), ("¿Qué hiciste el fin de semana pasado?", "El sábado fui… / El domingo…"),
  ("¿Qué vas a hacer este fin de semana?", "Voy a…"), ("¿Te gusta leer?", "Sí, me encanta… / No mucho, prefiero…")]),
 ("Rutina y comida", [
  ("¿A qué hora te levantas?", "Me levanto a las…"), ("¿Qué desayunas?", "Desayuno… / Normalmente tomo…"),
  ("¿Cuál es tu comida favorita?", "Mi comida favorita es…"), ("¿Ayudas en casa?", "Sí, pongo la mesa / paso la aspiradora…"),
  ("¿Qué comiste ayer?", "Ayer comí…"), ("¿Te gusta cocinar?", "Sí, sé hacer… / No, pero…")]),
 ("Las vacaciones", [
  ("¿Adónde vas de vacaciones normalmente?", "Normalmente voy a…"), ("¿Adónde fuiste el verano pasado?", "Fui a… con…"),
  ("¿Qué hiciste allí?", "Nadé, visité…, comí…"), ("¿Qué tiempo hizo?", "Hizo sol / Hizo calor / Llovió…"),
  ("¿Qué vas a hacer este verano?", "Este verano voy a…"), ("¿Prefieres la playa o la montaña?", "Prefiero… porque…")]),
 ("El futuro", [
  ("¿Qué te gustaría ser en el futuro?", "Me gustaría ser…"), ("¿Dónde te gustaría vivir?", "Me gustaría vivir en… porque…"),
  ("¿Vas a seguir estudiando español?", "Sí, voy a… / No estoy seguro…"), ("¿Qué país te gustaría visitar?", "Me gustaría visitar… porque…"),
  ("¿Trabajas los fines de semana?", "Sí, trabajo en… / No, pero me gustaría…"), ("¿Qué vas a hacer después de los exámenes?", "Voy a…")]),
 ("España y Latinoamérica", [
  ("¿Has visitado algún país hispanohablante?", "Sí, fui a… / No, pero me gustaría ir a…"), ("¿Qué sabes de España?", "España está en… La capital es…"),
  ("¿Conoces alguna fiesta española?", "Sí, conozco las Fallas / la Tomatina…"), ("¿Te gusta la comida española?", "Sí, me encanta… / Nunca he probado…"),
  ("¿Conoces a algún deportista hispano?", "Sí, … es de…"), ("¿Por qué estudias español?", "Porque…")]),
]

SURVIVAL = [
 ("¿Puede repetir, por favor?", "Can you repeat that, please?"),
 ("Más despacio, por favor.", "More slowly, please."),
 ("No entiendo la pregunta.", "I don't understand the question."),
 ("¿Qué significa «…»?", "What does … mean?"),
 ("¿Cómo se dice «…» en español?", "How do you say … in Spanish?"),
 ("Perdón, quiero decir…", "Sorry, I mean… (fixing your own mistake)"),
]
FILLERS = "Pues… · A ver… · Bueno… · Es una buena pregunta. · Creo que… · No estoy seguro / segura, pero…"
LINKS = "porque · pero · también · además · por ejemplo · sin embargo · y luego"
OPINIONS = "En mi opinión… · Creo que… · Me encanta… · Lo mejor es… · Lo malo es… · Prefiero… porque…"
TENSES = "Normalmente… (present) · El año pasado… / Ayer… (past) · El año que viene voy a… (future) · Me gustaría… (wish)"

LADDERS = [
 ("¿Qué haces en tu tiempo libre?",
  "Juego al fútbol.",
  "Juego al fútbol con mis amigos porque es divertido.",
  "Juego al fútbol con mis amigos dos veces a la semana porque es muy divertido. El sábado pasado marqué un gol y ganamos. ¡Fue genial! El año que viene voy a jugar en el equipo del colegio."),
 ("¿Cómo es tu casa?",
  "Es grande.",
  "Mi casa es grande y tiene un jardín bonito.",
  "Vivo en una casa bastante grande en las afueras. Tiene cuatro habitaciones y un jardín donde juego con mi perro. Lo mejor es mi habitación, porque tiene vistas al mar. En el futuro me gustaría vivir en un piso en la ciudad."),
]

PRON = [
 ("Vowels", "<i>a e i o u</i> are always short and clear: <i>me-sa</i>, <i>pe-lo</i>. Never swallow them."),
 ("h", "is silent: <i>hola</i> = \"ola\", <i>hago</i> = \"ago\"."),
 ("j, ge, gi", "a breathy sound from the throat: <i>jugar</i>, <i>gente</i>, <i>Jorge</i>."),
 ("ll and y", "sound like the y in \"yes\": <i>me llamo</i>, <i>playa</i>."),
 ("ñ", "like \"ny\" in \"canyon\": <i>España</i>, <i>año</i>."),
 ("r and rr", "one quick tap in <i>pero</i> (but); a roll in <i>perro</i> (dog) and at the start of a word: <i>Roma</i>."),
 ("z, ce, ci", "\"th\" in most of Spain, \"s\" in Latin America: <i>cinco</i>, <i>zapato</i>. Both are right; pick one."),
 ("v", "sounds like b: <i>vivo</i>, <i>verano</i>."),
 ("qu", "is a k sound: <i>queso</i>, <i>¿qué?</i>"),
 ("Stress", "Words ending in a vowel, n or s: stress the second-last syllable (<i>ha-blo</i>, <i>ha-blan</i>). Others: the last (<i>ha-blar</i>, <i>ciu-dad</i>). An accent shows an exception: <i>música</i>, <i>inglés</i>."),
 ("Lookalike words", "Say them the Spanish way: <i>hotel</i> (no h), <i>chocolate</i> (cho-co-LA-te), <i>animal</i> (a-ni-MAL)."),
]

MISTAKES = [
 ("Soy catorce años.", "Tengo catorce años."),
 ("Me gusta los perros.", "Me gustan los perros."),
 ("Es frío hoy.", "Hoy hace frío."),
 ("Soy cansado.", "Estoy cansado."),
 ("Fui a la playa y es genial.", "Fui a la playa y fue genial."),
 ("Mi madre es profesor.", "Mi madre es profesora."),
 ("Juego fútbol.", "Juego al fútbol."),
 ("En el fin de semana…", "El fin de semana…"),
 ("Um… like…", "Pues… / Bueno… / A ver…"),
]

IDEAS = {
 "Presentation": ["my sport, team or hobby", "a festival in a Spanish-speaking country (compare it with Ireland)",
                  "a Spanish or Latin American city you'd like to visit", "a famous Spanish-speaking person",
                  "my town for Spanish visitors", "a typical day in a Spanish school vs mine",
                  "food from a Spanish-speaking country (a recipe with props)"],
 "Interview": ["me, my family and my free time", "my school and my plans", "my holidays: last year and this year",
               "a pair interview: two friends compare their lives"],
 "Role-play": ["booking into a hotel or campsite", "arriving at a host family", "buying clothes or souvenirs",
               "ordering in a café or restaurant", "at the tourist office or train station", "at the doctor's"],
 "Conversation": ["a photo of a market, beach, street or festival", "a poster or menu", "a short video clip",
                  "an object you bring in (a souvenir, a jersey)"],
}

PLAN3 = [
 ("Before", "Speak Spanish in class every week. Learn the question bank (page 11) a topic at a time."),
 ("Day 1", "Choose your format and topic with your teacher. It must be one you haven't already practised or prepared, so use the models in this pack to learn HOW, then make your own."),
 ("Week 1", "Research: two or three sources (a website, a video, a book). Write down key words. Make a mind map and a plan (page 14)."),
 ("Week 2", "Build your talk or role-play in short, simple sentences. Practise aloud every day; record yourself on your phone and listen back. Prepare answers to 8–10 likely questions."),
 ("Week 3", "Practise with a friend or parent who asks you questions in a different order. Time it: about 3–4 minutes, including the questions. Use the survival phrases."),
 ("After", "Write your Student Reflection Note (page 15) in your own words."),
]

SELFCHECK = [
 "I can speak for about 3–4 minutes (including the teacher's questions) without reading.",
 "My talk has a clear start, middle and end.",
 "I use at least three time frames: present, past and future (or <i>me gustaría</i>).",
 "I give opinions with reasons (<i>porque…</i>).",
 "I join sentences with <i>y, pero, también, además</i>.",
 "I can answer my 10 likely questions with two sentences each.",
 "I can ask for help in Spanish (<i>¿Puede repetir, por favor?</i>).",
 "I've checked my pronunciation of the tricky words (page 13).",
 "I've said it out loud to someone at home at least three times.",
 "I've included something about a Spanish-speaking country or culture (if it fits).",
]

REFLECT = [
 "How did I prepare? What did I use from my Spanish classes?",
 "What did I do in the CBA? (my part, if I worked with others)",
 "Which materials or sources did I use?",
 "One important thing I learned.",
 "What would I change or improve next time?",
]
