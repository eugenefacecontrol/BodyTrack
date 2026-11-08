from pathlib import Path
import re,base64,json,subprocess
src=(Path(__file__).parent / 'source/prensa.es.html').read_text()
# Keep the educational model, remove live subscription integrations.
src=re.sub(r'<iframe name="mlFrame".*?</iframe>\s*<script>.*?</script>', '',src,flags=re.S)
src=re.sub(r'<div class="subform">.*?</div>', '<p><a href="./index.html">More exercises</a></p>',src,flags=re.S)
src=re.sub(r'(<div class="dd" id="dd-who" hidden>).*?(</div>)',r'\1<p>Original interactive model by <a href="https://cualigrafia.com/" target="_blank" rel="noopener">Pablo · Cualigrafía</a>.</p>\2',src,flags=re.S)
src=src.replace('<link rel="preconnect" href="https://tally.so">','')
src=re.sub(r'\(\(\(\)=>\{const _0x5667d2=.*?let _0x2b9483', 'let _0x2b9483',src,flags=re.S)
src=re.sub(r'<img src="https://cualigrafia.com/[^"]+" alt="Cualigrafía" decoding="async">', '<span style="font:italic 21px Georgia,serif">Cualigrafía</span>',src)
src=src.replace("function _0x398d6f(_0x1eaf3f){", "function _0x398d6f(_0x1eaf3f){return;")
# No Tally embeds remain; prevent loading its external script.
src=src.replace("function _0x440b45(){", "function _0x440b45(){return;")
src=src.replace('https://cualigrafia.com/wp-content/uploads/2024/12/134cce47-7636-40ee-99b1-ab26c0ec2040.png','/assets/logo.png')
D={}
def add(es,en,ru): D[es]=(en,ru)
add('Prensa de piernas: glúteo o cuádriceps','Leg press: glutes or quadriceps','Жим ногами: ягодицы или квадрицепсы')
add('La prensa.','The leg press.','Жим ногами.')
add('Pero bien explicada','Made clear','Понятно о биомеханике')
add('Cualigrafía. Pulsa para la sorpresa','Cualigrafía. Tap for a surprise','Cualigrafía. Нажмите для сюрприза')
add('Simulación','Simulation','Симуляция')
add('Persona de perfil en una prensa de piernas. Se ve la línea por la que pasa el empuje, su distancia a la rodilla y a la cadera, los músculos que se encienden según trabajan y dónde te sujeta el respaldo.','Side view of a person on a leg press. The diagram shows the line of force, its distance from the knee and hip, working muscles, and backrest support.','Вид сбоку: человек в тренажёре для жима ногами. Показаны линия силы, её расстояние до колена и таза, работающие мышцы и опора на спинку.')
add('Mover la plataforma a lo largo del recorrido. Usa las flechas del teclado.','Move the platform through its range. Use the arrow keys.','Переместить платформу по траектории. Используйте стрелки на клавиатуре.')
add('Subir o bajar los pies en la plataforma. Usa las flechas del teclado.','Move the feet higher or lower on the platform. Use the arrow keys.','Поднять или опустить стопы на платформе. Используйте стрелки на клавиатуре.')
add('Inclinar el empuje, del cuádriceps al glúteo. Usa las flechas del teclado.','Change the force direction, from quadriceps to glutes. Use the arrow keys.','Изменить направление усилия: от квадрицепсов к ягодицам. Используйте стрелки на клавиатуре.')
add('Poner el vídeo: repeticiones en bucle','Play repeating movement','Запустить повторение движения')
add('Parar el vídeo','Stop animation','Остановить анимацию')
add('Mansplaining activado','Explanation on','Объяснение включено')
add('Mansplaining desactivado','Explanation off','Объяснение выключено')
add('Patorras','Quadriceps','Квадрицепсы')
add('Culazo','Glutes','Ягодицы')
add('Reparto del esfuerzo: de patorras (cuádriceps) a culazo (glúteo)','Effort distribution: from quadriceps to glutes','Распределение усилия: от квадрицепсов к ягодичным мышцам')
add('Mensajes','Explanation','Объяснение')
add('Tarjeta anterior','Previous explanation','Предыдущее объяснение')
add('Tarjeta siguiente','Next explanation','Следующее объяснение')
add('Continuar','Continue','Продолжить')
add('¿Qué haces tú?','What do you do?','Что вы сделаете?')
add('Le cargo otro par de discos de 20','Add another pair of 20 kg plates','Добавить ещё два диска по 20 кг')
add('Le pregunto cuántas le quedan','Ask how many sets are left','Спросить, сколько подходов осталось')
add('Le empujo la prensa y le obligo a bajar hasta abajo','Push the sled into a deeper range','Опустить платформу глубже')
add('Volver a empezar','Start again','Начать заново')
add('Salir','Exit','Выйти')
add('Más','More','Подробнее')
add('Más info','About this model','Об этой модели')
add('Más ejercicios','More exercises','Другие упражнения')
add('More exercises','More exercises','Другие упражнения')
add('¿Quién ha hecho esto?','About the creator','Об авторе')
add('No pulses aquí','Do not press this','Не нажимайте сюда')
add('Cerrar','Close','Закрыть')
add('¿Te diviertes moviendo las flechitas?','Enjoying the interactive arrows?','Нравится управлять стрелками?')
add('¿Un proyecto en mente?','About the creator','Об авторе')
add('¿Te está gustando?','Enjoying this?','Вам нравится?')
add('<b>Modelo.</b> Es un modelo de perfil, con huesos rígidos y movimiento lento. Lo que trabaja cada músculo se toma como el giro que el empuje provoca en su articulación: fuerza × brazo de palanca.','<b>Model.</b> This side-view model assumes rigid bones and slow movement. Muscle demand is represented by the torque created at the joint: force × moment arm.','<b>Модель.</b> Вид сбоку, жёсткие звенья и медленное движение. Нагрузка на мышцы оценивается по моменту силы в суставе: сила × плечо силы.')
add('<b>Músculos.</b> «Glúteo» agrupa a todo lo que extiende la cadera; los isquios también ayudan ahí. El gemelo y el resto de músculos se dejan fuera para simplificar.','<b>Muscles.</b> “Glutes” represents all hip extensors, including assistance from the hamstrings. The calf and other muscles are omitted for simplicity.','<b>Мышцы.</b> «Ягодицы» здесь обозначает все разгибатели тазобедренного сустава; мышцы задней поверхности бедра тоже помогают. Икроножные и другие мышцы для простоты не учитываются.')
add('<b>Flechas azules.</b> Son la fuerza que haces sobre el asiento: una empujando el respaldo y otra tirando de las asas, que se iluminan cuanto más tiras. Cuentan el peso del cuerpo y una carga de referencia (un empuje de 2 veces tu peso).','<b>Blue arrows.</b> These show the forces you apply to the seat: pushing against the backrest and pulling on the handles, which brighten as you pull harder. The model includes body weight and a reference pushing force of twice your body weight.','<b>Синие стрелки.</b> Это силы, которые вы прикладываете к сиденью: давление на спинку и тяга за рукояти. Чем сильнее тяга, тем ярче рукояти. Учитываются вес тела и условное усилие, равное удвоенному весу тела.')
add('<b>Alcance.</b> Sirve para entender tendencias, no para medir a una persona concreta.','<b>Scope.</b> This illustrates general trends, not measurements for an individual.','<b>Применение.</b> Модель помогает понять общие закономерности, а не рассчитать нагрузку для конкретного человека.')
add('Original interactive model by','Original interactive model by','Автор исходной интерактивной модели:')
add('Empuja como si la plataforma fuera de hielo y no quisieras resbalarte.','Push as if the platform were ice and you wanted to avoid slipping.','Толкайте так, будто платформа покрыта льдом и вы не хотите поскользнуться.')
add('Está muy bien entender todo esto, pero lo importante es otra cosa: usar una técnica que te permita apretar con seguridad, coger cada vez más peso y hacerte cada vez más fuerte.','Understanding this helps, but the main goal is a technique that lets you exert force safely, increase the load gradually, and get stronger.','Разбираться в этом полезно, но главное — техника, которая позволяет безопасно прикладывать усилие, постепенно повышать нагрузку и становиться сильнее.')
add('Para conseguirlo, fíjate también en cómo empujas el respaldo.','To do this, pay attention to how you push against the backrest.','Для этого обратите внимание и на то, как вы давите на спинку.')
add('Máxima palanca para tus cuádriceps. Podrás mover menos peso.','Maximum moment arm at the knee. Your quadriceps face greater demand, so you can move less weight.','Максимальное плечо силы у колена. Нагрузка на квадрицепсы выше, поэтому рабочий вес будет меньше.')
add('También importa la intención con la que empujas la plataforma.','The direction in which you try to push the platform also matters.','Важно и то, в каком направлении вы стараетесь толкать платформу.')
add('Si empujas el respaldo solo con la parte baja, apretarás más los cuádriceps.','Pushing against the backrest with only your lower back increases quadriceps demand.','Если давить на спинку только нижней частью спины, нагрузка на квадрицепсы возрастёт.')
add('Empuja hacia abajo. Si algún cabrón hubiera echado aceite en la plataforma, tus pies se deslizarían hacia abajo.','Push downward along the platform. If it were slippery, your feet would slide down.','Толкайте вниз вдоль платформы. Если бы поверхность была скользкой, стопы сдвигались бы вниз.')
add('Notarás cómo empujas el respaldo con toda la espalda. Tendrás que agarrarte con las manos.','You will feel your whole back pressing into the backrest. You need to hold the handles.','Вы почувствуете, как давите на спинку всей спиной. Потребуется держаться за рукояти.')
add('¡Oh, no! El máquina de tu gimnasio ha cargado la prensa con todos los discos de 20 que había. Acaba de comenzar su ritual de apareamiento (para atraer a otros gymbros).','Oh no! The gym show-off has loaded every 20 kg plate onto the leg press. The ritual to impress the other gymbros has begun.','О нет! Главный герой зала загрузил в жим все диски по 20 кг. Начался ритуал привлечения внимания других качков.')
add('Mira cómo cambia el ejercicio: con los pies altos el culo puede tener más palanca; con los pies bajos, las piernas.','Notice the change: feet higher on the platform can increase the hip moment arm; feet lower can increase the knee moment arm.','Посмотрите, как меняется упражнение: стопы выше могут увеличить плечо силы у таза, а стопы ниже — у колена.')
add('Notarás cómo empujas el respaldo con la parte más alta de la espalda. Tendrás que agarrarte fuerte con las manos.','You will feel your upper back pressing into the backrest. Grip the handles firmly.','Вы почувствуете давление на спинку верхней частью спины. Крепко держитесь за рукояти.')
add('Ahora el recorrido es microscópico. En su cabeza sigue siendo espectacular.','Now the range of motion is microscopic. In his mind, it is still spectacular.','Теперь амплитуда микроскопическая. Но в его голове это всё ещё впечатляюще.')
add('Empuja hacia arriba. Si la superficie fuera resbalosa, tus pies deslizarían hacia arriba.','Push upward along the platform. If the surface were slippery, your feet would slide up.','Толкайте вверх вдоль платформы. На скользкой поверхности стопы сдвигались бы вверх.')
add('Si intentas clavar las tibias como si fueran palos de sombrilla, activarás más el culo.','Push along the line of your shins, as if planting poles in the platform, to increase hip extensor demand.','Толкайте вдоль голеней, будто втыкаете стойки в платформу: это увеличивает нагрузку на разгибатели тазобедренного сустава.')
add('Movimiento natural. Empuja todo lo que puedas y te moverás en esta zona.','Natural movement. Push hard and your movement tends to stay in this region.','Естественное движение. При сильном толчке движение обычно остаётся в этой области.')
add('Máxima palanca en el glúteo. Empuja siempre en la dirección de tus tibias, como si fueran sombrillas de playa y quisieras clavarlas en la plataforma. Podrás mover menos peso.','Maximum hip moment arm. Push along your shins, as if they were poles you were planting into the platform. You can move less weight.','Максимальное плечо силы у таза. Толкайте вдоль голеней, будто втыкаете стойки в платформу. Рабочий вес будет меньше.')
add(' La suela no agarra más: para más cuádriceps, baja los pies.',' Grip is at its limit: lower your feet for more quadriceps demand.',' Сцепление подошвы на пределе: для большей нагрузки на квадрицепсы опустите стопы.')
add(' La suela no agarra más: para más glúteo, sube los pies.',' Grip is at its limit: raise your feet for more glute demand.',' Сцепление подошвы на пределе: для большей нагрузки на ягодицы поднимите стопы.')
add('Notarás cómo empujas el respaldo con la parte más baja de la espalda, casi con el culo.','You will feel pressure against the backrest very low on your back, almost at your hips.','Вы почувствуете давление на спинку самой нижней частью спины, почти тазом.')
add('En la prensa puedes poner los pies más arriba o más abajo.','On the leg press, you can place your feet higher or lower.','В жиме ногами стопы можно поставить выше или ниже.')
add('Si intentas deslizar los pies hacia arriba, activarás más las piernas.','Trying to slide your feet upward increases quadriceps demand.','Попытка сдвинуть стопы вверх увеличивает нагрузку на квадрицепсы.')
add('Si empujas con la parte alta de la espalda y te agarras fuerte, conseguirás empujar más con el culo.','Pressing with your upper back and holding the handles firmly lets your hip extensors contribute more.','Давление верхней частью спины и крепкий хват помогают сильнее включить разгибатели тазобедренного сустава.')
add('Basta de chorradas.','Keep it practical.','Перейдём к практике.')
add('Ahora baja menos todavía.','Now he lowers it even less.','Теперь он опускает платформу ещё меньше.')
add('«Estoy calentando, BRO.»','“Just warming up, BRO.”','«Это разминка, БРО».')
add('GAME OVER\nImposible que salga de la prensa. Ahora te toca a ti recoger los discos.','GAME OVER\nHe is stuck in the leg press. Now you have to put all the plates away.','ИГРА ОКОНЧЕНА\nОн застрял в тренажёре. Теперь вам убирать все диски.')
add(' KG',' kg',' кг')
add('500 KG','500 kg','500 кг')
alpha='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'
standard='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
dec=str.maketrans(alpha,standard);enc=str.maketrans(standard,alpha)

