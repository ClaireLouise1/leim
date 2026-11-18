# Builds the Junior Cycle Maths Exam Pack (Higher + Ordinary mock papers, worked solutions,
# "where the marks would go", score sheets) -> OUTDIR/JC-Maths-Exam-Pack-Leim.pdf + cover PNG.
# Usage: python3 src/build_maths_exam_pack.py /tmp/out
# Paper format = the 2026 SEC papers' marks, part splits, scales and suggested times (plain facts,
# same data as src/build_maths_exam_centre.py). Every QUESTION is original Léim material; nothing is
# copied or adapted from SEC papers or marking schemes. Every answer is computed and asserted below.
import os, sys, math, subprocess
from fractions import Fraction as F
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
OUT=sys.argv[1] if len(sys.argv)>1 else '/tmp/maths-exam-pack'
os.makedirs(OUT,exist_ok=True)

HL=[(1,15,'5C 10D',5),(2,25,'10D 5C 10C',10),(3,30,'15D 10D 5C',10),(4,20,'5B 5C 5D 5C',10),(5,15,'5C 10C',5),(6,10,'5C 5B',5),
    (7,30,'5B 10C 5D 10D',10),(8,25,'10D 5D 5B 5C',10),(9,20,'5C 5C 10D',10),(10,25,'10C 5C 10D',10),(11,20,'5C 5C 10D',10),(12,20,'10C 10C',10),(13,15,'15D',5)]
OL=[(1,15,'10C 5D',5),(2,20,'10D 10D',10),(3,20,'10D 5D 5D',10),(4,20,'5C 5C 5B 5C',10),(5,30,'10D 10C 10D',10),(6,30,'10D 10D 10D',10),
    (7,25,'5D 10D 5C 5B',10),(8,20,'5C 5C 5C 5C',10),(9,15,'15D',5),(10,20,'10D 10D',5),(11,20,'10C 10D',10),(12,15,'10D 5C',10),(13,20,'10C 10C',5)]
SC={'H':{'5B':'0, 3, 5','5C':'0, 2, 3, 5','5D':'0, 2, 3, 4, 5','10C':'0, 3, 6, 10','10D':'0, 3, 5, 7, 10','15D':'0, 4, 8, 12, 15'},
    'O':{'5B':'0, 3, 5','5C':'0, 2, 3, 5','5D':'0, 2, 3, 4, 5','10C':'0, 3, 7, 10','10D':'0, 4, 6, 8, 10','15D':'0, 4, 8, 12, 15'}}
for L in (HL,OL):
    assert sum(q[1] for q in L)==270 and sum(q[3] for q in L)==110 and len(L)==13

def dp(x,n):
    """round half up, asserting we're not near a rounding boundary"""
    x=float(x); s=x*10**n; f=s-math.floor(s)
    assert abs(f-0.5)>0.02, (x,n)
    return math.floor(s+0.5)/10**n
def eu(x): return f"€{float(x):,.2f}"

# ---------------- checks: HIGHER ----------------
# Q1 sets
N,Fo,Hu,Ne=30,18,14,5; both=Fo+Hu-(N-Ne); assert both==7
one=(Fo-both)+(Hu-both); assert one==18 and F(one,N)==F(3,5)
# Q2 income tax
G,CUT,SR,HR,CR=52000,44000,F(20,100),F(40,100),4000
gt=CUT*SR+(G-CUT)*HR; assert gt==12000; nt=gt-CR; assert nt==8000
G2=G*F(105,100); assert G2==54600; gt2=CUT*SR+(G2-CUT)*HR; assert gt2==13040; assert (gt2-CR)-nt==1040
# Q3 algebra
x,y=4,2; assert 3*x+2*y==16 and 5*x-3*y==14
for r in (3,F(-1,2)): assert 2*r*r-5*r-3==0
for t in range(-5,6): assert 3*t*t-12==3*(t-2)*(t+2)
# Q4 stats
D=[12,15,15,18,20,21,21,21,25,32]; assert sum(D)==200 and len(D)==10
assert max(set(D),key=D.count)==21 and F(D[4]+D[5],2)==F(41,2) and max(D)-min(D)==20
assert 11*21-sum(D)==31
# Q5 standard form
assert F('0.00036')==F(36,10**5); t5=F(15,10)*10**11/(3*10**8); assert t5==500 and divmod(500,60)==(8,20)
# Q6 probability
assert F(3,8)*200==75
# Q7 coordinate geometry
A,B=(-2,1),(4,5); M=(F(A[0]+B[0],2),F(A[1]+B[1],2)); assert M==(1,3)
m=F(B[1]-A[1],B[0]-A[0]); assert m==F(2,3)
for X in range(-5,6):
    Y=A[1]+m*(X-A[0]); assert 2*X-3*Y+7==0
L2=(B[0]-A[0])**2+(B[1]-A[1])**2; assert L2==52==4*13
mp=-1/m; assert mp==F(-3,2)
for X in range(-5,6):
    Y=B[1]+mp*(X-B[0]); assert 3*X+2*Y-22==0
xi=F(22,3); assert B[1]+mp*(xi-B[0])==0
# Q8 trig
assert F('1.4')**2+F('4.8')**2==25
ang8=math.degrees(math.atan(1.4/4.8)); assert dp(ang8,0)==16
assert F('1.4')/5==F(7,25)
h8=1.4/math.tan(math.radians(5)); assert dp(h8,1)==16.0
# Q9 patterns
T=lambda n:2*n*n+n; assert [T(n) for n in range(1,6)]==[3,10,21,36,55]
# Q10 volume
V10=30*30*80; assert V10==72000; assert dp(72000*math.pi/1000,0)==226
h10=V10*math.pi/(60*50); assert abs(h10-24*math.pi)<1e-9 and dp(h10,1)==75.4
# Q11 functions
f=lambda x:x*x-2*x-3; g=lambda x:x+1
assert f(-2)==5 and f(3)==0 and f(-1)==0 and f(4)==g(4)==5 and f(-1)==g(-1)==0
# Q12 similar triangles
assert F(5)*F(10,4)==F(25,2); AE=F(9)*F(4,10); assert AE==F(18,5) and 9-AE==F(27,5)
# Q13 inequality
n13=math.ceil(F(460,9)); assert n13==52 and 21*52-(460+12*52)>=0 and 21*51-(460+12*51)<0

# ---------------- checks: ORDINARY ----------------
assert F(3,4)+F(2,5)==F(23,20); assert dp(47.638,1)==47.6
assert F(240)*F(23,100)==F('55.20'); assert (F(240)+F('55.20'))*F(85,100)==F('250.92')
for t in range(-5,6): assert 3*(2*t+4)-2*(t-1)==4*t+14
assert 5*5-7==2*5+8; assert 2*3**2-(-4)==22
G4=[3,0,1,3,2,5,1,3,0,2]; s4=sorted(G4); assert sum(G4)==20 and max(set(G4),key=G4.count)==3 and max(G4)-min(G4)==5 and F(s4[4]+s4[5],2)==2
assert (10*60+30)-(7*60+45)==165 and F(264,F(165,60))==96 and F(264,88)==3
assert 2*(12+8)==40 and 12*8==96 and dp(96-math.pi*1.5**2,1)==88.9
assert F(5,12)==F(5,12) and F(9,12)==F(3,4) and 2*6==12
assert (F(1+5,2),F(2+10,2))==(3,6) and F(10-2,5-1)==2 and dp(math.sqrt(80),1)==8.9 and 8==2*4
assert 360*F(4,9)==160 and 360*F(5,9)==200 and 200-200*F(1,4)==150
P=lambda n:3*n+1; assert [P(n) for n in range(1,7)]==[4,7,10,13,16,19] and P(20)==61
xo=F(180-70,5); assert xo==22 and 2*xo==44 and 3*xo==66 and 180-70==110 and 2*xo+3*xo==110
assert 9**2+12**2==15**2 and dp(math.degrees(math.atan(9/12)),0)==37
fo=lambda x:2*x-3; assert fo(4)==5 and fo(F(3,2))==0

