import re,json,base64,pathlib
ROOT=pathlib.Path('/workspace/sites/cualigrafia-en-ru')
source=(ROOT/'source/hipo.es.html').read_text()
# Translations of whole string values; simulation identifiers remain untouched.
rows='''El hip thrust: glúteo, femoral o cuádriceps|Hip thrust: glutes, hamstrings or quadriceps|Ягодичный мост: ягодицы, задняя поверхность бедра или квадрицепс
El hip thrust.|The hip thrust.|Ягодичный мост.
Pero bien explicado|Clearly explained|Понятно о биомеханике
Cualigrafía. Pulsa para la sorpresa|Cualigrafía. Press for a surprise|Cualigrafía. Нажмите для сюрприза
Simulación|Simulation|Симуляция
Persona de perfil haciendo un hip thrust con barra, con la espalda alta en un banco. Se ve la línea por la que pasa el empuje, su distancia a la rodilla y a la cadera, los músculos que se encienden según trabajan y lo que hace el banco.|Side view of a barbell hip thrust with the upper back on a bench. Shows the line of force, its distance from the knee and hip, the muscles involved, and bench movement.|Вид сбоку: ягодичный мост со штангой, верх спины на скамье. Показаны линия силы, её расстояние до колена и таза, работа мышц и движение скамьи.
Subir o bajar la cadera. Usa las flechas del teclado.|Raise or lower the hips. Use the arrow keys.|Поднять или опустить таз. Используйте стрелки на клавиатуре.
Suelo de hielo|Icy floor|Ледяной пол
100% CULO|GLUTES ONLY|ТОЛЬКО ЯГОДИЦЫ
Fijar banco|Fix bench|Закрепить скамью
Soltar banco|Release bench|Освободить скамью
Acercar o alejar los pies del banco. Usa las flechas del teclado.|Move the feet towards or away from the bench. Use the arrow keys.|Приблизить стопы к скамье или отдалить их. Используйте стрелки на клавиатуре.
Inclinar el empuje contra el suelo, del cuádriceps al femoral. Usa las flechas del teclado.|Change the angle of force into the floor, from quadriceps to hamstrings. Use the arrow keys.|Изменить угол усилия в пол — от квадрицепсов к задней поверхности бедра. Используйте стрелки на клавиатуре.
Poner el vídeo: repeticiones en bucle|Play looping repetitions|Запустить повторения по кругу
Parar el vídeo|Stop repetitions|Остановить повторения
Mansplaining activado|Explanations on|Пояснения включены
Mansplaining desactivado|Explanations off|Пояснения выключены
Peso que puedes levantar con esta técnica, respecto a lo máximo del simulador|Weight you can lift with this technique, relative to the maximum in this model|Вес, который можно поднять с этой техникой, относительно максимума в модели
Mensajes|Explanations|Пояснения
Tarjeta anterior|Previous tip|Предыдущая подсказка
Tarjeta siguiente|Next tip|Следующая подсказка
Continuar|Continue|Продолжить
¿Qué haces tú?|What do you do?|Ваши действия?
Me subo encima a ver si puede también con mi peso|Climb on to see if she can lift me too|Залезть сверху и проверить, поднимет ли она и меня
Le pregunto cuántas le quedan|Ask how many sets she has left|Спросить, сколько подходов осталось
Le doy un consejo que no me ha pedido|Offer some unsolicited advice|Дать непрошеный совет
Volver a empezar|Start again|Начать заново
Salir|Exit|Выйти
Más|More|Подробнее
Más info|About the model|О модели
Más ejercicios|More exercises|Другие упражнения
¿Quién ha hecho esto?|Credits|Авторы
No pulses aquí|Don't press here|Не нажимайте сюда
Cerrar|Close|Закрыть
¿Te está gustando?|Enjoying this?|Нравится симулятор?
¿Te diviertes moviendo las flechitas?|Having fun moving the arrows?|Интересно двигать стрелки?
Basta de chorradas.|Back to the essentials.|Вернёмся к главному.
Empujas el banco hacia abajo con la espalda alta.|Your upper back pushes the bench down.|Верх спины давит на скамью вниз.
Empujas el banco hacia abajo y hacia atrás.|You push the bench down and backwards.|Вы давите на скамью вниз и назад.
Empujas el banco hacia abajo y lo arrastras hacia ti.|You push the bench down and pull it towards you.|Вы давите на скамью вниз и тянете её к себе.
El banco vuelca hacia atrás. Fíjalo o empuja más vertical.|The bench tips backwards. Secure it or push more vertically.|Скамья опрокидывается назад. Закрепите её или направьте усилие ближе к вертикали.
El banco se levanta por detrás. Fíjalo o arrastra menos los talones.|The back of the bench lifts. Secure it or pull less with your heels.|Задний край скамьи поднимается. Закрепите её или меньше тяните пятки к себе.
Así no puedes hacer mucha fuerza.|This position limits how much force you can produce.|В этом положении трудно развить большое усилие.
Así puedes hacer mucha fuerza.|This position lets you produce a lot of force.|В этом положении можно развить большое усилие.
Así puedes hacer bastante fuerza.|This position lets you produce a fair amount of force.|В этом положении можно развить достаточно большое усилие.
Así estás intentando juntar los pies al banco.|You are trying to pull your feet towards the bench.|Вы стараетесь подтянуть стопы к скамье.
Así empujas en la dirección de la tibia, como si quisieras clavarla en el suelo.|You push along your shins, as though driving them into the floor.|Вы направляете усилие вдоль голеней, словно хотите воткнуть их в пол.
Estás empujando hacia delante: no podrías si el suelo resbalara.|You are pushing forwards; this would not work on a slippery floor.|Вы давите вперёд: на скользком полу так не получится.
Si empujas así, te resbalas.|Push this way and your feet will slip.|С таким направлением усилия стопы скользят.
Así empujas en vertical: no te resbalarías en una pista de hielo.|You are pushing vertically: your feet would not slip even on ice.|Вы давите вертикально: стопы не скользили бы даже на льду.
Es una buena instrucción, en caso de que quieras empujar verticalmente.|This is a useful cue when you want to push vertically.|Это полезная подсказка, если вы хотите направить усилие вертикально.
Empujando siempre en la dirección de las tibias.|Always pushing along the shins.|Усилие всегда направлено вдоль голеней.
Suelo de hielo activado|Icy floor enabled|Ледяной пол включён
100% culo activado|Glute focus enabled|Акцент на ягодицы включён
La colocación en este ejercicio es muy importante.|Your setup matters a great deal in this exercise.|В этом упражнении очень важно исходное положение.
Dependiendo de cómo empujes, también usarás otros músculos además del culo.|The direction of your push determines which muscles assist the glutes.|От направления усилия зависит, какие мышцы помогают ягодичным.
Si te imaginas que estás en una pista de hielo, conseguirás empujar verticalmente.|Imagine standing on ice to help you push vertically.|Представьте, что стоите на льду: это поможет давить вертикально.
Si quisieras aislar el glúteo lo máximo posible, tendrías que intentar clavar las tibias en el suelo como si fueran sombrillas en la playa.|To focus on the glutes, imagine driving your shins into the ground like beach umbrella poles.|Чтобы сильнее сосредоточить нагрузку на ягодицах, представьте, что втыкаете голени в землю, как стойки пляжного зонта.
Para intentar aislar el glúteo, haz como si tus tibias fueran palos de sombrilla y quisieras clavarlos en la playa. La fuerza tendrá que ir en la dirección de tu tibia.|To focus on the glutes, imagine driving your shins into the ground like beach umbrella poles. Direct the force along your shins.|Чтобы сильнее сосредоточить нагрузку на ягодицах, представьте, что втыкаете голени в землю, как стойки пляжного зонта. Направляйте усилие вдоль голеней.
Si juntas mucho los pies al banco no podrás hacer mucha fuerza. Si los alejas demasiado, tampoco. Mira cómo cambia la barra de fuerza.|Feet too close to the bench limit your force, and so do feet too far away. Watch the force bar change.|Если стопы слишком близко к скамье, развить большое усилие трудно. Если слишком далеко — тоже. Следите за изменением шкалы усилия.
Si haces fuerza hacia delante (como si quisieras empujar el banco), el cuádriceps empujará también. Pero cuidado: si el banco no está fijo, lo puedes llegar a volcar. No queremos eso.|Pushing forwards, as if to push the bench away, brings in the quadriceps too. An unsecured bench can tip over.|Если давить вперёд, словно отталкивая скамью, подключаются квадрицепсы. Незакреплённая скамья при этом может опрокинуться.
Si el suelo fuera de hielo, solo podrías empujar en vertical. Si te cuesta no empujar demasiado con el cuádriceps, prueba a visualizar esto.|On ice, you could only push vertically. Try imagining this if you find it hard to reduce your quadriceps contribution.|На льду можно было бы давить только вертикально. Представьте это, если вам трудно уменьшить участие квадрицепсов.
Está muy bien entender todo esto, pero lo importante es otra cosa: usar una técnica que te permita hacer un rango completo y empujar con seguridad, coger cada vez más peso y hacerte cada vez más fuerte.|Understanding this helps, but the priority is a technique that allows a full range of motion and a secure push, then gradually increasing the weight and getting stronger.|Понимать это полезно, но главное — техника, которая позволяет двигаться в полной амплитуде и безопасно развивать усилие, постепенно увеличивая вес и становясь сильнее.
Sóleo|Soleus|Камбаловидная
Vastos|Vasti|Широкие мышцы бедра
Glúteo mayor|Gluteus maximus|Большая ягодичная
Isquiotibiales|Hamstrings|Задняя поверхность бедра
recto femoral|rectus femoris|прямая мышца бедра
Me voy a avisar a otro gymbro|Go and get another gym buddy|Позвать ещё одного приятеля
Tiene los cascos puestos y está escuchando a Britney Spears a 250 dB. Te mira. No contesta. Procede a hacer su siguiente serie.|She has headphones on and is listening to Britney Spears at 250 dB. She looks at you, says nothing, and starts her next set.|Она в наушниках и слушает Бритни Спирс на 250 дБ. Смотрит на вас, молчит и начинает следующий подход.
¡Oh, no! La culona del gimnasio está haciendo su vigesimotercera serie de hip thrust (es su noveno ejercicio de glúteo de la sesión y le quedan 5 más). Tiene la barra cargada con todos los discos del gimnasio.|Oh no! The gym's hip thrust champion is on set twenty-three. This is her ninth glute exercise today, with five more to go. Every plate in the gym is on her bar.|О нет! Чемпионка зала по ягодичному мосту делает двадцать третий подход. Это её девятое упражнение на ягодицы сегодня, и впереди ещё пять. На штанге все блины из зала.
'''
maps={'en':{},'ru':{}}
for row in rows.strip().splitlines():
    es,en,ru=row.split('|');maps['en'][es]=en;maps['ru'][es]=ru
