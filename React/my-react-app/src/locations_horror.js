const locations = [
{ id: 1, position: { lat: 36.6422105660032, lng: 138.217733246194 }, message: 'あれ？…今、動いたよね？' },
{ id: 2, position: { lat: 36.66026419964217, lng: 138.18009624425352 }, message: '逃げても無駄よ。' },
{ id: 3, position: { lat: 36.65341089483074, lng: 138.18532386154683 }, message: '何かに取り憑かれてる…' },
{ id: 4, position: { lat: 36.64923300981816, lng: 138.23503900598774 }, message: '誰かがずっと見てる…' },
{ id: 5, position: { lat: 36.635363493019845, lng: 138.21533139174406 }, message: '消えた…目の前で…' },
{ id: 6, position: { lat: 36.63536273724915, lng: 138.1750403764722 }, message: 'おかえりなさい…' },
{ id: 7, position: { lat: 36.63229483225882, lng: 138.18126548310758 }, message: '夢じゃない…これは現実…' },
{ id: 8, position: { lat: 36.65761531148723, lng: 138.21918168338453 }, message: 'また同じ悪夢…' },
{ id: 9, position: { lat: 36.64930998176397, lng: 138.1747613857402 }, message: '消えた…目の前で…' },
{ id: 10, position: { lat: 36.65266135146104, lng: 138.1852684972462 }, message: '目を閉じちゃダメ！' },
{ id: 11, position: { lat: 36.63111984845971, lng: 138.21143910033103 }, message: '何かに取り憑かれてる…' },
{ id: 12, position: { lat: 36.66086566593134, lng: 138.22109718699002 }, message: '…後ろにいる。' },
{ id: 13, position: { lat: 36.65655831804095, lng: 138.21840312690648 }, message: 'ここは、あの人が死んだ場所。' },
{ id: 14, position: { lat: 36.6371282182678, lng: 138.1895497790304 }, message: '目を合わせちゃダメ…' },
{ id: 15, position: { lat: 36.63617209913069, lng: 138.22246560645826 }, message: '目を合わせちゃダメ…' },
{ id: 16, position: { lat: 36.63622159194878, lng: 138.19042543275967 }, message: '聞こえる…声が…' },
{ id: 17, position: { lat: 36.64000787778101, lng: 138.1963723303683 }, message: '声が頭に響くの…' },
{ id: 18, position: { lat: 36.6469173896273, lng: 138.22478040657225 }, message: '目を閉じちゃダメ！' },
{ id: 19, position: { lat: 36.64400927037481, lng: 138.218246048911 }, message: '…後ろにいる。' },
{ id: 20, position: { lat: 36.63960012992483, lng: 138.2317110076482 }, message: '…後ろにいる。' },
{ id: 21, position: { lat: 36.64964643870624, lng: 138.21878440255864 }, message: '目を合わせちゃダメ…' },
{ id: 22, position: { lat: 36.63484571154552, lng: 138.21275967444282 }, message: 'この匂い…血の匂い…' },
{ id: 23, position: { lat: 36.639628816132, lng: 138.18073948989573 }, message: '鍵が…開かない…' },
{ id: 24, position: { lat: 36.641954310874404, lng: 138.1992270983744 }, message: 'おかえりなさい…' },
{ id: 25, position: { lat: 36.644765193322144, lng: 138.1923112426688 }, message: 'ここに閉じ込められてるの。' },
{ id: 26, position: { lat: 36.655077281000814, lng: 138.19088017034295 }, message: 'ここに閉じ込められてるの。' },
{ id: 27, position: { lat: 36.63673136744395, lng: 138.24006204987734 }, message: '夢じゃない…これは現実…' },
{ id: 28, position: { lat: 36.64658769729671, lng: 138.20093943692513 }, message: '笑ってるのに、目が笑ってない…' },
{ id: 29, position: { lat: 36.64903736523296, lng: 138.23459998203865 }, message: 'あれ？…今、動いたよね？' },
{ id: 30, position: { lat: 36.63193032179407, lng: 138.21699837124493 }, message: '声が頭に響くの…' },
{ id: 31, position: { lat: 36.64951145205035, lng: 138.22804020802144 }, message: '出られない…ここから…' },
{ id: 32, position: { lat: 36.63581800258641, lng: 138.2083292825918 }, message: '目を合わせちゃダメ…' },
{ id: 33, position: { lat: 36.63251316445001, lng: 138.21333953721825 }, message: 'この匂い…血の匂い…' },
{ id: 34, position: { lat: 36.66020689765073, lng: 138.20764659836573 }, message: '夢じゃない…これは現実…' },
{ id: 35, position: { lat: 36.66073162629498, lng: 138.18759157860973 }, message: '昨日の私じゃない…' },
{ id: 36, position: { lat: 36.65580489153517, lng: 138.22315864588012 }, message: '彼はまだこの家にいる…' },
{ id: 37, position: { lat: 36.64001951904904, lng: 138.19336163998204 }, message: '目を合わせちゃダメ…' },
{ id: 38, position: { lat: 36.63353528405956, lng: 138.17606034261516 }, message: '目を合わせちゃダメ…' },
{ id: 39, position: { lat: 36.65191437158189, lng: 138.21796536247356 }, message: 'まだ生きてる…' },
{ id: 40, position: { lat: 36.64426644043155, lng: 138.18636832013655 }, message: '…後ろにいる。' },
{ id: 41, position: { lat: 36.63429876327872, lng: 138.23786599889743 }, message: '…後ろにいる。' },
{ id: 42, position: { lat: 36.645990555596406, lng: 138.23877472393602 }, message: '目を閉じちゃダメ！' },
{ id: 43, position: { lat: 36.631552378844304, lng: 138.23613933982227 }, message: 'お願い、こっちに来ないで…' },
{ id: 44, position: { lat: 36.658967178012574, lng: 138.19939190335288 }, message: '彼はまだこの家にいる…' },
{ id: 45, position: { lat: 36.63858337972347, lng: 138.17546266500005 }, message: '誰かいるの…？' },
{ id: 46, position: { lat: 36.65123409503807, lng: 138.2370469975784 }, message: 'この匂い…血の匂い…' },
{ id: 47, position: { lat: 36.64024190349745, lng: 138.20330646952235 }, message: '…後ろにいる。' },
{ id: 48, position: { lat: 36.646770484669524, lng: 138.2396332733867 }, message: 'おかえりなさい…' },
{ id: 49, position: { lat: 36.6476052835526, lng: 138.23942853408624 }, message: '夢じゃない…これは現実…' },
{ id: 50, position: { lat: 36.636267024022146, lng: 138.2319664252979 }, message: 'もう戻れない…' },
{ id: 51, position: { lat: 36.66085547546768, lng: 138.19428429860838 }, message: '笑ってる…あれ…誰？' },
{ id: 52, position: { lat: 36.65476259294549, lng: 138.20039973382939 }, message: '目を合わせちゃダメ…' },
{ id: 53, position: { lat: 36.65991278145575, lng: 138.23184008182378 }, message: '聞こえる…声が…' },
{ id: 54, position: { lat: 36.65851305797307, lng: 138.19580040044215 }, message: 'もう戻れない…' },
{ id: 55, position: { lat: 36.649209243084684, lng: 138.18585439214965 }, message: '目を閉じちゃダメ！' },
{ id: 56, position: { lat: 36.65936053527438, lng: 138.21198335562406 }, message: '声が頭に響くの…' },
{ id: 57, position: { lat: 36.63324765341808, lng: 138.23757565129407 }, message: '笑ってる…あれ…誰？' },
{ id: 58, position: { lat: 36.63661571749954, lng: 138.22137611911103 }, message: '鍵が…開かない…' },
{ id: 59, position: { lat: 36.63189199687493, lng: 138.21287790771382 }, message: '鍵が…開かない…' },
{ id: 60, position: { lat: 36.640668644298444, lng: 138.1809757265534 }, message: 'おかえりなさい…' },
{ id: 61, position: { lat: 36.64265353500213, lng: 138.2159100999421 }, message: '何かに取り憑かれてる…' },
{ id: 62, position: { lat: 36.638977213796444, lng: 138.24121184035081 }, message: '出られない…ここから…' },
{ id: 63, position: { lat: 36.656442222785714, lng: 138.18387039324804 }, message: '出られない…ここから…' },
{ id: 64, position: { lat: 36.641653241089855, lng: 138.20938794846404 }, message: '…後ろにいる。' },
{ id: 65, position: { lat: 36.63927756169512, lng: 138.23361006600985 }, message: '昨日の私じゃない…' },
{ id: 66, position: { lat: 36.64747950418094, lng: 138.22439433062527 }, message: 'あれ？…今、動いたよね？' },
{ id: 67, position: { lat: 36.63489053006397, lng: 138.221442633794 }, message: '目を閉じちゃダメ！' },
{ id: 68, position: { lat: 36.655610611466386, lng: 138.2218115441806 }, message: '誰かいるの…？' },
{ id: 69, position: { lat: 36.632810804269454, lng: 138.19867223934403 }, message: 'ドアが勝手に…' },
{ id: 70, position: { lat: 36.66139761975594, lng: 138.19422647966073 }, message: '夢じゃない…これは現実…' },
{ id: 71, position: { lat: 36.654672099703795, lng: 138.22902178352092 }, message: 'もうすぐ、あなたの番。' },
{ id: 72, position: { lat: 36.636701346665454, lng: 138.22907253177405 }, message: '聞こえる…声が…' },
{ id: 73, position: { lat: 36.6306478893802, lng: 138.2329151471092 }, message: '昨日の私じゃない…' },
{ id: 74, position: { lat: 36.656026234874005, lng: 138.2360297909916 }, message: '出られない…ここから…' },
{ id: 75, position: { lat: 36.65262327375995, lng: 138.2089165679389 }, message: 'もう戻れない…' },
{ id: 76, position: { lat: 36.653317308341485, lng: 138.20825367025762 }, message: '誰かがずっと見てる…' },
{ id: 77, position: { lat: 36.65464156749808, lng: 138.22827524043106 }, message: 'ドアが勝手に…' },
{ id: 78, position: { lat: 36.6327949497008, lng: 138.2182683812782 }, message: 'あれ？…今、動いたよね？' },
{ id: 79, position: { lat: 36.64170689687021, lng: 138.22177665190432 }, message: 'あれ？…今、動いたよね？' },
{ id: 80, position: { lat: 36.63410546057013, lng: 138.22810641383043 }, message: '聞こえる…声が…' },
{ id: 81, position: { lat: 36.65751903199305, lng: 138.23446227582477 }, message: '彼はまだこの家にいる…' },
{ id: 82, position: { lat: 36.65000505947024, lng: 138.19722205679236 }, message: '助けて…誰か…' },
{ id: 83, position: { lat: 36.64084310041167, lng: 138.19975783925838 }, message: '消えた…目の前で…' },
{ id: 84, position: { lat: 36.632466375723254, lng: 138.18076021261672 }, message: '出られない…ここから…' },
{ id: 85, position: { lat: 36.640219068971426, lng: 138.21343238349183 }, message: '誰かいるの…？' },
{ id: 86, position: { lat: 36.64066403797986, lng: 138.17684468726063 }, message: 'また同じ悪夢…' },
{ id: 87, position: { lat: 36.65333607751352, lng: 138.20583051843434 }, message: 'あれ？…今、動いたよね？' },
{ id: 88, position: { lat: 36.650451856615256, lng: 138.21102830817645 }, message: '助けて…誰か…' },
{ id: 89, position: { lat: 36.658274464604226, lng: 138.1937508261264 }, message: 'まだ生きてる…' },
{ id: 90, position: { lat: 36.645271073063434, lng: 138.21427925359527 }, message: '何かに取り憑かれてる…' },
{ id: 91, position: { lat: 36.63422218421411, lng: 138.17647755243965 }, message: '消えた…目の前で…' },
{ id: 92, position: { lat: 36.65282341560087, lng: 138.1769395343888 }, message: '…後ろにいる。' },
{ id: 93, position: { lat: 36.65431302496005, lng: 138.22991495245552 }, message: '声が頭に響くの…' },
{ id: 94, position: { lat: 36.648061718100664, lng: 138.198719428995 }, message: '笑ってるのに、目が笑ってない…' },
{ id: 95, position: { lat: 36.65463206818135, lng: 138.18299178973305 }, message: '笑ってるのに、目が笑ってない…' },
{ id: 96, position: { lat: 36.645947274010965, lng: 138.20965197186723 }, message: '彼はまだこの家にいる…' },
{ id: 97, position: { lat: 36.64685398280616, lng: 138.22636593010492 }, message: 'この匂い…血の匂い…' },
{ id: 98, position: { lat: 36.643871277022484, lng: 138.18897983325886 }, message: '出られない…ここから…' },
{ id: 99, position: { lat: 36.63127133508456, lng: 138.21644192694802 }, message: '声が頭に響くの…' },
{ id: 100, position: { lat: 36.633855492317224, lng: 138.18017770572953 }, message: 'この匂い…血の匂い…' },
{ id: 101, position: { lat: 36.63145965209814, lng: 138.17790651634195 }, message: 'まだ生きてる…' },
{ id: 102, position: { lat: 36.650415915049145, lng: 138.21026665159613 }, message: '目を合わせちゃダメ…' },
{ id: 103, position: { lat: 36.64032477799386, lng: 138.2108927405548 }, message: '誰かがずっと見てる…' },
{ id: 104, position: { lat: 36.64641023148852, lng: 138.2174227990617 }, message: '笑ってるのに、目が笑ってない…' },
{ id: 105, position: { lat: 36.65891222106209, lng: 138.22340415818456 }, message: 'お願い、こっちに来ないで…' },
{ id: 106, position: { lat: 36.6382860939191, lng: 138.24025374743195 }, message: '出られない…ここから…' },
{ id: 107, position: { lat: 36.64333365146828, lng: 138.2092510456861 }, message: 'あれ？…今、動いたよね？' },
{ id: 108, position: { lat: 36.65414902751446, lng: 138.1962075032605 }, message: '聞こえる…声が…' },
{ id: 109, position: { lat: 36.63764394033945, lng: 138.22806549927836 }, message: '声が頭に響くの…' },
{ id: 110, position: { lat: 36.6328869220165, lng: 138.19269105105528 }, message: '鍵が…開かない…' },
{ id: 111, position: { lat: 36.63955382860582, lng: 138.20403421041817 }, message: '彼はまだこの家にいる…' },
{ id: 112, position: { lat: 36.635526510873675, lng: 138.17971281310338 }, message: '聞こえる…声が…' },
{ id: 113, position: { lat: 36.65960567140359, lng: 138.1761301516922 }, message: 'あれ？…今、動いたよね？' },
{ id: 114, position: { lat: 36.65579621310271, lng: 138.23936298964887 }, message: '鍵が…開かない…' },
{ id: 115, position: { lat: 36.65032170561636, lng: 138.23081757663354 }, message: '夢じゃない…これは現実…' },
{ id: 116, position: { lat: 36.657780892357515, lng: 138.2213723688081 }, message: 'まだ生きてる…' },
{ id: 117, position: { lat: 36.65565683159558, lng: 138.202009076349 }, message: '鍵が…開かない…' },
{ id: 118, position: { lat: 36.63632078011746, lng: 138.18611085739136 }, message: '出られない…ここから…' },
{ id: 119, position: { lat: 36.65844198225373, lng: 138.18497361623213 }, message: '笑ってる…あれ…誰？' },
{ id: 120, position: { lat: 36.64737441613225, lng: 138.19130203317124 }, message: '聞こえる…声が…' },
{ id: 121, position: { lat: 36.65577489919733, lng: 138.21147235114069 }, message: '助けて…誰か…' },
{ id: 122, position: { lat: 36.65855266210951, lng: 138.22262864418863 }, message: 'もうすぐ、あなたの番。' },
{ id: 123, position: { lat: 36.64043906724859, lng: 138.21895875942454 }, message: '消えた…目の前で…' },
{ id: 124, position: { lat: 36.633923188565696, lng: 138.1933050746513 }, message: '鍵が…開かない…' },
{ id: 125, position: { lat: 36.6376168993171, lng: 138.23883791670028 }, message: '笑ってる…あれ…誰？' },
{ id: 126, position: { lat: 36.643857702358716, lng: 138.22420059728606 }, message: '誰かいるの…？' },
{ id: 127, position: { lat: 36.65610624022688, lng: 138.2118182596948 }, message: '笑ってるのに、目が笑ってない…' },
{ id: 128, position: { lat: 36.65744468220048, lng: 138.21568838437292 }, message: '逃げても無駄よ。' },
{ id: 129, position: { lat: 36.630692696903196, lng: 138.2027273620214 }, message: '鍵が…開かない…' },
{ id: 130, position: { lat: 36.646478432643434, lng: 138.19113257247764 }, message: '逃げろ…今すぐ…' },
{ id: 131, position: { lat: 36.643553866789084, lng: 138.1984348729101 }, message: 'もう戻れない…' },
{ id: 132, position: { lat: 36.63743430717457, lng: 138.2255464281524 }, message: '出られない…ここから…' },
{ id: 133, position: { lat: 36.63423067943388, lng: 138.17539094328748 }, message: '誰かいるの…？' },
{ id: 134, position: { lat: 36.64105357305267, lng: 138.18225051579188 }, message: '昨日の私じゃない…' },
{ id: 135, position: { lat: 36.66001965304979, lng: 138.1775233890789 }, message: 'ここに閉じ込められてるの。' },
{ id: 136, position: { lat: 36.64060198515555, lng: 138.17716760045212 }, message: '誰かいるの…？' },
{ id: 137, position: { lat: 36.646730459097576, lng: 138.23213178558711 }, message: 'ここは、あの人が死んだ場所。' },
{ id: 138, position: { lat: 36.65250300319388, lng: 138.22189073049623 }, message: '昨日の私じゃない…' },
{ id: 139, position: { lat: 36.641868699825615, lng: 138.20640906768404 }, message: '何かに取り憑かれてる…' },
{ id: 140, position: { lat: 36.66092432972664, lng: 138.18102009468163 }, message: 'もう戻れない…' },
{ id: 141, position: { lat: 36.660631836861995, lng: 138.20758575904264 }, message: '彼はまだこの家にいる…' },
{ id: 142, position: { lat: 36.63836411676789, lng: 138.20636170478053 }, message: 'お願い、こっちに来ないで…' },
{ id: 143, position: { lat: 36.646055466229484, lng: 138.18610462043355 }, message: '彼はまだこの家にいる…' },
{ id: 144, position: { lat: 36.639902473516365, lng: 138.20368881568444 }, message: 'もうすぐ、あなたの番。' },
{ id: 145, position: { lat: 36.639399950406926, lng: 138.20130420959086 }, message: '…後ろにいる。' },
{ id: 146, position: { lat: 36.63163066362862, lng: 138.2159669625049 }, message: '笑ってるのに、目が笑ってない…' },
{ id: 147, position: { lat: 36.64957472977152, lng: 138.21726518877196 }, message: 'ここは、あの人が死んだ場所。' },
{ id: 148, position: { lat: 36.64622562409594, lng: 138.17747625730723 }, message: '逃げても無駄よ。' },
{ id: 149, position: { lat: 36.63208787793524, lng: 138.19969237742245 }, message: '…後ろにいる。' },
{ id: 150, position: { lat: 36.63920586890636, lng: 138.21664225403458 }, message: '何かに取り憑かれてる…' },
{ id: 151, position: { lat: 36.65893413618605, lng: 138.20836295775237 }, message: '…後ろにいる。' },
{ id: 152, position: { lat: 36.637981207011755, lng: 138.2322012222819 }, message: '目を閉じちゃダメ！' },
{ id: 153, position: { lat: 36.635014944884865, lng: 138.21885731238902 }, message: 'ドアが勝手に…' },
{ id: 154, position: { lat: 36.64581119715546, lng: 138.18541194875783 }, message: 'また同じ悪夢…' },
{ id: 155, position: { lat: 36.661358876260735, lng: 138.17918069028454 }, message: 'また同じ悪夢…' },
{ id: 156, position: { lat: 36.63805933370549, lng: 138.21775939698418 }, message: '聞こえる…声が…' },
{ id: 157, position: { lat: 36.651535313546226, lng: 138.17620844693957 }, message: '何かに取り憑かれてる…' },
{ id: 158, position: { lat: 36.6543391749716, lng: 138.21393804778077 }, message: 'ここは、あの人が死んだ場所。' },
{ id: 159, position: { lat: 36.63792091022893, lng: 138.2378505942167 }, message: '笑ってるのに、目が笑ってない…' },
{ id: 160, position: { lat: 36.653292529091466, lng: 138.2132430850259 }, message: '助けて…誰か…' },
{ id: 161, position: { lat: 36.641998845043304, lng: 138.20060699325109 }, message: 'ここに閉じ込められてるの。' },
{ id: 162, position: { lat: 36.65028730360271, lng: 138.21781801822993 }, message: '誰かいるの…？' },
{ id: 163, position: { lat: 36.6503256522213, lng: 138.20533499467479 }, message: '彼はまだこの家にいる…' },
{ id: 164, position: { lat: 36.64726263156495, lng: 138.2112288184055 }, message: '夢じゃない…これは現実…' },
{ id: 165, position: { lat: 36.63330396836375, lng: 138.23793388173536 }, message: 'ここに閉じ込められてるの。' },
{ id: 166, position: { lat: 36.65664792769673, lng: 138.20046752793843 }, message: '笑ってるのに、目が笑ってない…' },
{ id: 167, position: { lat: 36.64052606791559, lng: 138.2392646387731 }, message: '笑ってる…あれ…誰？' },
{ id: 168, position: { lat: 36.63631916491583, lng: 138.23549751458273 }, message: 'また同じ悪夢…' },
{ id: 169, position: { lat: 36.63175249489965, lng: 138.18762855820643 }, message: 'あれ？…今、動いたよね？' },
{ id: 170, position: { lat: 36.64898968716434, lng: 138.17909923241604 }, message: 'まだ生きてる…' },
{ id: 171, position: { lat: 36.651705418054625, lng: 138.18121869477352 }, message: '目を閉じちゃダメ！' },
{ id: 172, position: { lat: 36.63099461839233, lng: 138.1756492140823 }, message: 'おかえりなさい…' },
{ id: 173, position: { lat: 36.646520600066566, lng: 138.1807913144339 }, message: 'もうすぐ、あなたの番。' },
{ id: 174, position: { lat: 36.637571798074575, lng: 138.22049754793278 }, message: '…後ろにいる。' },
{ id: 175, position: { lat: 36.65069047226868, lng: 138.17922251062026 }, message: '彼はまだこの家にいる…' },
{ id: 176, position: { lat: 36.6359383959918, lng: 138.19593894399083 }, message: '目を合わせちゃダメ…' },
{ id: 177, position: { lat: 36.65212445459033, lng: 138.2314176721571 }, message: 'お願い、こっちに来ないで…' },
{ id: 178, position: { lat: 36.64259268685022, lng: 138.1759899092557 }, message: 'おかえりなさい…' },
{ id: 179, position: { lat: 36.659826020089156, lng: 138.22936633872195 }, message: 'おかえりなさい…' },
{ id: 180, position: { lat: 36.63478389289316, lng: 138.1934346626788 }, message: '聞こえる…声が…' },
{ id: 181, position: { lat: 36.64116171106772, lng: 138.18239166084416 }, message: '誰かいるの…？' },
{ id: 182, position: { lat: 36.63403039963979, lng: 138.22142384026841 }, message: '目を閉じちゃダメ！' },
{ id: 183, position: { lat: 36.65944887680977, lng: 138.2168502375669 }, message: '彼はまだこの家にいる…' },
{ id: 184, position: { lat: 36.65796509539756, lng: 138.23361674089904 }, message: '誰かいるの…？' },
{ id: 185, position: { lat: 36.638557111046005, lng: 138.2240099556488 }, message: 'お願い、こっちに来ないで…' },
{ id: 186, position: { lat: 36.65115456279643, lng: 138.22862508636493 }, message: 'あれ？…今、動いたよね？' },
{ id: 187, position: { lat: 36.656081406259176, lng: 138.1934467923633 }, message: 'ここに閉じ込められてるの。' },
{ id: 188, position: { lat: 36.64787132282, lng: 138.18639050628747 }, message: 'ここに閉じ込められてるの。' },
{ id: 189, position: { lat: 36.64707074105094, lng: 138.2250585795695 }, message: '鍵が…開かない…' },
{ id: 190, position: { lat: 36.63805297358443, lng: 138.22885134410578 }, message: 'この匂い…血の匂い…' },
{ id: 191, position: { lat: 36.63339210981807, lng: 138.24124228582 }, message: 'お願い、こっちに来ないで…' },
{ id: 192, position: { lat: 36.65858789547079, lng: 138.2022563099048 }, message: 'また同じ悪夢…' },
{ id: 193, position: { lat: 36.658688235156234, lng: 138.1995173429309 }, message: 'ここは、あの人が死んだ場所。' },
{ id: 194, position: { lat: 36.65031223348138, lng: 138.2267990020902 }, message: '…後ろにいる。' },
{ id: 195, position: { lat: 36.64109789823308, lng: 138.19741151853754 }, message: '聞こえる…声が…' },
{ id: 196, position: { lat: 36.641416867890094, lng: 138.23721152365303 }, message: '笑ってる…あれ…誰？' },
{ id: 197, position: { lat: 36.65322169408328, lng: 138.23233094744987 }, message: 'ここに閉じ込められてるの。' },
{ id: 198, position: { lat: 36.65858458983458, lng: 138.20336110632854 }, message: 'ここに閉じ込められてるの。' },
{ id: 199, position: { lat: 36.65827050659194, lng: 138.2250758714055 }, message: '昨日の私じゃない…' },
{ id: 200, position: { lat: 36.654911199697146, lng: 138.22532358218027 }, message: '彼はまだこの家にいる…' }
];

export default locations;