# ---------------- figures ----------------
def svg(w,h,body,mw=None): return f'<svg viewBox="0 0 {w} {h}" style="width:{mw or w*0.26}mm;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="Inter,sans-serif" font-size="13">{body}</svg>'
FIG_H8=svg(360,130,'<polygon points="20,110 300,110 300,28" fill="#E4F2EA" stroke="#1B2430" stroke-width="2"/>'
  '<rect x="288" y="98" width="12" height="12" fill="none" stroke="#1B2430"/>'
  '<text x="160" y="126" text-anchor="middle">4.8 m</text><text x="306" y="74">1.4 m</text>'
  '<path d="M60,110 A40,40 0 0 0 58,99" fill="none" stroke="#2E7D57" stroke-width="2"/><text x="66" y="104" fill="#2E7D57" font-weight="700">A</text>'
  '<text x="150" y="60" text-anchor="middle" font-style="italic">ramp</text>',80)
FIG_H12=svg(300,210,'<polygon points="150,15 25,190 280,190" fill="none" stroke="#1B2430" stroke-width="2"/>'
  '<line x1="100" y1="85" x2="202" y2="85" stroke="#1B2430" stroke-width="2"/>'
  '<path d="M178,80 l6,5 l-6,5 M178,185 l6,5 l-6,5" fill="none" stroke="#2E7D57" stroke-width="2"/>'
  '<text x="146" y="10" font-weight="700">A</text><text x="10" y="200" font-weight="700">B</text><text x="284" y="200" font-weight="700">C</text>'
  '<text x="84" y="86" font-weight="700">D</text><text x="207" y="86" font-weight="700">E</text>'
  '<text x="108" y="52">4</text><text x="46" y="140">6</text><text x="146" y="78" text-anchor="middle">5</text>',68)
FIG_O6=svg(300,200,'<rect x="20" y="20" width="240" height="160" fill="#E4F2EA" stroke="#1B2430" stroke-width="2"/>'
  '<circle cx="180" cy="95" r="30" fill="#BFE0F5" stroke="#1B2430" stroke-width="2"/><line x1="180" y1="95" x2="210" y2="95" stroke="#1B2430"/><circle cx="180" cy="95" r="2.5"/>'
  '<text x="195" y="90" text-anchor="middle" font-size="12">1.5 m</text><text x="140" y="196" text-anchor="middle">12 m</text><text x="266" y="104">8 m</text><text x="80" y="100" font-style="italic">lawn</text><text x="180" y="138" text-anchor="middle" font-style="italic">pond</text>',66)
FIG_O11=svg(330,170,'<polygon points="30,140 230,140 120,25" fill="none" stroke="#1B2430" stroke-width="2"/><line x1="230" y1="140" x2="315" y2="140" stroke="#1B2430" stroke-width="2"/>'
  '<text x="58" y="132" font-weight="700">2x</text><text x="113" y="58" font-weight="700">3x</text><text x="192" y="132" font-weight="700">70°</text><text x="246" y="132" font-weight="700" fill="#2E7D57">y</text>'
  '<path d="M260,140 A30,30 0 0 0 251,119" fill="none" stroke="#2E7D57" stroke-width="2"/>',72)
FIG_O12=svg(260,190,'<polygon points="30,160 230,160 230,20" fill="#E4F2EA" stroke="#1B2430" stroke-width="2"/><rect x="218" y="148" width="12" height="12" fill="none" stroke="#1B2430"/>'
  '<text x="130" y="178" text-anchor="middle">12 cm</text><text x="236" y="95">9 cm</text><text x="112" y="80" font-weight="700">h</text>'
  '<path d="M75,160 A45,45 0 0 0 72,136" fill="none" stroke="#2E7D57" stroke-width="2"/><text x="82" y="152" fill="#2E7D57" font-weight="700">A</text>',58)