def make(lang,idx):
 s=src
 # Translate encoded string-table entries without changing indices or control keys.
 def table(m):
  def token(n):
   raw=n[1]
   try:v=base64.b64decode(raw.translate(dec)+'===').decode()
   except:return n[0]
   if v in D:return "'"+base64.b64encode(D[v][idx].encode()).decode().rstrip('=').translate(enc)+"'"
   return n[0]
  return m[1]+re.sub(r"'([^']*)'",token,m[2])+m[3]
 s=re.sub(r'(function _0x4879\(\)\{const _0x3bca02=\[)(.*?)(\];)',table,s,flags=re.S)
 # Translate ordinary string literals, including hex-escaped whitespace.
 def script(m):
  def literal(n):
   val=re.sub(r'\\x([0-9a-fA-F]{2})',lambda z:chr(int(z[1],16)),n[1])
   if val in D:return json.dumps(D[val][idx],ensure_ascii=False)
   return n[0]
  return '<script>'+re.sub(r"'((?:\\.|[^'\\])*)'",literal,m[1])+'</script>'
 s=re.sub(r'<script>(.*?)</script>',script,s,flags=re.S)
 # HTML text and attribute strings.
 parts=re.split(r'(<script>.*?</script>)',s,flags=re.S)
 for i in range(0,len(parts),2):
  for k in sorted(D,key=len,reverse=True):parts[i]=parts[i].replace(k,D[k][idx])
 s=''.join(parts).replace('lang="es"',f'lang="{lang}"')
 s=s.replace('</head>','''<style>
 .localeNav{max-width:1200px;margin:16px auto 0;padding:0 18px;display:flex;align-items:center;gap:10px;font:500 13px/1.4 var(--font);flex-wrap:wrap}
 .localeNav a{color:#bfc0c9;text-decoration:none;padding:8px 12px;border-radius:18px;border:1px solid #33353c}.localeNav a:first-child{margin-right:auto}.localeNav a[aria-current]{color:#f6c915;border-color:#f6c915}
 .xsw .xl{max-width:100px;overflow-wrap:anywhere}.splitlab{gap:20px;line-height:1.25}.pageTitle{overflow-wrap:anywhere}.sheet{display:none!important}.gq,.gtext,.gopt{font-family:var(--font)}
 @media(max-width:460px){.top{gap:10px}.logo{height:44px}.pageTitle{font-size:28px}.localeNav{padding:0 10px}.split{width:90%}.splitlab{font-size:12px}.dock2{max-width:60%}}
 </style></head>''')
 home='All exercises' if lang=='en' else 'Все упражнения'
 nav=f'<nav class="localeNav" aria-label="Navigation"><a href="./index.html">← {home}</a><a href="../en/prensa.html" lang="en" '+('aria-current="page"' if lang=='en' else '')+'>EN</a><a href="../ru/prensa.html" lang="ru" '+('aria-current="page"' if lang=='ru' else '')+'>RU</a></nav>'
 s=s.replace('<body>','<body>'+nav)
 # Keep working settings while changing languages.
 state='''<script>(()=>{const key='cg-legpress-state';try{const saved=JSON.parse(sessionStorage.getItem(key)||'null');if(saved&&window.__s){for(const k of ['e','tr','frac'])if(Number.isFinite(saved[k]))window.__s.st[k]=saved[k];window.__s.step();window.__s.redraw();}document.querySelectorAll('.localeNav a[lang]').forEach(a=>a.addEventListener('click',()=>{if(window.__s){const s=window.__s.st;sessionStorage.setItem(key,JSON.stringify({e:s.e,tr:s.tr,frac:s.frac}));}}));localStorage.setItem('cg-locale',document.documentElement.lang);}catch{}})();</script>'''
 s=s.replace('</body>',state+'</body>')
 out=Path('/workspace/sites/cualigrafia-en-ru/dist')/lang/'prensa.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(s)
 for n,code in enumerate(re.findall(r'<script>(.*?)</script>',s,re.S)):
  f=Path(f'/tmp/prensa-{lang}-{n}.js');f.write_text(code);subprocess.run(['node','--check',str(f)],check=True)
 print(lang, len(s), 'syntax OK')
make('en',0);make('ru',1)
