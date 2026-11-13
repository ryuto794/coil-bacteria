import io
def load(p): return io.open(p,encoding='utf-8').read()
def save(p,s): io.open(p,'w',encoding='utf-8').write(s); print('saved',p,len(s))
def rep(s,a,b):
    assert s.count(a)==1, ('count %d for: %s'%(s.count(a),a[:70]))
    return s.replace(a,b)
def afterline(s,prefix,new):
    L=s.split('\n'); idx=[i for i,l in enumerate(L) if l.startswith(prefix)]
    assert len(idx)==1, ('lines %d for prefix: %s'%(len(idx),prefix[:60]))
    L.insert(idx[0]+1,new); return '\n'.join(L)
P='/home/user/coil-bacteria/CLAUDE.md'; s=load(P)
s=rep(s,'# CLAUDE.md — コイリオ / Coilio（試作 v29.8）','# CLAUDE.md — コイリオ / Coilio（試作 v29.9）')
s=afterline(s,'v29.7 で足したもの:','\nv29.9 で足したもの: `__g.ui.end.next`（クリア画面の「次のステージへ」の位置。出ていなければ `null`）')
s=afterline(s,'- ステージの記録は `bestOf(i)`。','- 次のステージへ（v29.9、`nextStage()` / `goNext()`。オーナー「次のステージに行けるようにしようか」）: クリア画面で、次のステージがあれば、いちばん上に大きく「次のステージへ（池の水）」を出す（その下に もう一度 / タイトルへ、その下に 共有 / エンドレス）。押すか N か Enter で、そのステージがすぐ始まり、タイトルで選ぶステージもそれになる。次のステージが製品版だけ（体験版の `full:1`）なら「次のステージは製品版で」と押せないボタンを出す（続きがあることを見せる）。最後のステージ（いまは蠱毒）と、`soon:1` のステージの前では出さない（ボタンの並びは前と同じ）。強さは持ち越さない（新しく始まる）。ゲームオーバーの画面は変えていない。')
save(P,s)
P='/home/user/coil-bacteria/HANDOFF.md'; s=load(P)
s=rep(s,'# HANDOFF — コイリオ / Coilio（試作 v29.8）','# HANDOFF — コイリオ / Coilio（試作 v29.9）')
s=rep(s,'| **v29.8**（現行・試作） |','| **v29.9**（現行・試作） | クリア画面に「次のステージへ」（体験版では「次のステージは製品版で」） |\n| **v29.8**（試作） |')
SEC="""### 4.48 v29.9 で変えた仕組み（クリア画面から次のステージへ）

**なぜ:** オーナー「あとは次のステージに行けるようにしようか」。それまでは、クリアしたらタイトルへ戻って、ステージの欄を ‹ › で動かしてから始める必要があった。

**作り:** `nextStage()` は、いま遊んだステージ（`CS`）の次の番号を返す（製品版だけなら -2、ない・準備中なら -1）。`endLayout()` は、クリア画面で次がある（-1 でない）とき、いちばん上に幅いっぱいの `next`（高さ 52、横長の画面では 44）を置き、もう一度 / タイトルへを 1 段下げて少し低く（46 / 40）、共有 / エンドレスをさらに下へ置く。次がないときは前と同じ並び。`goNext()` は、クリア画面が出て 0.6 秒たってから（ほかのボタンと同じ）、`stgIdx` と保存データの `stg` を次のステージにして `reset(true)` で始める。キーは N か Enter（クリア画面だけ）。PC の画面下の説明は、次があるとき `end_mouse_n`（N：次のステージ…）。

**体験版:** 次のステージ（池の水）は製品版だけなので、押せない（灰色の）ボタンで「次のステージは製品版で」と出す。

**テスト:** `t_next.js`（ステージ 1 → 2 をタップで、2 → 3 を N で、3 では出ない、もう一度は下にずれても効く、体験版は押しても何も起きない）。

"""
s=rep(s,'\n## 5. ロードマップ（目安）','\n'+SEC+'## 5. ロードマップ（目安）')
save(P,s)