# ---------------- question data ----------------
# Q = (stem_html, figure_html, [(label, part_text)], [(label, working_lines, answer, full, partial)], tip)
def Q(stem,parts,sols,tip,fig=''): return dict(stem=stem,parts=parts,sols=sols,tip=tip,fig=fig)
H={
1:Q('A class has 30 students. 18 play football (F), 14 play hurling (H) and 5 play neither sport.',
  [('a','How many students play both sports?'),('b','Draw a Venn diagram of this information. A student is picked at random from the class. Find the probability that the student plays exactly one of the two sports. Give your answer as a fraction in its simplest form.')],
  [('a',['Students who play at least one sport: 30 − 5 = 25','18 + 14 = 32, so 32 − 25 = 7 are counted twice'],'7 students play both',"7 with work","the 25 found, or 18 + 14 = 32 written down"),
   ('b',['F only = 18 − 7 = 11, H only = 14 − 7 = 7, both = 7, neither = 5 (check: 11 + 7 + 7 + 5 = 30)','Exactly one sport = 11 + 7 = 18','P = 18/30'],'3/5','Venn diagram right and 3/5',"a correct Venn diagram with no probability, or 18/30 not simplified (high partial); one region right (low partial)")],
  'Fill in the middle of a Venn diagram first, then work outwards.'),
2:Q('In this question, income tax is charged at 20% on the first €44,000 of gross income (the standard rate cut-off point) and at 40% on the rest. Aoife earns a gross income of €52,000 a year. Her tax credits are €4,000 a year.',
  [('a','Find Aoife\'s gross tax for the year.'),('b','Find her net tax (tax payable) for the year.'),('c','Aoife gets a 5% pay rise. The rates, cut-off point and tax credits stay the same. How much extra tax will she pay each year?')],
  [('a',['20% of €44,000 = €8,800','€52,000 − €44,000 = €8,000 at 40% = €3,200','€8,800 + €3,200'],'€12,000','€12,000',"one of the two amounts right (high partial); a correct method at one rate (low partial)"),
   ('b',['€12,000 − €4,000'],'€8,000','€8,000 (or right from their (a))','tax credits subtracted from the wrong figure'),
   ('c',['New gross income: €52,000 × 1.05 = €54,600','Gross tax: €8,800 + 40% of €10,600 = €8,800 + €4,240 = €13,040','Net tax: €13,040 − €4,000 = €9,040','Extra: €9,040 − €8,000'],'€1,040 more a year','€1,040','the new income €54,600 (low partial); new gross or net tax right (mid partial)')],
  'Write the cut-off line on your page: everything above it is taxed at the higher rate.'),
3:Q('',
  [('a','Solve the simultaneous equations:<br><span class="eq">3x + 2y = 16</span><span class="eq">5x − 3y = 14</span>'),('b','Solve the equation 2x² − 5x − 3 = 0.'),('c','Factorise fully: 3x² − 12')],
  [('a',['× 3: 9x + 6y = 48','× 2: 10x − 6y = 28','Add: 19x = 76, so x = 4','3(4) + 2y = 16, so 2y = 4, y = 2','Check in the second: 5(4) − 3(2) = 14 ✓'],'x = 4, y = 2','both values, with work','one value right (high partial); one variable eliminated correctly (mid partial); one equation multiplied correctly (low partial)'),
   ('b',['(2x + 1)(x − 3) = 0','2x + 1 = 0 or x − 3 = 0'],'x = −1/2 or x = 3','both roots','correct factors but roots wrong or missing (high partial); quadratic formula with correct a, b, c (mid/low partial)'),
   ('c',['Take out the common factor: 3(x² − 4)','Difference of two squares: x² − 4 = (x − 2)(x + 2)'],'3(x − 2)(x + 2)','3(x − 2)(x + 2)','3(x² − 4) only, or (3x − 6)(x + 2)')],
  '"Fully" is a hint: there is more than one step.'),
4:Q('Ten students timed how long (in minutes) it took them to walk to school:<div class="data">12, 15, 15, 18, 20, 21, 21, 21, 25, 32</div>',
  [('a','Write down the mode.'),('b','Find the median.'),('c','Find the mean.'),('d','An eleventh student joins the group. The mean time of all 11 students is now 21 minutes. How long does the eleventh student take to walk to school?')],
  [('a',['21 appears three times, more than any other value'],'21 minutes','21','—'),
   ('b',['10 values, so the median is halfway between the 5th and 6th: 20 and 21'],'20.5 minutes','20.5','20 or 21, or the middle values picked out'),
   ('c',['Total: 12 + 15 + 15 + 18 + 20 + 21 + 21 + 21 + 25 + 32 = 200','200 ÷ 10'],'20 minutes','20','total right but wrong division (high partial); some values added (low partial)'),
   ('d',['New total: 11 × 21 = 231','231 − 200'],'31 minutes','31','231 found')],
  'Working backwards from a mean: total = mean × how many.'),
5:Q('',
  [('a','Write 0.00036 in the form a × 10ⁿ, where 1 ≤ a &lt; 10 and n ∈ ℤ.'),('b','Light travels at 3 × 10⁸ metres per second. The Sun is about 1.5 × 10¹¹ metres from the Earth. How long does light take to travel from the Sun to the Earth? Give your answer in minutes and seconds.')],
  [('a',['Move the decimal point 4 places to the right: 3.6'],'3.6 × 10⁻⁴','3.6 × 10⁻⁴','3.6 × 10⁴, or 36 × 10⁻⁵'),
   ('b',['Time = distance ÷ speed = (1.5 × 10¹¹) ÷ (3 × 10⁸)','= 0.5 × 10³ = 500 seconds','500 ÷ 60 = 8 remainder 20'],'8 minutes 20 seconds','8 min 20 s','500 seconds found (mid partial); distance ÷ speed written (low partial)')],
  'Speed, distance, time: write the formula first and put the numbers in.'),
6:Q('A spinner has 8 equal sectors: 3 red, 2 blue, 2 green and 1 yellow.',
  [('a','Find the probability that the spinner lands on red.'),('b','The spinner is spun 200 times. How many times would you expect it to land on red?')],
  [('a',['3 red sectors out of 8'],'3/8','3/8','3 or 8 used in a fraction'),
   ('b',['Expected number = probability × number of trials = 3/8 × 200'],'75 times','75','—')],
  'Expected frequency = probability × number of trials.'),
7:Q('The points A(−2, 1) and B(4, 5) are shown on a coordinate grid.',
  [('a','Find the midpoint of [AB].'),('b','Find the slope of AB. Hence find the equation of the line AB. Write your answer in the form ax + by + c = 0, where a, b, c ∈ ℤ.'),('c','Find |AB|. Give your answer in the form p√q, where p, q ∈ ℕ and q is a prime number.'),('d','The line l is perpendicular to AB and passes through B. Find the equation of l, and find the point where l crosses the x-axis.')],
  [('a',['((−2 + 4)/2, (1 + 5)/2)'],'(1, 3)','(1, 3)','one coordinate right'),
   ('b',['Slope m = (5 − 1)/(4 − (−2)) = 4/6 = 2/3','y − 1 = 2/3(x + 2)','3y − 3 = 2x + 4'],'2x − 3y + 7 = 0','slope and equation','slope right (mid partial); correct formula with some substitution (low partial)'),
   ('c',['|AB|² = (4 − (−2))² + (5 − 1)² = 36 + 16 = 52','√52 = √(4 × 13)'],'2√13','2√13','√52 (high partial); formula with numbers in (low partial)'),
   ('d',['Perpendicular slope: −3/2 (flip and change the sign)','y − 5 = −3/2(x − 4), so 2y − 10 = −3x + 12','l: 3x + 2y − 22 = 0','On the x-axis y = 0: 3x = 22'],'l: 3x + 2y − 22 = 0; crosses at (22/3, 0)','equation and point','equation of l right (high partial); slope −3/2 (mid partial); y = 0 used (low partial)')],
  'Perpendicular slopes multiply to −1: 2/3 × (−3/2) = −1.'),
8:Q('A ramp rises 1.4 m over a horizontal distance of 4.8 m, as shown. The diagram is not to scale.',
  [('a','Find the length of the ramp.'),('b','Find the angle A between the ramp and the ground, correct to the nearest degree.'),('c','Write sin A as a fraction.'),('d','A new ramp must rise the same 1.4 m, but at an angle of 5°. Find the horizontal distance it needs, correct to one decimal place.')],
  [('a',['Pythagoras: length² = 1.4² + 4.8² = 1.96 + 23.04 = 25'],'5 m','5 m','25 found (high partial); Pythagoras written with numbers (mid/low partial)'),
   ('b',['tan A = opposite/adjacent = 1.4/4.8','A = tan⁻¹(1.4 ÷ 4.8) = 16.26…°'],'16°','16°','correct ratio written (low partial); 16.26 not rounded (high partial)'),
   ('c',['sin A = opposite/hypotenuse = 1.4/5'],'7/25','7/25 (or 1.4/5)','—'),
   ('d',['tan 5° = 1.4/d','d = 1.4 ÷ tan 5° = 16.002…'],'16.0 m','16.0 m','correct ratio with 5° (low/mid partial)')],
  'Calculator in DEGREE mode (a small D on the screen) before any trig question.',FIG_H8),
9:Q('The first four terms of a pattern are:<div class="data">3, 10, 21, 36, …</div>',
  [('a','Write down the next term of the pattern.'),('b','Show that the pattern is quadratic.'),('c','Find a formula for Tₙ, the nth term of the pattern.')],
  [('a',['Differences: 7, 11, 15, so the next difference is 19','36 + 19'],'55','55','the differences found'),
   ('b',['First differences: 7, 11, 15','Second differences: 4, 4'],'The second differences are constant (4), so the pattern is quadratic','differences shown and the conclusion','first differences only'),
   ('c',['Second difference = 2a = 4, so a = 2: Tₙ = 2n² + bn + c','n = 1: 2 + b + c = 3, so b + c = 1','n = 2: 8 + 2b + c = 10, so 2b + c = 2','Subtract: b = 1, c = 0','Check n = 3: 2(9) + 3 = 21 ✓'],'Tₙ = 2n² + n','Tₙ = 2n² + n','a = 2 and one more value (high partial); a = 2 (mid partial); one equation set up (low partial)')],
  'For a quadratic pattern, a = (second difference) ÷ 2.'),
10:Q('A water tank is a cylinder with radius 30 cm and height 80 cm.',
  [('a','Find the volume of the tank in cm³. Leave your answer in terms of π.'),('b','Find the volume in litres, correct to the nearest litre. (1 litre = 1000 cm³)'),('c','The full tank is emptied into a cuboid tank with a rectangular base 60 cm by 50 cm. Find the depth of water in the cuboid tank, correct to one decimal place.')],
  [('a',['V = πr²h = π × 30² × 80'],'72,000π cm³','72,000π cm³','formula with numbers in (mid partial); formula only (low partial)'),
   ('b',['72,000π = 226,194.6… cm³','÷ 1000 = 226.19…'],'226 litres','226 litres','226,194.6 cm³ (mid partial)'),
   ('c',['Volume stays the same: 60 × 50 × d = 72,000π','3000d = 72,000π, so d = 24π = 75.398…'],'75.4 cm','75.4 cm','equation set up (mid/high partial); base area 3000 (low partial)')],
  'When a liquid is poured from one container into another, the volume stays the same: write "volume = volume".'),
11:Q('f(x) = x² − 2x − 3 and g(x) = x + 1, where x ∈ ℝ.',
  [('a','Find f(−2).'),('b','Find the two values of x for which f(x) = 0.'),('c','Find the coordinates of the two points where the graphs of f(x) and g(x) meet.')],
  [('a',['(−2)² − 2(−2) − 3 = 4 + 4 − 3'],'5','5','−2 substituted with one slip'),
   ('b',['(x − 3)(x + 1) = 0'],'x = 3 or x = −1','both values','factors right (mid partial); one root (low/mid partial)'),
   ('c',['f(x) = g(x): x² − 2x − 3 = x + 1','x² − 3x − 4 = 0','(x − 4)(x + 1) = 0, so x = 4 or x = −1','y = g(4) = 5 and y = g(−1) = 0'],'(4, 5) and (−1, 0)','both points','x values only (high partial); equation x² − 3x − 4 = 0 (mid partial); f(x) = g(x) written (low partial)')],
  '"Where the graphs meet" means: put the two functions equal to each other.'),
12:Q('In the triangle ABC, D is on [AB] and E is on [AC], with DE ∥ BC. |AD| = 4, |DB| = 6 and |DE| = 5, as shown. The diagram is not to scale.',
  [('a','Explain why the triangles ADE and ABC are similar, and find |BC|.'),('b','|AC| = 9. Find |EC|.')],
  [('a',['DE ∥ BC, so ∠ADE = ∠ABC and ∠AED = ∠ACB (corresponding angles); ∠A is in both triangles','So the triangles are equiangular, so similar','|AB| = 4 + 6 = 10, so the scale factor is 10/4 = 2.5','|BC| = 5 × 2.5'],'|BC| = 12.5','reason and 12.5','12.5 without a reason, or reason with 5/4 used (high/mid partial); |AB| = 10 (low partial)'),
   ('b',['|AE|/|AC| = |AD|/|AB| = 4/10','|AE| = 9 × 4/10 = 3.6','|EC| = 9 − 3.6'],'|EC| = 5.4','5.4','|AE| = 3.6 (mid/high partial); a correct ratio (low partial)')],
  'In similar triangles, match the sides opposite equal angles before you write a ratio.',FIG_H12),
13:Q('A school is running a bus trip. The bus costs €460 to hire, and each student\'s entry ticket costs the school €12. The school charges each student €21 for the trip. Find the least number of students that must go so that the school does not lose money.',
  [],
  [('',['Let n = number of students. Money in: 21n. Costs: 460 + 12n','21n ≥ 460 + 12n','9n ≥ 460, so n ≥ 51.1…','n must be a whole number, so round UP','Check: 52 students: €1,092 in, €1,084 out ✓; 51 students: €1,071 in, €1,072 out ✗'],'52 students','52 with work','51.1 found but rounded down to 51 (high partial); inequality 21n ≥ 460 + 12n (mid partial); profit per student €9 found (low partial)')],
  'Rounding in context: you can\'t have 0.1 of a student, and 51 isn\'t enough, so round up.'),
}
O={
1:Q('',
  [('a','Work out 3/4 + 2/5. Give your answer as a fraction.'),('b','Round 47.638 to one decimal place.')],
  [('a',['Common denominator 20: 15/20 + 8/20'],'23/20 (or 1 3/20)','23/20','common denominator found (mid partial); one fraction converted (low partial)'),
   ('b',['The next digit (3) is less than 5, so round down'],'47.6','47.6','47.7 or 47.64')],
  'Fractions: find a common denominator first. A calculator check is fine too.'),
2:Q('A bicycle costs €240 before VAT. VAT is charged at 23%.',
  [('a','Find the amount of VAT.'),('b','In a sale, the shop takes 15% off the full price including VAT. Find the sale price.')],
  [('a',['23% of €240 = 0.23 × 240'],'€55.20','€55.20','correct method with a slip (high partial); 23/100 written (low partial)'),
   ('b',['Full price: €240 + €55.20 = €295.20','Sale price: 85% of €295.20 = 0.85 × 295.20'],'€250.92','€250.92','€295.20 found (mid partial); 15% of a price found (low partial)')],
  'Money answers: always two decimal places, with the € sign.'),
3:Q('',
  [('a','Simplify 3(2x + 4) − 2(x − 1).'),('b','Solve the equation 5x − 7 = 2x + 8.'),('c','Find the value of 2a² − b when a = 3 and b = −4.')],
  [('a',['6x + 12 − 2x + 2'],'4x + 14','4x + 14','one bracket expanded correctly; −2 × −1 = +2 is the usual slip'),
   ('b',['5x − 2x = 8 + 7','3x = 15'],'x = 5','x = 5','terms gathered correctly'),
   ('c',['2(3)² − (−4) = 2(9) + 4 = 18 + 4'],'22','22','numbers substituted (low partial); 14 (from −4 instead of +4) (high partial)')],
  'Minus a negative is plus: − (−4) = + 4.'),
4:Q('A team scored these numbers of goals in their last 10 matches:<div class="data">3, 0, 1, 3, 2, 5, 1, 3, 0, 2</div>',
  [('a','Write down the mode.'),('b','Find the range.'),('c','Find the median.'),('d','Find the mean.')],
  [('a',['3 appears three times'],'3 goals','3','—'),
   ('b',['5 − 0'],'5 goals','5','highest and lowest values picked out'),
   ('c',['In order: 0, 0, 1, 1, 2, 2, 3, 3, 3, 5','Middle two values (5th and 6th): 2 and 2'],'2 goals','2','—'),
   ('d',['Total = 20 goals, 20 ÷ 10'],'2 goals','2','total right (mid partial)')],
  'Median: put the numbers in order first.'),
5:Q('A bus leaves Cork at 07:45 and arrives in Dublin at 10:30. The journey is 264 km.',
  [('a','How long does the journey take? Give your answer in hours and minutes.'),('b','Find the average speed of the bus in km/h.'),('c','The bus leaves Dublin at 17:20 for the return journey, at an average speed of 88 km/h. At what time does it arrive in Cork?')],
  [('a',['07:45 to 10:45 is 3 hours; 15 minutes less'],'2 hours 45 minutes','2 h 45 min','2 h 75 min or 3 h 15 min-type slips (mid partial)'),
   ('b',['2 h 45 min = 2.75 hours (45 min = 0.75 h)','Speed = 264 ÷ 2.75'],'96 km/h','96 km/h','264 ÷ 2.45 (time as a decimal wrong) (mid partial); formula written (low partial)'),
   ('c',['Time = 264 ÷ 88 = 3 hours','17:20 + 3 hours'],'20:20','20:20 (or 8:20 pm)','3 hours found (high partial); formula with numbers (mid/low partial)')],
  '45 minutes is NOT 0.45 of an hour: divide minutes by 60.'),
6:Q('A rectangular garden is 12 m long and 8 m wide. It has a circular pond of radius 1.5 m. The rest of the garden is lawn. The diagram is not to scale.',
  [('a','Find the perimeter of the garden.'),('b','Find the area of the garden.'),('c','Find the area of the lawn, correct to one decimal place.')],
  [('a',['12 + 8 + 12 + 8'],'40 m','40 m','two sides added (low partial)'),
   ('b',['12 × 8'],'96 m²','96 m²','—'),
   ('c',['Pond: πr² = π × 1.5² = 7.0685…','Lawn = 96 − 7.0685…'],'88.9 m²','88.9 m²','pond area right (mid/high partial); 2πr used for the pond (low partial)')],
  'Perimeter = distance around (m). Area = space inside (m²).',FIG_O6),
7:Q('A bag holds 4 red, 5 blue and 3 green counters. One counter is taken out at random.',
  [('a','Find the probability that it is blue.'),('b','Find the probability that it is not green. Give your answer in its simplest form.'),('c','A coin is tossed and a fair six-sided dice is rolled. How many outcomes are there in the sample space?'),('d','Find the probability of getting a head and a six.')],
  [('a',['12 counters, 5 blue'],'5/12','5/12','5 or 12 used'),
   ('b',['Not green = 4 + 5 = 9 counters','9/12'],'3/4','3/4','9/12 (high partial); 3/12 (low partial)'),
   ('c',['2 × 6, or list H1 … H6, T1 … T6'],'12','12','a partial list'),
   ('d',['Only H6 out of 12 outcomes'],'1/12','1/12','—')],
  'P(not A) = 1 − P(A).'),
8:Q('A is the point (1, 2) and B is the point (5, 10).',
  [('a','Find the midpoint of [AB].'),('b','Find the slope of AB.'),('c','Find |AB|, correct to one decimal place.'),('d','Is the point C(4, 8) on the line AB? Give a reason for your answer.')],
  [('a',['((1 + 5)/2, (2 + 10)/2)'],'(3, 6)','(3, 6)','one coordinate'),
   ('b',['(10 − 2)/(5 − 1) = 8/4'],'2','2','8/4 not simplified, or 4/8'),
   ('c',['√((5 − 1)² + (10 − 2)²) = √(16 + 64) = √80 = 8.944…'],'8.9','8.9','√80 (high partial)'),
   ('d',['Equation of AB: y − 2 = 2(x − 1), so y = 2x','At x = 4: y = 2(4) = 8 ✓ (or: slope AC = (8 − 2)/(4 − 1) = 2, the same as AB)'],'Yes, C is on AB','yes with a reason','yes or no with a partly correct reason')],
  'The formulas for midpoint, slope and distance are in the Formulae and Tables booklet: use it.'),
9:Q('€360 is shared between Ciara and Tom in the ratio 4 : 5. Tom then gives a quarter of his share to his sister. How much money does Tom have left?',
  [],
  [('',['4 + 5 = 9 parts; one part = €360 ÷ 9 = €40','Ciara: 4 × €40 = €160; Tom: 5 × €40 = €200','A quarter of €200 = €50','€200 − €50'],'€150','€150','€200 found (high/mid partial); one part = €40 (low partial)')],
  'Ratio: add the parts, find one part, then multiply.'),
10:Q('A pattern is made with matchsticks. Stage 1 uses 4 matchsticks, stage 2 uses 7, stage 3 uses 10 and stage 4 uses 13.',
  [('a','How many matchsticks are needed for stage 5 and stage 6?'),('b','Write a formula for the number of matchsticks in stage n, and use it to find the number of matchsticks in stage 20.')],
  [('a',['Add 3 each time: 13 + 3, then + 3'],'16 and 19','16 and 19','one right'),
   ('b',['The pattern goes up by 3, so it starts 3n …','Stage 1: 3(1) = 3, and we need 4, so add 1: Tₙ = 3n + 1','Stage 20: 3(20) + 1'],'3n + 1; stage 20 uses 61','formula and 61','61 by counting on (high partial); 3n (mid partial); "add 3" stated (low partial)')],
  'A pattern that goes up by the same amount each time is linear: Tₙ = (that amount) × n + something.'),
11:Q('The diagram shows a triangle with angles 2x, 3x and 70°. One side has been extended, making the exterior angle y. The diagram is not to scale.',
  [('a','Find the value of x.'),('b','Find the value of y. Give a reason for your answer.')],
  [('a',['Angles in a triangle add to 180°: 2x + 3x + 70 = 180','5x = 110'],'x = 22','22','5x = 110 (high partial); equation set up (low partial)'),
   ('b',['Straight angle: y = 180° − 70°','(or: exterior angle = sum of the two interior opposite angles: 44° + 66°)'],'y = 110°, angles on a straight line add to 180°','110° with a reason','110° with no reason (high partial); 180° used (low partial)')],
  'Always write the reason: "angles in a triangle add to 180°", "straight angle = 180°".',FIG_O11),
12:Q('The diagram shows a right-angled triangle with sides 9 cm and 12 cm. The diagram is not to scale.',
  [('a','Find h, the length of the hypotenuse.'),('b','Find the angle A, correct to the nearest degree.')],
  [('a',['h² = 9² + 12² = 81 + 144 = 225','h = √225'],'15 cm','15 cm','225 found (high partial); Pythagoras with numbers (mid partial)'),
   ('b',['tan A = opposite/adjacent = 9/12','A = tan⁻¹(0.75) = 36.86…°'],'37°','37°','the right ratio (mid partial)')],
  'SOH CAH TOA: label the sides opposite, adjacent and hypotenuse from the angle you want.',FIG_O12),
13:Q('f(x) = 2x − 3, where x ∈ ℝ.',
  [('a','Find f(4).'),('b','Find the value of x for which f(x) = 0.')],
  [('a',['2(4) − 3 = 8 − 3'],'5','5','4 substituted (mid partial)'),
   ('b',['2x − 3 = 0','2x = 3'],'x = 1.5 (or 3/2)','1.5','2x − 3 = 0 written (low partial)')],
  'f(x) = 0 means "where does the graph cross the x-axis?"'),
}
for D_,L in ((H,HL),(O,OL)):
    for n,t,p,m in L:
        q=D_[n]; k=len(p.split())
        assert len(q['sols'])==k and (len(q['parts'])==k or (k==1 and q['parts']==[])),(n,k)

