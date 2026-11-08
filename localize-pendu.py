from pathlib import Path
import re,base64,json,subprocess
root=Path('/workspace/sites/cualigrafia-en-ru')
src=(root/'source/pendu.es.html').read_text()
# The source uses a custom base64 alphabet for its string table. Keep table order,
# executable names and checksum data intact; only replace human-readable copy.
custom='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'
standard='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
def decode(v):return base64.b64decode(v.translate(str.maketrans(custom,standard))+'===').decode()
def encode(v):return base64.b64encode(v.encode()).decode().rstrip('=').translate(str.maketrans(standard,custom))
rows=[
('La pendular: glúteo o cuádriceps','Pendulum squat: glutes or quadriceps','Маятниковый присед: ягодицы или квадрицепс'),
('La pendular.','Pendulum squat.','Маятниковый присед.'),
('Pero bien explicada','The mechanics, explained','Механика простыми словами'),
('Cualigrafía. Pulsa para la sorpresa','Cualigrafía. Press for a surprise','Cualigrafía. Нажмите для сюрприза'),
('Simulación','Simulation','Симуляция'),
('Persona de perfil en una sentadilla pendular. Se ve la línea por la que pasa el empuje, su distancia a la rodilla y a la cadera, los músculos que se encienden según trabajan y dónde te sujetan hombreras, respaldo y cinturón.','Side view of a person in a pendulum squat machine. The simulation shows the line of force, its distance from the knee and hip, working muscles, and support from the shoulder pads, backrest and belt.','Вид сбоку на человека в маятниковом тренажёре. Показаны линия действия силы, её расстояние до коленного и тазобедренного суставов, работающие мышцы и опора на подплечники, спинку и ремень.'),
('Mover el brazo de la máquina: subir o bajar. Usa las flechas del teclado.','Move the machine arm up or down. Use the arrow keys.','Перемещайте рычаг тренажёра вверх или вниз. Используйте клавиши со стрелками.'),
('Subir o bajar los pies por la plataforma. Usa las flechas del teclado.','Move the feet up or down the platform. Use the arrow keys.','Перемещайте стопы выше или ниже по платформе. Используйте клавиши со стрелками.'),
('Inclinar el empuje, del cuádriceps al glúteo. Usa las flechas del teclado.','Change the direction of force, from quadriceps to glutes. Use the arrow keys.','Меняйте направление усилия, смещая нагрузку с квадрицепса на ягодицы. Используйте клавиши со стрелками.'),
('Poner el vídeo: repeticiones en bucle','Play repeating movement','Запустить повторение движения'),
('Parar el vídeo','Stop animation','Остановить анимацию'),
('Cinturón','Belt','Ремень'),
('Mansplaining activado','Explanation on','Пояснения включены'),
('Mansplaining desactivado','Explanation off','Пояснения выключены'),
('Patorras','Quadriceps','Квадрицепс'),
('Culazo','Glutes','Ягодицы'),
('Reparto del esfuerzo: de patorras (cuádriceps) a culazo (glúteo)','Effort distribution: quadriceps to glutes','Распределение усилия: от квадрицепса к ягодицам'),
('Mensajes','Explanations','Пояснения'),
('Tarjeta anterior','Previous explanation','Предыдущее пояснение'),
('Tarjeta siguiente','Next explanation','Следующее пояснение'),
('Continuar','Continue','Продолжить'),
('¿Qué haces tú?','What do you do?','Что будете делать?'),
('Le cargo 40 kg más','Add another 40 kg','Добавить ещё 40 кг'),
('Lanzo al suelo un botecito de cristal que pone «testotrembo3000»','Drop a little glass bottle labelled “testotrembo3000”','Бросить на пол пузырёк с надписью «testotrembo3000»'),
('Le empujo hacia abajo para que haga el recorrido completo','Push him down so he uses the full range of motion','Толкнуть его вниз, чтобы он прошёл полную амплитуду'),
('Volver a empezar','Start again','Начать заново'),
('Salir','Exit','Выйти'),
('Más info','How the model works','Как устроена модель'),
('Más ejercicios','More exercises','Другие упражнения'),
('¿Quién ha hecho esto?','About the original creator','Об авторе оригинала'),
('No pulses aquí','Do not press here','Не нажимайте сюда'),
('Cerrar','Close','Закрыть'),
('¿Te está gustando?','Enjoying this?','Вам нравится?'),
('¿Te diviertes moviendo las flechitas?','Having fun moving the arrows?','Нравится двигать стрелки?'),
('¿Un proyecto en mente?','About the creator','Об авторе'),
('Más','More','Подробнее'),
(' La pelvis quiere despegarse.',' The pelvis tends to lift off the backrest.',' Таз стремится оторваться от спинки.'),
(' Empuja la barriga contra el cinturón: así sujeta la pelvis.',' Push your abdomen into the belt to keep the pelvis supported.',' Надавите животом на ремень: так он удержит таз.'),
('Con un cinturón, podrías empujar con el culo como si fuera un hip thrust.','With a belt, you could drive through your glutes as in a hip thrust.','С ремнём можно сильнее включить ягодицы, как в ягодичном мосте.'),
('Glúteo mayor','Gluteus maximus','Большая ягодичная'),
('glúteo','glutes','ягодицы'),
('Sóleo','Soleus','Камбаловидная'),
('sóleo','soleus','камбаловидная'),
('Recto femoral','Rectus femoris','Прямая мышца бедра'),
('recto femoral','rectus femoris','прямая мышца бедра'),
('Vastos','Vasti','Широкие мышцы бедра'),
('Gemelos','Gastrocnemius','Икроножные'),
('Isquiotibiales','Hamstrings','Задняя поверхность бедра'),
('Empuja perpendicular a la plataforma, como si fuera de hielo y no quisieras resbalarte.','Push perpendicular to the platform, as if it were icy and you wanted to avoid slipping.','Давите перпендикулярно платформе, словно она покрыта льдом и вы не хотите поскользнуться.'),
('Máxima palanca en el glúteo. Clava los pies como si arrastraras la plataforma hacia ti. Moverás menos peso: tu empuje pasa más cerca del pivote.','Maximum glute moment arm. Dig your feet in as if pulling the platform towards you. You will move less weight: your line of force passes closer to the pivot.','Максимальное плечо силы для ягодиц. Упритесь стопами, словно тянете платформу к себе. Рабочий вес будет меньше: линия усилия проходит ближе к оси вращения.'),
('¡Oh, no! El máquina de tu gimnasio está con cinco gymbros en la pendular. Ya lleva 20 repeticiones con un recorrido de 15 cm. Mientras, todos le ayudan a mover esos 200 kg.','Oh no! The gym superstar has five gym buddies around the pendulum machine. He has done 20 reps through just 15 cm of movement, while everyone helps him move 200 kg.','О нет! Звезда вашего зала окружена пятью приятелями у маятникового тренажёра. Уже 20 повторений с амплитудой 15 см, пока все помогают двигать эти 200 кг.'),
('Basta de chorradas.','Back to the essentials.','Вернёмся к главному.'),
(' Tu empuje pasa más cerca del pivote: necesitas más fuerza para mover lo mismo.',' Your line of force passes closer to the pivot: you need more force to move the same load.',' Линия усилия проходит ближе к оси вращения: для того же веса нужно больше силы.'),
('Notarás las hombreras y el respaldo en media espalda.','You will feel the shoulder pads and the backrest against your mid-back.','Вы почувствуете подплечники и давление спинки в средней части спины.'),
('También importa la intención con la que empujas la plataforma.','The direction in which you try to push the platform also matters.','Важно и то, в каком направлении вы стараетесь давить на платформу.'),
('Máxima palanca para tus cuádriceps. Podrás mover menos peso.','Maximum quadriceps moment arm. You will be able to move less weight.','Максимальное плечо силы для квадрицепса. Рабочий вес будет меньше.'),
('Clava los pies rampa abajo, como si arrastraras la plataforma hacia ti. Si alguien hubiera echado aceite, resbalarías hacia el talón.','Drive your feet down the ramp, as if pulling the platform towards you. If the surface were oily, your feet would slip towards your heels.','Давите стопами вниз по наклонной платформе, словно тянете её к себе. На скользкой поверхности стопы поехали бы в сторону пяток.'),
('Si intentas clavar los pies rampa abajo, como si arrastraras la plataforma hacia ti, puedes activar más el culo. Pero no es cómodo, y necesitarás una cincha que te sujete la cadera al respaldo (luego lo vemos).','Trying to drive your feet down the ramp, as if pulling the platform towards you, can shift more effort to your glutes. But it is uncomfortable, and you will need a belt to hold your pelvis against the backrest (more on that later).','Если давить стопами вниз по платформе, словно тянуть её к себе, нагрузка сильнее смещается на ягодицы. Но это неудобно, и понадобится ремень, удерживающий таз у спинки (к этому ещё вернёмся).'),
('GAME OVER\\nLos gymbros se han lanzado a por el bote y se han ido corriendo al vestuario. El máquina se ha quedado abajo y te toca a ti recoger los discos.','GAME OVER\\nThe gym buddies grab the bottle and run to the changing room. The superstar is stuck at the bottom, and you have to unload the plates.','ИГРА ОКОНЧЕНА\\nПриятели хватают пузырёк и бегут в раздевалку. Звезда зала застряла внизу, а вам досталось снимать блины.'),
(' Sin cinturón, hasta aquí: con más glúteo la pelvis se despegaría.',' This is the limit without a belt: more glute effort would lift the pelvis off the backrest.',' Без ремня это предел: при большем усилии ягодиц таз оторвётся от спинки.'),
('Tu empuje hace girar el brazo alrededor del pivote. Cuanto más lejos del pivote pasa la línea, menos fuerza hace falta.','Your push rotates the arm around the pivot. The farther the line of force passes from the pivot, the less force you need.','Ваше усилие поворачивает рычаг вокруг оси. Чем дальше от оси проходит линия усилия, тем меньше силы требуется.'),
('Notarás las hombreras y el respaldo en la zona baja de la espalda.','You will feel the shoulder pads and the backrest against your lower back.','Вы почувствуете подплечники и давление спинки в нижней части спины.'),
('Empuja la plataforma rampa arriba. Si fuera de hielo, tus pies se irían hacia la punta.','Push up the ramp. If the platform were icy, your feet would slip towards your toes.','Давите вверх по наклонной платформе. На льду стопы поехали бы в сторону носков.'),
('Movimiento natural. Empuja todo lo que puedas y te moverás en esta zona.','Natural movement. Push as hard as you can and you will move within this region.','Естественное движение. Давите изо всех сил — движение будет в этой области.'),
(' La suela va casi al límite de agarre.',' The soles are close to their grip limit.',' Подошвы почти на пределе сцепления.'),
(' Sin cinturón la pelvis se despegaría: empuja la barriga contra el cinturón y queda sujeta.',' Without a belt the pelvis would lift off: push your abdomen into the belt to keep it supported.',' Без ремня таз оторвётся: надавите животом на ремень, чтобы удержать его.'),
('En la pendular puedes poner los pies más arriba o más abajo en la plataforma.','On a pendulum squat machine you can place your feet higher or lower on the platform.','В маятниковом тренажёре можно ставить стопы выше или ниже на платформе.'),
('Está muy bien entender todo esto, pero lo importante es otra cosa: usar una técnica que te permita bajar bien y empujar con seguridad, coger cada vez más peso y hacerte cada vez más fuerte.','Understanding this is useful, but the essentials are a technique that lets you descend comfortably and push safely, gradually increase the load, and grow stronger.','Понимать всё это полезно, но главное — техника, которая позволяет комфортно опускаться и безопасно подниматься, постепенно увеличивать нагрузку и становиться сильнее.'),
('GAME OVER\\nLos gymbros se han desmayado del esfuerzo y el máquina se ha quedado abajo. Te toca recoger los discos.','GAME OVER\\nThe gym buddies collapse from the effort and the superstar is stuck at the bottom. You have to unload the plates.','ИГРА ОКОНЧЕНА\\nПриятели падают от усталости, а звезда зала застревает внизу. Вам досталось снимать блины.'),
('Si empujas más arriba, llega un punto en que la pelvis quiere despegarse. Sin cinturón, ese es tu tope.','If you push higher up, eventually the pelvis tends to lift off the backrest. Without a belt, that is your limit.','Если направлять усилие выше, в какой-то момент таз начнёт отрываться от спинки. Без ремня это ваш предел.'),
('Si empujas la plataforma hacia delante, activas más las piernas. Esto es lo más natural en esta máquina.','Pushing the platform forwards shifts more effort to the quadriceps. This is the most natural action on this machine.','Если давить на платформу вперёд, нагрузка сильнее смещается на квадрицепс. Для этого тренажёра такое движение наиболее естественно.'),
('Llega hasta abajo y los gymbros le ayudan a subir mientras le gritan: «¡Vas tú solo, bro!»','He reaches the bottom and his gym buddies help him up while shouting, “All you, bro!”','Он опускается до конца, а приятели помогают ему подняться, крича: «Сам, брат, всё сам!»'),
('Notarás las hombreras y el respaldo en la parte alta de la espalda. La pelvis quiere despegarse.','You will feel the shoulder pads and the backrest against your upper back. The pelvis tends to lift off.','Вы почувствуете подплечники и давление спинки в верхней части спины. Таз стремится оторваться.'),
('Los gymbros empiezan a sudar, pero él sigue haciendo repes. Ya lleva ','The gym buddies start sweating, but he keeps going. He has now done ','Приятели уже потеют, а он продолжает. Уже выполнено повторений: '),
('Si empujas más hacia el pivote, cuesta mucho más. Mira cómo se hace más grande la flecha naranja.','Pushing more towards the pivot makes the movement much harder. Notice how the orange arrow gets larger.','Если направить усилие ближе к оси вращения, двигаться станет гораздо тяжелее. Посмотрите, как увеличивается оранжевая стрелка.'),
('Ni con cinturón: el respaldo no puede sujetarte con este empuje.','Even with a belt, the backrest cannot support this direction of force.','Даже с ремнём спинка не удержит вас при таком направлении усилия.'),
('La pelvis se despega del respaldo. Con cinturón podrías seguir.','The pelvis lifts off the backrest. A belt would let you continue.','Таз отрывается от спинки. С ремнём можно продолжить.'),
('Si los bajas mucho, quizá no puedas doblar tanto el tobillo. Busca comodidad y profundidad.','If you place your feet too low, your ankles may not bend enough. Find a comfortable position that allows depth.','Если поставить стопы слишком низко, подвижности голеностопа может не хватить. Ищите удобное положение и достаточную глубину.'),
('En la pendular no levantas un peso: empujas una palanca.','On a pendulum machine, you push a lever rather than lift a weight directly.','В маятниковом тренажёре вы давите на рычаг, а не поднимаете вес напрямую.'),
('Puedes centrarte en empujar el respaldo: cuanto más abajo lo empujes, más trabajarás los cuádriceps.','Focus on pushing against the backrest: the lower you push, the more your quadriceps work.','Сосредоточьтесь на давлении на спинку: чем ниже точка давления, тем сильнее работают квадрицепсы.'),
('MARGEN','MARGIN','ЗАПАС'),
(' REPS',' REPS',' ПОВТ.'),
(' KG · ',' KG · ',' КГ · '),
]
info=[
('Modelo.','Model.','Модель.'),
(' Es un modelo de perfil, con huesos rígidos y movimiento lento. Los pies van fijos en la plataforma y la cadera fija al respaldo, que gira con el brazo de la máquina. Lo que trabaja cada músculo se toma como el giro que el empuje provoca en su articulación: fuerza × brazo de palanca, contando lo que pesan tus propias piernas.',' This is a side-view model with rigid bones and slow movement. The feet stay fixed on the platform and the hip stays against the backrest, which rotates with the machine arm. Muscle demand is estimated from the torque around each joint: force × moment arm, including the weight of your legs.',' Это модель сбоку с жёсткими костными сегментами и медленным движением. Стопы закреплены на платформе, таз — у спинки, которая вращается вместе с рычагом тренажёра. Нагрузка на мышцы оценивается по моменту силы в суставе: сила × плечо силы, с учётом веса ног.'),
('Máquina.','Machine.','Тренажёр.'),
(' Geometría estimada de una Gymleco 045 a partir de fotos y de su ficha (resistencia inicial de 23 kg arriba y 17 abajo). Con 20 kg por lado sientes unos 80 kg en los hombros, y las piernas mueven además tu tronco y tus muslos.',' Geometry estimated from photographs and specifications of a Gymleco 045 (initial resistance of 23 kg at the top and 17 kg at the bottom). With 20 kg per side, the shoulder load is about 80 kg; your legs also move your torso and thighs.',' Геометрия оценена по фотографиям и характеристикам Gymleco 045 (начальное сопротивление 23 кг сверху и 17 кг снизу). При 20 кг с каждой стороны нагрузка на плечи составляет около 80 кг; ноги также перемещают туловище и бёдра.'),
('Músculos.','Muscles.','Мышцы.'),
(' «Glúteo» agrupa a todo lo que extiende la cadera; los isquios también ayudan ahí. El gemelo y el resto de músculos se dejan fuera para simplificar.',' “Glutes” represents all hip extensors; the hamstrings also contribute. Calves and other muscles are omitted for simplicity.',' «Ягодицы» здесь объединяют все разгибатели тазобедренного сустава; мышцы задней поверхности бедра тоже помогают. Икроножные и остальные мышцы исключены для упрощения.'),
('Azul.','Blue.','Синий цвет.'),
(' Es el apoyo del tronco. Hombreras y cinturón se tiñen de azul según lo que aprietan. Las flechas azules marcan hacia dónde empujas tú: las hombreras hacia arriba y el respaldo hacia atrás, a la altura donde aprieta. La flecha negra del cinturón es tu barriga empujando contra él. El respaldo solo puede empujar dentro de tu espalda; por eso, sin cinturón, hay un tope de glúteo. Entra solo cuando hace falta; con el botón «Cinturón» lo dejas puesto o quitado.',' Blue shows torso support. The shoulder pads and belt turn blue according to pressure. Blue arrows show where you push: up against the shoulder pads and back against the backrest at the point of contact. The black belt arrow shows your abdomen pressing into it. The backrest can only push against your back, so glute emphasis has a limit without a belt. The belt engages when needed; the Belt button lets you keep it on or off.',' Синий показывает опору туловища. Подплечники и ремень окрашиваются в синий по мере роста давления. Синие стрелки показывают, куда вы давите: вверх на подплечники и назад на спинку в точке контакта. Чёрная стрелка у ремня — давление живота на него. Спинка может лишь давить на спину, поэтому без ремня акцент на ягодицах ограничен. Ремень включается при необходимости; кнопкой «Ремень» можно оставить его включённым или выключенным.'),
('Pivote.','Pivot.','Ось вращения.'),
(' La flecha naranja engorda con la fuerza que necesitas. Cuando la línea de empuje se acerca al pivote, aparece su palanca en gris: cuanto más corta, más fuerza para mover lo mismo.',' The orange arrow grows thicker as the required force increases. When the line of force approaches the pivot, its moment arm appears in grey: the shorter it is, the more force is needed for the same load.',' Оранжевая стрелка становится толще с ростом необходимой силы. Когда линия усилия приближается к оси вращения, серым появляется плечо силы: чем оно короче, тем больше силы нужно для той же нагрузки.'),
('Alcance.','Scope.','Ограничения.'),
(' Sirve para entender tendencias, no para medir a una persona concreta.',' This model illustrates trends; it does not measure an individual person.',' Модель помогает понять общие закономерности, но не предназначена для измерений у конкретного человека.'),
]
rows+=info
# Remove the external mailing integration entirely before translating.
src=re.sub(r'<script>\(function\(\)\{\s*var ACTION.*?</script>','',src,flags=re.S)
src=re.sub(r'<iframe name="mlFrame".*?</iframe>','',src,flags=re.S)
src=re.sub(r'<div class="subform">.*?<p class="subMsg".*?</p></div>','<p><a href="./index.html">CG_MORE</a></p>',src,flags=re.S)
src=re.sub(r'<div class="dd" id="dd-who" hidden>.*?</div>','<div class="dd" id="dd-who" hidden><p>CG_CREDIT <a href="https://cualigrafia.com/" target="_blank" rel="noopener">Cualigrafía · Pablo</a></p></div>',src,flags=re.S)
src=src.replace('https://cualigrafia.com/wp-content/uploads/2024/12/134cce47-7636-40ee-99b1-ab26c0ec2040.png','../assets/logo.png')
css='''<style>.locale-nav{max-width:904px;margin:16px auto 0;padding:0 14px;display:flex;justify-content:space-between;gap:20px;font:500 13px/1.5 Inter,Arial,sans-serif}.locale-nav a{color:#a0a0a8;text-decoration:none}.locale-nav a:hover,.locale-nav a[aria-current]{color:#f6c915}.locale-nav .languages{display:flex;gap:16px}.sheet{display:none!important}.pageTitle{overflow-wrap:normal;font-size:clamp(24px,5vw,44px)}.top{gap:12px}.logo{max-width:25%}.logo img{max-width:100%;object-fit:contain}.xsw .xl{max-width:120px}.hipbtn{font-size:12px}.gtext,.gq,.gopt{font-family:ui-monospace,monospace}.splitlab{gap:20px}.row p,.ts{overflow-wrap:anywhere}@media(max-width:480px){.pageTitle{font-size:27px}.logo{height:54px}.panel{padding:16px 14px}.row p{font-size:15px}.tt{font-size:17px}.ts{font-size:15px}.top{min-height:80px}}</style>'''
for lang,col in [('en',1),('ru',2)]:
 mapping={x[0]:x[col] for x in rows}
 source=src
 # Translate encoded values without changing decoder keys or other literals.
 def array_replace(m):
  def one(q):
   try:d=decode(q[1])
   except:return q[0]
   return "'"+encode(mapping[d])+"'" if d in mapping else q[0]
  return re.sub(r"'([^']*)'",one,m[0])
 source=re.sub(r"const _0xf5eb1a=\[.*?\];",array_replace,source)
 # Translate escaped JS literals independently; JSON quoting avoids apostrophe bugs.
 def js_replace(m):
  raw=m[1]
  d=re.sub(r'\\x([0-9a-fA-F]{2})',lambda x:chr(int(x[1],16)),raw)
  return json.dumps(mapping[d],ensure_ascii=False) if d in mapping else m[0]
 parts=re.split(r'(<script[^>]*>.*?</script>)',source,flags=re.S)
 for i,p in enumerate(parts):
  if p.startswith('<script'):
   parts[i]=re.sub(r"'((?:\\.|[^'\\])*)'",js_replace,p)
  else:
   # Longest source first prevents translating fragments inside longer passages.
   for a,b in sorted(mapping.items(),key=lambda x:len(x[0]),reverse=True):p=p.replace(a,b)
   parts[i]=p
 source=''.join(parts)
 source=re.sub(r'<img[^>]*src="[^"]*logo.png"[^>]*>', '<span style="font:italic 25px Georgia,serif">Cualigrafía</span>',source)
 source=source.replace('lang="es"',f'lang="{lang}"',1)
 source=source.replace('CG_MORE','Explore all exercises' if lang=='en' else 'Открыть все упражнения').replace('CG_CREDIT','Original simulator by' if lang=='en' else 'Автор оригинального симулятора:')
 source=source.replace('</head>',css+'</head>',1)
 home='All exercises' if lang=='en' else 'Все упражнения'
 nav=f'<nav class="locale-nav" aria-label="{"Navigation" if lang=="en" else "Навигация"}"><a href="./index.html">← {home}</a><div class="languages"><a href="../en/pendu.html" lang="en" {"aria-current=\"page\"" if lang=="en" else ""}>EN</a><a href="../ru/pendu.html" lang="ru" {"aria-current=\"page\"" if lang=="ru" else ""}>RU</a></div></nav>'
 source=source.replace('<body>','<body>'+nav,1)
 out=root/'dist'/lang/'pendu.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(source)
 for n,script in enumerate(re.findall(r'<script[^>]*>(.*?)</script>',source,re.S)):
  js=Path('/tmp')/f'pendu-{lang}-{n}.js';js.write_text(script);subprocess.run(['node','--check',str(js)],check=True)
 print(lang,len(source),'bytes; JS syntax OK')
