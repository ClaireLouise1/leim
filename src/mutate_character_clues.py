import subprocess,sys
src=open('character-clues.html',encoding='utf-8').read()
M=[("trait line wrong",'["kind", 1], ["shy", 3]','["kind", 2], ["shy", 3]'),
("method wrong",'"how": ["act", "effect", "say", "think"]','"how": ["act", "act", "say", "think"]'),
("method speech->thought",'"how": ["say", "look", "effect", "think"]','"how": ["think", "look", "effect", "think"]'),
("look->act",'"how": ["look", "act", "effect", "say"]','"how": ["act", "act", "effect", "say"]'),
("quote from other line",'"q": ["grabbed the biggest slice", "watched','"q": ["his little sister", "watched'),
("trait label swap",'"traits": [["honest", 3]]},','"traits": [["clever", 3]]},'),
("close off",'CLOSE={bossy:["rude"],rude:["bossy","selfish"],selfish:["jealous","rude"],jealous:["selfish"]};','CLOSE={};'),
("trait bar off",'var T=text(),t=rnd(T.traits),bar=T.traits.map(function(x){return x[0];});','var T=text(),t=rnd(T.traits),bar=[t[0]];'),
("line answer off by one",'return C("Which line shows it?","Line "+ln,','return C("Which line shows it?","Line "+(ln%4+1),'),
("how wrong highlight",'card(T,i+1),{t:"how"','card(T,(i+1)%4+1),{t:"how"'),
("trait highlight wrong",'card(T,t[1]),{t:"trait"','card(T,t[1]%4+1),{t:"trait"'),
("quote pool includes answer line",'return i!==ln-1;}).map(cq);','return i!==(ln%4);}).map(cq);'),
("effect->say",'"how": ["act", "effect", "think", "say"]','"how": ["act", "say", "think", "say"]'),
("think->act",'"how": ["think", "act", "effect", "look"]','"how": ["act", "act", "effect", "look"]'),
]
ok=0
for name,a,b in M:
    assert src.count(a)==1,(name,src.count(a))
    open('/tmp/m.html','w',encoding='utf-8').write(src.replace(a,b))
    subprocess.run('N=200 node src/test_character_clues.js /tmp/m.html > /tmp/m.jsonl',shell=True,check=True)
    r=subprocess.run(['python3','src/test_character_clues.py','/tmp/m.jsonl','/tmp/m.html'],capture_output=True,text=True)
    caught=r.returncode!=0; ok+=caught
    print('CAUGHT' if caught else 'MISSED',name,r.stdout.strip().splitlines()[-1])
print(ok,'/',len(M))