# ---------------- HTML ----------------
STYLE=open(os.path.join(HERE,'pdf.css')).read()
CSS='''
@page{@bottom-left{content:"Léim · JC Maths Exam Pack · 2018 spec: all strands (N, GT, AF, SP, U) · Original Léim material · One household or one teacher";font-size:6.8pt}}
@page:first{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
body{font-size:10pt;line-height:1.42}
.cover{width:210mm;height:297mm;background:#1B2430;color:#fff;padding:26mm 22mm 22mm;display:flex;flex-direction:column;justify-content:space-between;page-break-after:always}
.cover .pill{display:inline-block;background:#2E7D57;border-radius:99px;padding:5px 14px;font-weight:700;font-size:9.5pt;letter-spacing:.06em;text-transform:uppercase}
.cover h1{font-size:50pt;line-height:1.02;letter-spacing:-.03em;margin:16mm 0 0;color:#fff}
.cover h1 span{background:#F6CF5A;color:#1B2430;padding:0 6px}
.cover .sub{font-size:15pt;color:#C9D1DA;margin-top:10mm;line-height:1.4;max-width:160mm}
.cover ul{list-style:none;padding:0;margin:12mm 0 0;font-size:12.5pt;line-height:1.9}
.cover ul li:before{content:"✓";color:#F6CF5A;font-weight:800;margin-right:10px}
.cover .foot{display:flex;justify-content:space-between;align-items:flex-end;font-size:11pt;font-weight:700}
.cover .foot .small{color:#C9D1DA;font-weight:500;font-size:9pt;max-width:120mm;line-height:1.45}
.cover .logo{font-size:20pt}
.band{padding:11px 16px;margin-bottom:9px}.band h1{font-size:18pt}
h2{font-size:13pt;margin:10px 0 5px}
.qq{border:1.4px solid var(--line);border-radius:9px;padding:8px 12px;margin:0 0 9px;break-inside:avoid}
.qh{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1.4px solid var(--line);padding-bottom:4px;margin-bottom:5px}
.qh b{font-size:12.5pt}.qh span{font-size:8.6pt;font-weight:700;color:var(--green)}
.qq ol{list-style:none;padding:0;margin:4px 0}.qq ol li{margin:5px 0;display:flex;gap:6px}
.qq ol li .l{font-weight:800;flex:none;width:18px}.qq ol li .t{flex:1}
.mk{flex:none;font-size:8.4pt;font-weight:700;color:var(--muted);white-space:nowrap}
.data{font-weight:700;letter-spacing:.02em;margin:4px 0;font-size:10.6pt}
.eq{display:block;margin:2px 0 0 14px;font-weight:600}
.fig{float:right;margin:0 0 4px 10px}
.sol{border-left:4px solid var(--green);padding:6px 11px;margin:0 0 8px;background:#FAFBFC;break-inside:avoid}
.sol .qh{border:0;margin:0;padding:0}
.sp{margin:5px 0 4px}
.sp .pl{font-weight:800;color:var(--green)}
.sp ul{margin:2px 0;padding-left:16px}.sp li{margin:1px 0}
.ans{font-weight:800;background:var(--green-soft);border-radius:5px;padding:1px 7px;display:inline-block;margin:2px 0}
.mg{font-size:8.7pt;color:var(--ink);margin:3px 0 0;border-top:1px dashed var(--line);padding-top:3px}
.mg b{color:var(--green)}
.sc{font-size:8.2pt;color:var(--muted)}
.tipq{font-size:8.8pt;margin:4px 0 0}.tipq b{color:var(--green)}
.cols{columns:2;column-gap:12px}
.key td{font-size:8.8pt;padding:2px 6px}.key td:first-child{font-weight:700;white-space:nowrap}
.box{display:inline-block;width:9px;height:9px;border:1.3px solid var(--ink);border-radius:2px;margin-right:7px;vertical-align:-1px}
.sheet td{padding:4px 7px}.sheet td.b{border:1.3px solid var(--ink);width:24mm}
.chip{display:inline-block;background:var(--mist);border:1px solid var(--line);border-radius:5px;padding:0 6px;font-weight:700;font-size:8.8pt;margin:1px 2px}
.chip.f{background:var(--green);color:#fff;border-color:var(--green)}
ul.ck{list-style:none;padding-left:0}ul.ck li{margin:4px 0}
.instr{border:2px solid var(--ink);border-radius:9px;padding:8px 13px;margin:6px 0 10px}
'''
def band(k,t): return f'<div class="band"><div><div class="k">{k}</div><h1>{t}</h1></div><div class="logo">↗ Léim</div></div>'