# Phrase fragments retain surrounding spaces because the original composes sentences.
fragments=[
('empujar menos hacia delante','push less forwards','меньше давить вперёд'),
('acercar ','move ','приблизить '),('alejar ','move ','отдалить '),
('empujando ','by pushing ','направляя усилие '),('Si arrastras ','If you pull ','Если тянуть '),
(' podrás con más peso.',' you can lift more weight.',' можно поднять больший вес.'),
(', podrás con más peso.',', you can lift more weight.',', можно поднять больший вес.'),
('más hacia delante','further forwards','дальше вперёд'),('hacia delante','forwards','вперёд'),
('los pies del banco','your feet away from the bench','стопы от скамьи'),
('los pies al banco','your feet towards the bench','стопы к скамье'),
('arrastrar ','pull ','тянуть '),('Con los pies ','With your feet ','Если стопы '),
('Si empujas con los pies más hacia delante','If you push further forwards with your feet','Если сильнее давить стопами вперёд'),
(' Para poder levantar más peso, prueba a ',' To lift more weight, try to ',' Чтобы поднять больший вес, попробуйте '),
('más los talones hacia ti','your heels more towards you','пятки сильнее к себе'),
('Si empujas ','If you push ','Если давить '),
('empujando más hacia delante','by pushing further forwards','усиливая давление вперёд'),
('Si empujas menos hacia delante','If you push less forwards','Если меньше давить вперёд'),
(' Vas al límite de lo que agarra la suela.',' You are at the limit of your soles’ grip.',' Сцепление подошвы с полом на пределе.'),
('un poco ','a little ','немного '),('arrastrando ','by pulling ','подтягивая '),
('más cerca del banco','closer to the bench','ближе к скамье'),
('más lejos del banco','further from the bench','дальше от скамьи'),
('empujar ','push ','давить '),('los talones hacia ti','your heels towards you','пятки к себе'),
('Así no puedes ni con ','This way, you cannot even lift ','Так не получится поднять даже '),
(' Si quieres hacer cuádriceps, vete a la máquina de extensiones.',' For a quadriceps-focused exercise, use the leg extension machine.',' Для акцента на квадрицепсах подойдёт тренажёр для разгибания ног.'),
(' Si quieres hacer femoral, vete a la máquina de curl.',' For a hamstring-focused exercise, use the leg curl machine.',' Для акцента на задней поверхности бедра подойдёт тренажёр для сгибания ног.'),
(' Si es un banco pesado o lo apoyas en la pared, aguantará. Si no… game over.',' A heavy bench or one supported by a wall can stay in place. Otherwise… game over.',' Тяжёлая скамья или скамья у стены может устоять. Иначе… игра окончена.'),
(' gymbros se balanceaban sobre la barra de una tocha.',' gym buddies were balancing on her barbell.',' приятелей балансировали на её штанге.'),
('Como veías que no se caía, fuisteis a llamar a otro gymbro: ','Seeing that she was still going, you called another gym buddy: ','Увидев, что она справляется, вы позвали ещё одного приятеля: '),
(' GYMBRO',' BUDDY',' ПРИЯТЕЛЬ'),(' KG · ',' KG · ',' КГ · '),(' kg.',' kg.',' кг.'),
]
for es,en,ru in fragments: maps['en'][es]=en;maps['ru'][es]=ru
long='Se quita los cascos para escucharte y, sonriendo, te da las gracias por tu sabiduría. Acaba dándote su Instagram y suplicándote tener una cita contigo.\nTe despiertas. Te había dado un bajón de azúcar haciendo press banca con 50 kg. Mientras el monitor te acompaña al vestuario, ves por el rabillo del ojo cómo la culona empieza otra serie con 400 kg.'
maps['en'][long]='She takes off her headphones and thanks you for your wisdom, smiling. She gives you her Instagram and begs you for a date.\nYou wake up. You had a blood sugar crash while bench pressing 50 kg. As the trainer helps you to the changing room, you see her starting another set with 400 kg.'
maps['ru'][long]='Она снимает наушники и с улыбкой благодарит вас за мудрый совет. Даёт свой Instagram и просит пригласить её на свидание.\nВы просыпаетесь. У вас упал сахар во время жима лёжа с 50 кг. Пока тренер провожает вас в раздевалку, вы видите, как она начинает ещё один подход с 400 кг.'
info={
'en':'<p><b>Model.</b> A 175 cm, 80 kg person viewed from the side, with the upper back on the edge of a 43 cm flat bench and a 100 kg barbell at the hips. This is a static model: each position is calculated as though held still.</p><p><b>Muscles.</b> Glute brightness follows the torque required at the hip; quadriceps brightness follows the torque at the knee. Hamstrings extend the hip and bend the knee, so they contribute when the force line passes in front of the knee. Their brightness reflects a minimum-effort distribution of force between muscles. These are not EMG readings: this is a simplified mechanical model.</p><p><b>The white bar.</b> The weight you could lift with the selected foot position and force direction, relative to the maximum possible in this model. It uses approximate maximum muscle forces. At each point in the movement, the first muscle to reach its limit sets the load, and the weakest position determines the result.</p><p><b>Scope.</b> Explore how forces act and how to change them. This model does not measure an individual person.</p>',
'ru':'<p><b>Модель.</b> Человек ростом 175 см и массой 80 кг, вид сбоку. Верх спины опирается на край горизонтальной скамьи высотой 43 см, на тазу — штанга 100 кг. Модель статическая: каждое положение рассчитывается как неподвижное.</p><p><b>Мышцы.</b> Яркость ягодичных мышц соответствует моменту силы в тазобедренном суставе, квадрицепсов — в коленном. Мышцы задней поверхности бедра разгибают тазобедренный и сгибают коленный сустав, поэтому подключаются, когда линия силы проходит перед коленом. Их яркость отражает распределение нагрузки по принципу минимального усилия. Это не показания ЭМГ, а упрощённая механическая модель.</p><p><b>Белая шкала.</b> Вес, который можно поднять с выбранным положением стоп и направлением усилия, относительно максимума модели. Расчёт использует ориентировочные предельные силы мышц. В каждой точке движения нагрузку ограничивает мышца, первой достигающая своего предела, а итог определяет самое слабое положение.</p><p><b>Назначение.</b> Помочь понять действие сил и способы их изменить. Модель не измеряет показатели конкретного человека.</p>'}
# Base64 alphabet used by the original minifier.
custom='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'
standard='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
dec_trans=str.maketrans(custom,standard);enc_trans=str.maketrans(standard,custom)
def dec(x): return base64.b64decode(x.translate(dec_trans)+'===').decode()
def enc(x): return base64.b64encode(x.encode()).decode().rstrip('=').translate(enc_trans)
for locale in ['en','ru']:
    tr=maps[locale];s=source
    # Remove the original subscription script and iframe entirely.
    s=re.sub(r'<script>\(function\(\)\{\s*var ACTION =.*?</script>','',s,flags=re.S)
    s=re.sub(r'<iframe name="mlFrame".*?</iframe>','',s,flags=re.S)
    # Keep original hook elements, but replace subscription and author content.
    s=re.sub(r'<div class="subform">.*?<p class="subMsg"[^>]*>.*?</p></div>', '<p><a class="btnY" href="./index.html">'+('Explore all exercises' if locale=='en' else 'Все упражнения')+'</a></p>',s,flags=re.S)
    s=re.sub(r'(<div class="dd" id="dd-who" hidden>).*?(</div>)',r'\1<p>'+('Original simulator by Pablo · ' if locale=='en' else 'Оригинальный симулятор: Пабло · ')+'<a href="https://cualigrafia.com/" target="_blank" rel="noopener">Cualigrafía</a></p>'+r'\2',s,flags=re.S)
    s=re.sub(r'(<div class="dd" id="dd-info" hidden>).*?(</div>)',lambda m:m[1]+info[locale]+m[2],s,flags=re.S)
    s=s.replace('¿Un proyecto en mente?', 'Original website' if locale=='en' else 'Оригинальный сайт')
    s=s.replace('href="#dd-who" id="sheetWork"','href="https://cualigrafia.com/" id="sheetWork"')
    # Localize encoded strings without disturbing the dictionary order or numeric guard.
    arr=re.search(r"const _0xb95e51=\[(.*?)\];_0x2680",s)
    entries=re.findall(r"'([^']*)'",arr[1])
    replacement=','.join("'"+enc(tr.get(dec(x),dec(x)))+"'" for x in entries)
    s=s[:arr.start(1)]+replacement+s[arr.end(1):]
    # All remaining ordinary JavaScript string literals, including escaped spaces.
    scripts=[]
    def localize_script(m):
        code=m[1]
        def localize_literal(q):
            raw=q[0];v=raw[1:-1]
            v=re.sub(r'\\x([0-9a-fA-F]{2})',lambda n:chr(int(n[1],16)),v)
            if v in tr:return json.dumps(tr[v],ensure_ascii=False)
            return raw
        code=re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"",localize_literal,code)
        scripts.append(code);return f'<!--SCRIPT{len(scripts)-1}-->'
    s=re.sub(r'<script>(.*?)</script>',localize_script,s,flags=re.S)
    # Match whole text nodes or attributes; never globally substitute substrings.
    def replace_html(m):
        text=m[0]
        if text.startswith('>'):
            value=text[1:-1];return '>'+tr.get(value,value)+'<'
        value=text[1:-1];return '"'+tr.get(value,value).replace('"','&quot;')+'"'
    s=re.sub(r'>[^<>]*<|"[^"<>]*"',replace_html,s)
    s=s.replace('<html lang="es">',f'<html lang="{locale}">')
    s=re.sub(r'<img src="https://cualigrafia.com/[^>]+>','<span style="font:italic 25px Georgia,serif">Cualigrafía</span>',s)
    s=s.replace('400 KG · 0 GYMBROS','400 KG · 0 BUDDIES' if locale=='en' else '400 КГ · 0 ПРИЯТЕЛЕЙ')
    nav='<nav class="locale-nav" aria-label="'+('Navigation and language' if locale=='en' else 'Навигация и язык')+'"><a href="./index.html">← '+('All exercises' if locale=='en' else 'Все упражнения')+'</a><span><a lang="en" href="../en/hipo.html"'+(' aria-current="page"' if locale=='en' else '')+'>EN</a><a lang="ru" href="../ru/hipo.html"'+(' aria-current="page"' if locale=='ru' else '')+'>RU</a></span></nav>'
    css='<style>.locale-nav{max-width:960px;margin:0 auto;padding:20px 28px 0;display:flex;justify-content:space-between;gap:16px;font-size:13px}.locale-nav a{color:#a0a0a8;text-decoration:none}.locale-nav span{display:flex;gap:16px}.locale-nav [aria-current]{color:#f6c915}.sheet{display:none!important}.top{gap:12px;flex-wrap:wrap}.pageTitle{font-size:clamp(25px,6vw,44px)}.banner{white-space:normal;letter-spacing:.08em}.modebtn{white-space:normal;max-width:170px}.hipbtn{max-width:170px}.xsw .xl{max-width:110px}@media(max-width:480px){.modos{gap:4px;top:16px}.modebtn{font-size:10px;padding:7px 8px;max-width:120px}.logo{height:36px}.locale-nav{padding:16px 14px 0}.top{min-height:80px}.banner{top:70px}.gbox,.gopt{font-family:monospace;font-size:13px}}</style>'
    s=s.replace('</head>',css+'</head>').replace('<body>','<body>'+nav)
    for i,code in enumerate(scripts):s=s.replace(f'<!--SCRIPT{i}-->',f'<script>{code}</script>')
    out=ROOT/'dist'/locale/'hipo.html';out.parent.mkdir(exist_ok=True);out.write_text(s)
    for i,code in enumerate(re.findall(r'<script>(.*?)</script>',s,re.S)):
        path=pathlib.Path(f'/tmp/hipo-{locale}-{i}.js');path.write_text(code)
    print(locale,len(s),'characters', 'scripts:',len(scripts))