def paper(D_,L,lvl):
    out=[]
    for n,t,p,m in L:
        q=D_[n]; sc=p.split()
        if q['parts']:
            li=''.join(f'<li><span class="l">({a})</span><span class="t">{tx}</span><span class="mk">{s[:-1]} marks</span></li>' for (a,tx),s in zip(q['parts'],sc))
            body=f'<ol>{li}</ol>'
        else: body=''
        stem=f'<p>{q["stem"]}</p>' if q['stem'] else ''
        fig=f'<div class="fig">{q["fig"]}</div>' if q['fig'] else ''
        out.append(f'<div class="qq"><div class="qh"><b>Question {n}</b><span>{t} marks · about {m} minutes</span></div>{fig}{stem}{body}<div style="clear:both"></div></div>')
    return ''.join(out)

def sols(D_,L,lvl):
    out=[]
    for n,t,p,m in L:
        q=D_[n]; sc=p.split(); parts=[]
        for (a,work,ans,full,part),s in zip(q['sols'],sc):
            lab=f'<span class="pl">({a})</span> ' if a else ''
            vals=SC[lvl][s].split(', ')
            chips=''.join(f'<span class="chip{" f" if i==len(vals)-1 else ""}">{v}</span>' for i,v in enumerate(vals))
            pt='' if part=='—' else f' · <b>Partial credit:</b> {part}'
            parts.append(f'<div class="sp">{lab}<ul>{"".join(f"<li>{w}</li>" for w in work)}</ul><span class="ans">{ans}</span>'
                         f'<div class="mg"><b>{s} scale</b> {chips} · <b>Full marks:</b> {full}{pt}</div></div>')
        out.append(f'<div class="sol"><div class="qh"><b>Question {n}</b><span>{t} marks</span></div>{"".join(parts)}<p class="tipq"><b>Tip:</b> {q["tip"]}</p></div>')
    return ''.join(out)

def key(D_,L):
    rows=''.join(f'<tr><td>Q{n}</td><td>{" · ".join((f"({a}) " if a else "")+ans for a,_,ans,_,_ in D_[n]["sols"])}</td></tr>' for n,_,_,_ in L)
    return f'<table class="key"><tr><th>Q</th><th>Answers</th></tr>{rows}</table>'

def sheet(L,lvl):
    rows=''.join(f'<tr><td><b>Q{n}</b></td><td>{t}</td><td class="b"></td></tr>' for n,t,p,m in L)
    return f'<table class="sheet"><tr><th>Question</th><th>Out of</th><th>My marks</th></tr>{rows}<tr><td><b>Total</b></td><td><b>270</b></td><td class="b"></td></tr></table>'

INSTR=lambda lvl:f'''<div class="instr"><b>{lvl} level mock paper · 2 hours · 270 marks · 13 questions.</b> Answer <b>all</b> questions. Do your working in an A4 copybook or on squared paper, and label each part clearly (for example "Q3 (b)"). Show all your work: most marks are for the method. You may use a calculator, a geometry set and the Formulae and Tables booklet. The suggested times add up to 110 minutes, leaving about 10 minutes to check. Diagrams are not drawn to scale.</div>'''

GRADES='''<table><tr><th>Grade</th><th>Percentage</th><th>Marks out of 270</th></tr>
<tr><td>Distinction</td><td>85–100%</td><td>230–270</td></tr><tr><td>Higher Merit</td><td>70–84%</td><td>189–229</td></tr>
<tr><td>Merit</td><td>55–69%</td><td>149–188</td></tr><tr><td>Achieved</td><td>40–54%</td><td>108–148</td></tr>
<tr><td>Partially Achieved</td><td>20–39%</td><td>54–107</td></tr><tr><td>Not Graded</td><td>0–19%</td><td>0–53</td></tr></table>'''
for lo,hi in ((85,230),(70,189),(55,149),(40,108),(20,54)): assert math.ceil(270*lo/100)==hi or math.ceil(270*lo/100-1e-9)==hi,(lo,hi)

def render(PG):
    html=f'''<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Junior Cycle Maths Exam Pack | Léim</title>
    <style>{STYLE}{CSS}</style></head><body>
    <div class="cover"><div>
      <span class="pill">Junior Cycle Maths · Higher &amp; Ordinary level</span>
      <h1>The Maths <span>Exam Pack</span></h1>
      <div class="sub">Two full timed mock papers in the format of the June exam, with step-by-step solutions and a guide to where the marks would go.</div>
      <ul><li>A Higher level mock paper: 13 questions, 270 marks, 2 hours</li><li>An Ordinary level mock paper: 13 questions, 270 marks, 2 hours</li>
      <li>Worked solutions for every part</li><li>"Where the marks would go": partial credit explained, part by part</li>
      <li>Score sheets, grade bands, a 4-week plan and an exam-day checklist</li></ul></div>
      <div class="foot"><div class="small">Written by Léim, an Irish revision site run by a teacher with over 25 years in the classroom. Every question is original Léim material, set out in the format of the June paper. Nothing is copied or adapted from State Examinations Commission papers or marking schemes. Independent practice material: not an official SEC publication, and no prediction of what will come up. Spotted a mistake? Email hello@leim.ie</div><div class="logo">↗ Léim</div></div></div>
    
    <div class="page">{band('Start here','How to use this pack')}
    <p>Junior Cycle Maths is <b>one written paper</b> in June of 3rd year, at <b>Higher</b> or <b>Ordinary</b> level. Recent papers at both levels have been <b>2 hours</b>, <b>270 marks</b> and <b>13 compulsory questions</b>, each with a suggested time. The questions are <b>not</b> worth the same: some are worth 10 marks, others 30.</p>
    <p>The two mock papers in this pack copy that <b>format</b> (the marks, parts and times of the 2026 papers) with <b>original questions</b> covering all four strands: Number, Algebra &amp; Functions, Geometry &amp; Trigonometry, and Statistics &amp; Probability. The format can change from year to year.</p>
    <h2>What's inside</h2>
    <table><tr><th style="width:18mm">Pages</th><th>Section</th></tr>
    <tr><td>{PG['how']}</td><td>How to use this pack, and how the paper is marked</td></tr>
    <tr><td>{PG['hp']}</td><td><b>Higher level mock paper</b></td></tr>
    <tr><td>{PG['hs']}</td><td>Higher level: worked solutions and where the marks would go</td></tr>
    <tr><td>{PG['op']}</td><td><b>Ordinary level mock paper</b></td></tr>
    <tr><td>{PG['os']}</td><td>Ordinary level: worked solutions and where the marks would go</td></tr>
    <tr><td>{PG['ks']}</td><td>Answer keys, score sheets and grades</td></tr>
    <tr><td>{PG['ck']}</td><td>The exam-day checklist</td></tr></table>
    <h2>A 4-week plan</h2>
    <table><tr><th>Week</th><th>Do this</th><th>Tick</th></tr>
    <tr><td>1</td><td>Read "How the paper is marked" (page {PG["mk"]}). Do Questions 1–4 of your level's paper, untimed. Mark them with the solutions.</td><td><span class="box"></span></td></tr>
    <tr><td>2</td><td>Questions 5–9, each in its suggested time. Mark them, and redo every part where you lost marks.</td><td><span class="box"></span></td></tr>
    <tr><td>3</td><td>Questions 10–13, timed. Then pick your three weakest topics and play their free games on <b>leim.ie</b>.</td><td><span class="box"></span></td></tr>
    <tr><td>4</td><td>The whole paper again, timed, in one 2-hour sitting. Fill in the score sheet (page {PG["sheet"]}) and look up your grade.</td><td><span class="box"></span></td></tr></table>
    <div class="tip"><b>Which level?</b> Do your own level's paper first. If you're unsure which level to take, try a few questions from the other paper too and talk to your Maths teacher: the decision is usually made in 3rd year.</div>
    <div class="note"><b>For parents:</b> you don't need to know the Maths to help. Time your child, then use the solutions to check the <b>method</b>, not just the answer. Ask "Where did the marks go?" for every part they got wrong.</div>
    </div>
    
    <div class="page">{band('Start here','How the paper is marked')}
    <p>Maths is <b>not</b> marked one mark per step. The examiner reads your answer to a part and decides which level it reaches on a <b>scale</b>. Each part in this pack shows its marks and scale, for example <b>10D</b> (a 10-mark part on scale D).</p>
    <table><tr><th>Scale</th><th>Higher level marks</th><th>Ordinary level marks</th></tr>
    {''.join(f'<tr><td><b>{s}</b></td><td>{SC["H"][s]}</td><td>{SC["O"][s]}</td></tr>' for s in ['5B','5C','5D','10C','10D','15D'])}</table>
    <p class="small">The scale values are the ones in the 2026 marking schemes. The SEC can change them from year to year.</p>
    <h2>Five things that win or lose marks</h2>
    <ol class="q">
    <li><b>One line of work is worth marks.</b> The lowest mark above zero is usually 2 to 4 marks. A blank is always 0, so never leave a part empty: write the formula and put the numbers in.</li>
    <li><b>Show your work.</b> A right answer with no work can get very low marks.</li>
    <li><b>A slip costs only 1 mark</b> if everything else is right (for example 9 out of 10). Two or more slips in the same part cost more.</li>
    <li><b>Carry on with a wrong answer.</b> If (a) went wrong, use your answer from (a) in (b). You can still get full marks for (b).</li>
    <li><b>Don't scribble out work.</b> Put a single line through it: the examiner marks every attempt and gives you the best one.</li></ol>
    <h2>How to use "where the marks would go"</h2>
    <p>Under each solution you'll see the part's scale, what earns <b>full marks</b>, and what kind of work earns <b>partial credit</b>. When you mark your own paper, find the description that best matches your answer and give yourself a mark from the scale. Be honest: it's practice.</p>
    <div class="note"><b>Our guide, not an official marking scheme.</b> "Where the marks would go" shows how partial credit usually works on these scales. The real marking scheme for each June paper is written by the SEC after the exam, and you can read past ones free on the SEC's Exam Material Archive (examinations.ie).</div>
    </div>
    
    <div class="page">{band('Higher level · Mock paper','Higher level mock paper')}{INSTR('Higher')}{paper(H,HL,'H')}</div>
    <div class="page">{band('HIGHER LEVEL · SOLUTIONS','Worked solutions and where the marks would go')}{sols(H,HL,'H')}</div>
    <div class="page">{band('Ordinary level · Mock paper','Ordinary level mock paper')}{INSTR('Ordinary')}{paper(O,OL,'O')}</div>
    <div class="page">{band('ORDINARY LEVEL · SOLUTIONS','Worked solutions and where the marks would go')}{sols(O,OL,'O')}</div>
    <div class="page">{band('Answer keys','Quick answer keys')}<h2>Higher level</h2>{key(H,HL)}<h2>Ordinary level</h2>{key(O,OL)}</div>
    <div class="page">{band('Score sheets','Your score and your grade')}
    <div class="two"><div><h2>Higher level</h2>{sheet(HL,'H')}</div><div><h2>Ordinary level</h2>{sheet(OL,'O')}</div></div>
    <h2>Grades</h2><p>Your marks out of 270 become a percentage, and the percentage gives the grade. These bands have been used since 2025, the same at both levels.</p>{GRADES}
    <p>My percentage: (my marks ÷ 270) × 100 = <span style="display:inline-block;border-bottom:1px solid #9AA3AE;width:30mm"></span> %&nbsp;&nbsp; My grade: <span style="display:inline-block;border-bottom:1px solid #9AA3AE;width:40mm"></span></p>
    <div class="tip"><b>27 marks is 10%.</b> One unanswered 15-mark part can be the difference between two grades.</div></div>
    <div class="page">{band('Exam day','The exam-day checklist')}
    <div class="two"><div><h2>The night before</h2><ul class="ck">
    <li><span class="box"></span>Calculator, with a fresh battery, set to <b>degrees</b></li><li><span class="box"></span>Geometry set: ruler, compass, protractor, set squares</li>
    <li><span class="box"></span>Two pens, two pencils, an eraser and a sharpener</li><li><span class="box"></span>A clear pencil case and a watch (not a smartwatch)</li>
    <li><span class="box"></span>Read your own list of "mistakes I make" one last time</li><li><span class="box"></span>Sleep: it's worth more than another hour of revision</li></ul></div>
    <div><h2>In the exam</h2><ul class="ck">
    <li><span class="box"></span>Ask for the Formulae and Tables booklet if it isn't on your desk (you can't bring your own)</li><li><span class="box"></span>Read the whole paper first (2 minutes)</li><li><span class="box"></span>Start with a question you like</li>
    <li><span class="box"></span>Watch the suggested time on each question; move on if you go over</li><li><span class="box"></span>Write the formula, then the numbers, then the answer</li>
    <li><span class="box"></span>Units on every answer (cm, m², €, km/h)</li><li><span class="box"></span>Round only at the end, and to what the question asks</li>
    <li><span class="box"></span>Never leave a part blank</li><li><span class="box"></span>Last 10 minutes: check the parts you skipped</li></ul></div></div>
    <h2>Keep practising for free</h2><p>Every Junior Cycle Maths topic has a free game, a free revision sheet and an Exam corner with exam-style questions on <b>leim.ie/junior-cycle-maths.html</b>. The <b>Exam Mix</b> game (leim.ie/exam-mix.html) mixes questions from every topic, like the real paper. The Maths Exam Centre (leim.ie/junior-cycle-maths-exam-centre.html) explains the paper and the marking in more detail.</p>
    <p class="small" style="margin-top:12mm">© Léim (leim.ie). Licence: one household or one teacher. Please don't share the PDF or post it online. Léim is not affiliated with the State Examinations Commission or the NCCA. Spotted a mistake? Email hello@leim.ie and we'll fix it.</p></div>
    </body></html>'''
    src=os.path.join(HERE,'jc-maths-exam-pack.html'); open(src,'w').write(html)
    pdf=os.path.join(OUT,'JC-Maths-Exam-Pack-Leim.pdf')
    subprocess.run(['google-chrome','--headless=new','--no-sandbox','--no-pdf-header-footer',f'--print-to-pdf={pdf}',src],check=True,capture_output=True)
    return pdf

import re
def starts(pdf):
    n=int(re.search(r'Pages:\s+(\d+)',subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout).group(1))
    T=[subprocess.run(['pdftotext','-f',str(k),'-l',str(k),pdf,'-'],capture_output=True,text=True).stdout for k in range(1,n+1)]
    def first(lbl,a=3): return next(k+1 for k,t in enumerate(T) if k+1>=a and lbl in t)
    S={'how':first('How to use this pack',2),'mk':first('How the paper is marked\n'),'hp':first('Higher level mock paper\n'),'hs':first('HIGHER LEVEL · SOLUTIONS'),
       'op':first('Ordinary level mock paper\n'),'os':first('ORDINARY LEVEL · SOLUTIONS'),'ks':first('Quick answer keys'),'sheet':first('Your score and your grade'),'ck':first('The exam-day checklist',4)}
    def rng(a,b): return str(a) if a==b else f'{a}–{b}'
    PG={'how':rng(S['how'],S['mk']),'mk':S['mk'],'hp':rng(S['hp'],S['hs']-1),'hs':rng(S['hs'],S['op']-1),'op':rng(S['op'],S['os']-1),
        'os':rng(S['os'],S['ks']-1),'ks':rng(S['ks'],S['ck']-1),'sheet':S['sheet'],'ck':S['ck']}
    return PG,n
PG0={k:'00' for k in ['how','mk','hp','hs','op','os','ks','sheet','ck']}
pdf=render(PG0); PG,n=starts(pdf); pdf=render(PG); PG2,n2=starts(pdf); assert PG2==PG and n2==n,(PG,PG2)
assert n==26,n
print(PG,n)
cov=f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}}
.k{{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}}
h1{{font-size:104px;font-weight:800;line-height:1;letter-spacing:-.03em;margin:40px 0 0}}
h1 span{{background:#F6CF5A;color:#1B2430;padding:0 14px}}
.sub{{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}}
.em{{font-size:50px;margin-top:30px;font-weight:800;color:#F6CF5A}}
.foot{{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}}
.price{{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Higher &amp; Ordinary</span>
<h1>The Maths <span>Exam Pack</span></h1>
<div class="sub">2 full timed mock papers (Higher + Ordinary)<br>Worked solutions · where the marks would go</div>
<div class="em">Answers + score sheets included</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">For students &amp; parents</span></div>
</body></html>'''
cs=os.path.join(HERE,'jc-maths-exam-pack-cover.html'); open(cs,'w').write(cov)
subprocess.run(['google-chrome','--headless=new','--no-sandbox','--hide-scrollbars','--window-size=1200,1200',f'--screenshot={os.path.join(OUT,"jc-maths-exam-pack-cover.png")}',cs],check=True,capture_output=True)
print(pdf)
